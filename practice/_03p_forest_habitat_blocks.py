#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  name:        _03_forest_habitat_blocks.py
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

# Point to directory where you hold input data. 
# The 'midd' DEM is relatively small and good for testing. 

lc = root+"/inputs/LCHP_1m_midd.tif"  

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPLEMENT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ------------------------------------------------------------------------------
# 1. Identify clumps of recovering habitat. 
# ------------------------------------------------------------------------------

# Resample LCHP to 3 meter to speed up pilot. 



# Make a binary where recovering habitat = 0 and not recovering habitat = 1.



# Pass a majority filter over the binary to remove noise from random pixels.  



# Buffer 50 meters into recovering habitat to identify cores.  
# Because images sometimes lose their crs information, it can be safer to specific distance in cell units. 



# Invert figure and ground.  



# Identify clumps of core recovering habitat. 
 

# ------------------------------------------------------------------------------
# 2. Identify recovering clumps with a majority of tree canopy. 
# ------------------------------------------------------------------------------

# Compute area of each core recovering habitat clump.



# Make a binary of tree canopy. 



# Count the number of tree canopy pixels in each clump.  



# Divide the count of tree canopy by the pixel area of each clump. 



# Replace background value with zero.


# Threshold habitat blocks by percent tree canopy (> 49%). 



# ------------------------------------------------------------------------------
# 3. Identify clumps of tree canopy that overlap blocks          . 
# ------------------------------------------------------------------------------

# Clump tree canopy binary to identify stands of trees. 



# Set background as no data. 




# Identify tree stands that overlap habitat blocks with majority trees. 



# ------------------------------------------------------------------------------
# 4. Combine habitat blocks with majority of trees and overlapping tree stands.         . 
# ------------------------------------------------------------------------------

# Replace background value with zeros for overlapping tree stands.



# Union the overlapping tree stands and habitat blocks. 



# Identify individual forested habitat blocks. 



# ------------------------------------------------------------------------------
# 5. Classify forested habitat blocks by area. 
# ------------------------------------------------------------------------------

# Set background as no data. 



# Compute the area of each block. 



# Convert square meters to acres.

