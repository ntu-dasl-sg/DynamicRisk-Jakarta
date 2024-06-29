# -*- coding: utf-8 -*-
"""
@author: bern

assigning damage values based on original damage curve and policy damage curve.
depending on the building type in the area, first select an appropriate damage-flood depth curve
the values here are obtained from FEMA HAZUS. 

change input and output folder paths accordingly
edit return periods accordingly

part 2 of analysis. assign damage values for the merged flood hazard files. 

"""
import rasterio
import numpy as np

# Flood depth values and corresponding damage percentages in an array
# Hard coding
flood_depth_values = np.array([0, 0.3048, 0.6096, 0.9144, 1.2192, 1.524, 1.8288, 2.1336, 2.4384, 2.7432, 3.048, 3.3528, 3.6576, 3.9624, 4.2672, 4.572, 4.8768, 5.1816, 5.4864, 5.7912, 6.096, 6.4008, 6.7056, 7.0104, 7.3152])
new_damage_percentages = np.array([0, 0, 23.56, 51.28, 63.81, 72.62, 77.09, 79.52, 81.57, 83, 83, 83, 87.19, 92.57, 96.09, 98, 98.52, 99, 99, 99, 99, 99, 99, 99, 99])

# Function to map depth to damage using interpolation
def map_depth_to_damage(depth):
    return np.interp(depth, flood_depth_values, new_damage_percentages)

# List of return periods
# Edit according to naming 
return_periods = ["RP1", "RP2", "RP5", "RP10", "RP25", "RP50", "RP100", "RP250", "RP500", "RP1000", "RP2000", "RP10000"]

# Paths for input and output rasters
# Input: folder for merged flood tiles from part 1 with flood depth values
# Output: folder for merged flood tiles with corresponding damage values
input_folder_path = "C:/Users/alexa/OneDrive/Desktop/SLEUTH/Hazard/New Outputs/2030_merged_flood_hazard/"
output_folder_path = "C:/Users/alexa/OneDrive/Desktop/SLEUTH/Hazard/New Outputs/2030_merged_new_damage/"

for rp in return_periods:
    # Define input and output raster paths for the return periods
    input_raster_path = f"{input_folder_path}merged_{rp}.tif"
    output_raster_path = f"{output_folder_path}2030_new_damage_{rp}.tif"

    # Read the merged flood depth raster (from part 1)
    with rasterio.open(input_raster_path) as src:
        # Read the source raster data
        flood_depth_data = src.read(1)
        
        # Map each flood depth value to a damage percentage
        damage_data = map_depth_to_damage(flood_depth_data).astype(np.uint8)

        # Get metadata for the new raster
        metadata = src.meta.copy()
        metadata.update(dtype=rasterio.uint8)

        # Write the new damage percentage raster
        with rasterio.open(output_raster_path, 'w', **metadata) as dst:
            dst.write(damage_data, 1)

    print(f"Damage percentage raster created successfully for return period {rp} at:", output_raster_path)
