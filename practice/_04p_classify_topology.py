#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  name:        _0.py
#  purpose:     Classify forest habitat blocks from land cover.
#
#  author:      Jeff Howarth
#  update:      04/08/2023
#  license:     Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import tools from WBT module

import sys
sys.path.insert(1, '/Users/liamsmith/Documents/GEOG_310/wbt_starter')     # path points to my WBT directory
from WBT.whitebox_tools import WhiteboxTools

# declare a name for the tools

wbt = WhiteboxTools()

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Working directories
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define personal storage root.
# This is the path where you will store inputs and outputs from this workflow.
# For example, my root points to the directory (folder) of s23 in GEOG0310 
# on an external drive named drosera. 

root = "/Users/liamsmith/Documents/GEOG_310/vt-conservation/practice/practice_files"

# Set up separate directories to store temporary and keeper outputs. 

temps = root+"/temps/"     
keeps = root+"/keeps/"   

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Required datasets:
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

valleys = keeps+"_0204_valley_bottoms_clumps.tif"
blocks = temps+"_0343_forested_habitat_blocks.tif"


# ==============================================================================
# WORKFLOW
# ==============================================================================

# currently, valleys res is 10 m and blocks is 3 m. We MUST make everything in the same cell size. (extent is good)

# ------------------------------------------------------------------------------
# Align images
# ------------------------------------------------------------------------------

# wbt.resample( # in "image processing tools" in wbt
#     # resample basically changes the raster to a new resolution -- in this case, we want a coarser resolution
#     inputs = blocks,                           # input raster
#     output = temps+"_0401_blocks_resample.tif",       # output raster
#     cell_size = None,                          # new cell size (OR USE FOLLOWING)
#     base = valleys,                            # base raster file (OR USE ABOVE) sets extent and cell size
#     method = "nn"                              # resampling method -- here we use nearest neighbor bc we have categorical data
# )

# # Erase clumps from valley bottoms
# wbt.equal_to( # so we have the interior "recovering habitat", which is the interior tree, grass, and water
#     # if  input1 = input2, we return 1; else, 0
#     input1 = temps+"_0401_blocks_resample.tif", 
#     input2 = 0, 
#     output = temps+"_0402_inverse_binary.tif"
# )

# wbt.multiply(
#     input1 = temps+"_0402_inverse_binary.tif",
#     input2 = valleys,
#     output = temps+"_0403_valleys_not_blocks.tif"
# )

# wbt.multiply(
#     input1 = temps+"_0403_valleys_not_blocks.tif",
#     input2 = 0,
#     output = temps+"_0404_blank_image.tif"
# )

# wbt.divide(
#     input1 = temps+"_0403_valleys_not_blocks.tif",
#     input2 = temps+"_0403_valleys_not_blocks.tif",
#     output = temps+"_0405_clumps_1s.tif"
# )

# wbt.convert_nodata_to_zero(
#     i = temps+"_0405_clumps_1s.tif", 
#     output = temps+"_0406_back0.tif", 
#     # callback=None
# )

# # then buffer
# wbt.buffer_raster(
#     # creates buffer around nonzero cells (the cells that are NOT tree, grass, water)
#     i = temps+"_0406_back0.tif",       # input raster
#     output = temps+"_407_buffered_1s.tif", # output raster 
#     size = 2,                             # buffer size in cells
#     gridcells=True                         # if true, we're working in number of cells rather than default map units
# )
# # then clump
# # then assign value?

# # JEFF STUFF
# # clump then
# # wbt.maximum_filter(
# #     i = temps+"_0403_valleys_not_blocks.tif",
# #     output = temps + ...
# #     filterx = 3,
# #     filtery = 3
# # )

# # set no data to 0

# # then do the zonal stat

# ==============================================================================
# JEFF'S WORKFLOW
# ==============================================================================

# ------------------------------------------------------------------------------
# Align images: must be same extent and cell size. 
# ------------------------------------------------------------------------------

# Resample blocks to match valley cell size. 

wbt.resample(
    inputs = blocks, 
    output = temps+"_0401_resample.tif", 
    cell_size = None, 
    base = valleys, 
    method = "nn"
)


# ------------------------------------------------------------------------------
# Erase valleys where they overlap blocks. 
# ------------------------------------------------------------------------------

# Convert blocks into an inverse binary. 

