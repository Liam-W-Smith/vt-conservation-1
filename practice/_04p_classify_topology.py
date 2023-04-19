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

wbt.resample( # in "image processing tools" in wbt
    # resample basically changes the raster to a new resolution -- in this case, we want a coarser resolution
    inputs = blocks,                           # input raster
    output = temps+"_0401_blocks_resample.tif",       # output raster
    cell_size = None,                          # new cell size (OR USE FOLLOWING)
    base = valleys,                            # base raster file (OR USE ABOVE) sets extent and cell size
    method = "nn"                              # resampling method -- here we use nearest neighbor bc we have categorical data
)

# Erase clumps from valley bottoms
wbt.equal_to( # so we have the interior "recovering habitat", which is the interior tree, grass, and water
    # if  input1 = input2, we return 1; else, 0
    input1 = temps+"_0401_blocks_resample.tif", 
    input2 = 0, 
    output = temps+"_0402_inverse_binary.tif"
)

wbt.multiply(
    input1 = temps+"_0402_inverse_binary.tif",
    input2 = valleys,
    output = temps+"_0403_valleys_not_blocks.tif"
)

wbt.multiply(
    input1 = temps+"_0403_valleys_not_blocks.tif",
    input2 = 0,
    output = temps+"_0404_blank_image.tif"
)

wbt.divide(
    input1 = temps+"_0403_valleys_not_blocks.tif",
    input2 = temps+"_0403_valleys_not_blocks.tif",
    output = temps+"_0405_clumps_1s.tif"
)

wbt.convert_nodata_to_zero(
    i = temps+"_0405_clumps_1s.tif", 
    output = temps+"_0406_back0.tif", 
    # callback=None
)

# then buffer
wbt.buffer_raster(
    # creates buffer around nonzero cells (the cells that are NOT tree, grass, water)
    i = temps+"_0406_back0.tif",       # input raster
    output = temps+"_407_buffered_1s.tif", # output raster 
    size = 2,                             # buffer size in cells
    gridcells=True                         # if true, we're working in number of cells rather than default map units
)
# then clump
# then assign value?

# JEFF STUFF
# clump then
# wbt.maximum_filter(
#     i = temps+"_0403_valleys_not_blocks.tif",
#     output = temps + ...
#     filterx = 3,
#     filtery = 3
# )

# set no data to 0

# then do the zonal stat