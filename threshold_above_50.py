# -*- coding: utf-8 -*-
"""
@author: bern

part 4 of analysis
now that i have the rasters with damage values for 2020 and 2030 (both original and policy damage curves).
extract the significantly damaged areas (threshold of 50%).

i.e if they have 50% or more damage,the pixel is considered as significantly damaged 
(and subsequently all buildings in that pixel as well)

input folder: output from part 2 analysis (rasters with damage values)
output folder: rasters with damage values that hit the damage threshold (considered significantly damaged)
change file/folder paths based on years and return periods. 
"""
import rasterio
import numpy as np

# List of return periods
# Edit according to naming 
return_periods = ["RP1", "RP2", "RP5", "RP10", "RP25", "RP50", "RP100", "RP250", "RP500", "RP1000", "RP2000", "RP10000"]

# Read the damage values raster 
input_folder_path = "C:/Users/alexa/OneDrive/Desktop/SLEUTH/Hazard/New Outputs/2030_merged_new_damage/" # damage value layer
output_folder_path = "C:/Users/alexa/OneDrive/Desktop/SLEUTH/Hazard/New Outputs/2030_above50_new_damage/" # new output layer of damage = and above 50

for rp in return_periods:
    # Define input and output raster paths for the return periods
    input_raster_path = f"{input_folder_path}2030_new_damage_{rp}.tif"
    output_raster_path = f"{output_folder_path}2030_above50_new_damage_{rp}.tif"

    with rasterio.open(input_raster_path) as src:
        # Read the damage value raster data
        flood_depth_data = src.read(1)
        
        # Apply a mask to select only damage values above 50%
        # Threshold can be edited accordingly
        flood_depth_data[flood_depth_data <= 50] = 0

        # Get metadata for the new raster with damage values above threshold 
        metadata = src.meta.copy()
        metadata.update(dtype=rasterio.uint8)

        # Write the new damage percentage raster
        with rasterio.open(output_raster_path, 'w', **metadata) as dst:
            dst.write(flood_depth_data, 1)

print("Damage percentage rasters created successfully.")

