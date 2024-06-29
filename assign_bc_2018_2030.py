# -*- coding: utf-8 -*-
"""
@author: bern
part 7 of analysis
1. calculate average building number per pixel 
2. assigning average building count level of 5 for projected urban growth in 2030
based on assumption of 5 buildings per pixel

input: 
        1. rasters obtained from QGIS raster calculator in part 5
        (coastal flooding rasters that intersect with significantly damaged buildings, in urbanised areas)
        2. building count (obtained from Google Open Buildings) 
    
output: building count per pixel for the urban development from 2018 to 2030. 
    
"""
import rasterio
import numpy as np

# Path to the raster file
# Finding out the average building count in Jakarta currently 
raster_path = "C:/Users/alexa/OneDrive/Desktop/SLEUTH/Input/Aligned_Building_Count2.tif"

# Open the raster file
with rasterio.open(raster_path) as src:
    # Read the raster data
    data = src.read(1)

    # Remove NaN values and values equal to 0
    data_clean = data[np.isfinite(data) & (data != 0)]

    # Calculate the average value of the remaining pixels
    if data_clean.size > 0:
        average_value = np.mean(data_clean)
    else:
        average_value = np.nan

print(f"The average value of the pixels (excluding NaN and 0) is: {average_value}")

"""
assigning value of 5 to the urban extents
for the urban rasters between 2018 and 2030

"""
import rasterio
import numpy as np

# List of return periods
# Edit according to naming
return_periods = [1, 2, 5, 10, 25, 50, 100, 250, 500, 1000, 2000, 10000]

# Loop through each return period
for rp in return_periods:
    # Path to the input raster(from QGIS Raster Calculator)
    input_raster_path = f"C:/Users/alexa/OneDrive/Desktop/SLEUTH/Hazard/New Outputs/testing using qgis raster calc/2030_new_dmg/2030_new_urb_rp{rp}.tif"
    # Path to the output raster (building count at the urban development from 2018 to 2030)
    output_raster_path = f"C:/Users/alexa/OneDrive/Desktop/SLEUTH/Hazard/New Outputs/building counts/2030 (new dmg)/2030_new_urbanised_rp{rp}_processed.tif"

    # Open the input raster
    with rasterio.open(input_raster_path) as src:
        # Read the raster data
        data = src.read(1)

        # Apply the condition: if the value is greater than 0, assign it a value of 5
        # Urban areas get assigned 5 buildings per pixel 
        data[data > 0] = 5

        # Count the total number of non-zero pixels and their sum
        # Using the number of non-zero pixels, we can calculate the built-up areas
        # The total value of pixels gives us the total number of buildings 
        non_zero_pixels = np.count_nonzero(data)
        total_value = np.sum(data[data > 0])  # Only summing the non-zero pixels

        # Get metadata from the input raster
        profile = src.profile

        # Save the modified raster
        with rasterio.open(output_raster_path, 'w', **profile) as dst:
            dst.write(data, 1)

        print(f"Processed raster for return period {rp} saved successfully.")
        print(f"Return period {rp}:")
        print(f"  - Non-zero pixels count: {non_zero_pixels}")
        print(f"  - Total value of pixels: {total_value}")

print("All rasters processed and saved successfully.")
