#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  name:        _02_valley_bottoms.py
#  purpose:     Classify landforms with geomorphons and isolate valley bottoms.
#
#  author:      Jeff Howarth
#  update:      04/07/2023
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
starts = root+"/inputs/" 

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Required datasets:
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Point to directory where you hold input data. 
# The 'midd' DEM is relatively small and good for testing. 

dem =root+"/inputs/DEM_10m_midd.tif" 
lc = starts+"LCHP_1m_Midd.tif"

# ------------------------------------------------------------------------------
# IMPLEMENT
# ------------------------------------------------------------------------------

# Classify landforms from DEM with geomorphons. 
# See WBT manual for parameter definitions.

wbt.geomorphons(
    dem = dem, 
    output = temps + "_0201_landforms.tif", # note: apparently it can id keeps within root
    search=100, 
    threshold=0.0, 
    fdist=0, 
    skip=0, 
    forms=True, 
    residuals=False, 
    # callback=default_callback
)


# Threshold landform class to isolate valley bottoms. 
 
wbt.greater_than( # in "math and statistical analysis" in wbt
    # returns a 1 if input1 greater than (or equal to if set true) input2
    # in this case, gives 1 for valleys and pits
  input1 = temps+"_0201_landforms.tif", 
  input2 = 7,
  output = temps+"_0202_valley_bottoms.tif",
  incl_equals=True
)

# Remove noise by taking majority class within neighborhood kernel filter.

wbt.majority_filter( # in "filters" in wbt
    # moving kernel over every pixel in an image, it assigns to a new image the value of the mode within the search distance for each pixel
    i = temps+"_0202_valley_bottoms.tif",                   # i = input raster file
    output = temps+"_0203_valley_bottoms_smoothed.tif",     # o = output raster file
    filterx=5,                                              # Size of the filter kernel in the x-direction
    filtery=5                                               # Size of the filter kernel in the y-direction
  )

# Clump valley bottoms into distinct objects. 
wbt.clump( #create clumps -- finding each contiguous section of lowlands
    i = temps+"_0203_valley_bottoms_smoothed.tif", 
    output = keeps+"_0204_valley_bottoms_clumps.tif", 
    diag=True, 
    zero_back=True, 
)

# ------------------------------------------------------------------------------
# Remove developed land cover from valley bottoms. 
# ------------------------------------------------------------------------------

# Resample lc to match valley cell size. 

valleys = keeps+"_0204_valley_bottoms_clumps.tif"

wbt.resample(
    inputs = lc, 
    output = temps+"_0211_lc_resample.tif", 
    cell_size = None, 
    base = valleys, 
    method = "nn"
)

# Reclassify lc to make developed land eraser.

# NOT SURE WHERE TO FIND THE STUFF
wbt.reclass( # in "gis analysis" in wbt
    # reclass allows a user to specify how to change the values in an input raster to an output raster
    i = temps+"_0211_lc_resample.tif",                                     # input raster
    output = temps+"_0212_devt_eraser.tif",                                  # output raster
    reclass_vals = "1;1;1;2;1;3;1;4;0;5;0;6;0;7;0;8;0;9;0;10",      # FIX THE RECLASS
    assign_mode=True                                                    # reclass_vals values are interpreted as new value; old value pairs (INSTEAD OF TRIPLETS)
) # note: possible to work with NoData and if a number is not within a range it will remain its value in new raster


# Erase developed land from valley bottoms.  
wbt.multiply(
    input1 = temps+"_0212_devt_eraser.tif", 
    input2 = temps+"_0211_lc_resample.tif", 
    output = temps+"_0213_valleys_devt_erased.tif", 
)


# Re-clump undeveloped lowlands to identify individual objects. 
wbt.clump(
    i = temps+"_0213_valleys_devt_erased.tif", 
    output = temps+"_0214_valleys_devt_erased_clumps.tif", 
    diag=True, 
    zero_back=True
)


# ------------------------------------------------------------------------------
# Make copies of output with background masked and background 0.
# ------------------------------------------------------------------------------

# Mask background.
wbt.set_nodata_value(
    i = temps+"_0214_valleys_devt_erased_clumps.tif", 
    output = keeps+"_0215_potential_connector_clumps.tif", 
    back_value=0.0,
)