wbt.equal_to(
    input1 = temps+"_0401_resample.tif", 
    input2 = 0, 
    output = temps+"_0411_inverse_binary.tif", 
)

# Erase blocks from valley bottoms.  

wbt.multiply(
    input1 = temps+"_0411_inverse_binary.tif", 
    input2 = valleys, 
    output = temps+"_0412_valleys_not_blocks.tif", 
)

# # Re-clump valley bottoms to identify individual objects. BC BY taking away the forested parts of valley bottoms, we have made new islands 

wbt.clump(
    i = temps+"_0412_valleys_not_blocks.tif", 
    output = temps+"_0413_valleys_not_blocks_clumps.tif", 
    diag=True, 
    zero_back=True
) # OUTPUT: all possible connectors. we need to remove islands and spits

# ------------------------------------------------------------------------------
# Identify and remove islands. 
# ------------------------------------------------------------------------------

# Grow valley bottom edge by one pixel.

wbt.maximum_filter(
    i = temps+"_0413_valleys_not_blocks_clumps.tif", 
    output = temps+"_0414_valleys_not_blocks_clumps_extra_edge.tif", 
    filterx=3, 
    filtery=3
)

# Mask background.

wbt.set_nodata_value(
    i = temps+"_0414_valleys_not_blocks_clumps_extra_edge.tif", 
    output = temps+"_0415_valleys_not_blocks_extra_edge_clumps_bg_masked.tif", 
    back_value=0.0,
)

# Test for overlap between valley bottoms and habitat blocks.

wbt.zonal_statistics(
    i = temps+"_0401_resample.tif", 
    features = temps+"_0415_valleys_not_blocks_extra_edge_clumps_bg_masked.tif", 
    output = temps+"_0416_test_overlap.tif", 
    stat = "max", 
    out_table = None
) # if valley bottom connector overlaps block, retains the value of the block. if not, it retains the value 0. doesn't consider spots that are not valley bottom connectors

# Mask islands.  

wbt.set_nodata_value(
    i = temps+"_0416_test_overlap.tif", 
    output = temps+"_0417_not_islands.tif", 
    back_value=0.0, 
)

# Re-clump valley bottoms without islands to identify individual objects. 
  # currently their value is the value of the forest block, so they are NOT UNIQUELY IDENTIFIED. WE fix below
wbt.clump(
    i = temps+"_0417_not_islands.tif", 
    output = temps+"_0418_not_island_clumps.tif", 
    diag=True, 
    zero_back=True
)

# # ------------------------------------------------------------------------------
# Select corridors. 
# ------------------------------------------------------------------------------

# Set background of blocks to no data. 

wbt.set_nodata_value(
    i = temps+"/_0401_resample.tif", 
    output = temps+"_0421_resample_blocks_mask_bg.tif", 
    back_value=0.0, 
)

# Test for min of overlap.

wbt.zonal_statistics(
    i = temps+"_0421_resample_blocks_mask_bg.tif", 
    features = temps+"_0418_not_island_clumps.tif", 
    output=temps+"_0422_valley_blocks_overlap_min.tif", 
    stat="min", 
    out_table=None, 
)

# Test for max of overlap.

wbt.zonal_statistics(
    i = temps+"_0421_resample_blocks_mask_bg.tif", 
    features = temps+"_0418_not_island_clumps.tif", 
    output=temps+"_0423_valley_blocks_overlap_max.tif", 
    stat="max", 
    out_table=None, 
)

# Bridges (tombolos) will have unequal min and max values, 
# while piers (spits) will have equal min and max values. 

wbt.not_equal_to(
    input1 = temps+"_0423_valley_blocks_overlap_max.tif", 
    input2 = temps+"_0422_valley_blocks_overlap_min.tif", 
    output = temps+"_0424_valley_corridors_test.tif", 
)

# Unmask background values. 

wbt.convert_nodata_to_zero(
    i = temps+"_0424_valley_corridors_test.tif", 
    output = temps+"_0425_valley_corridors_test_bg_0.tif"
)

# Select valley bottom corridors. 

wbt.zonal_statistics(
    i = temps+"_0425_valley_corridors_test_bg_0.tif", 
    features = temps+"_0414_valleys_not_blocks_clumps_extra_edge.tif", 
    output=keeps+"_0426_valley_corridors.tif", 
    stat="max", 
    out_table=None
)