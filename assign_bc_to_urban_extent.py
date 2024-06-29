# -*- coding: utf-8 -*-
"""
@author: bern
part 6 of analysis 
input: 1. rasters obtained from QGIS raster calculator in part 5
        (coastal flooding rasters that intersect with significantly damaged buildings, in urbanised areas)
       2. building count (obtained from Google Open Buildings) 
        
output: building count per pixel for the year 2020 (present)

intersection of building count layer and coastal flooding model layers for different return periods
building count layer has been generated as Aligned_Building_Count2

count number of overlapping pixels (for area)
count values of the overlapping pixels (for number of buildings exposed to coastal flooding)

"""
import rasterio
from rasterio.features import shapes
from rasterio.mask import mask
import numpy as np

# List of return periods
# Edit according to naming 
return_periods = [1, 2, 5, 10, 25, 50, 100, 250, 500, 1000, 2000, 10000]

# Path to the second raster (building count layer)
second_raster_path = "C:/Users/alexa/OneDrive/Desktop/SLEUTH/Input/Aligned_Building_Count2.tif"

# Loop through each return period (rasters from QGIS raster calculator in part 5)
for rp in return_periods:
    # Paths to the first raster and output raster
    first_raster_path = f"C:/Users/alexa/OneDrive/Desktop/SLEUTH/Hazard/New Outputs/testing using qgis raster calc/2020_urbanised_rp{rp}.tif"
    output_raster_path = f"C:/Users/alexa/OneDrive/Desktop/SLEUTH/Hazard/New Outputs/building counts/2020_rp{rp}.tif"
    
    # Open the first raster
    with rasterio.open(first_raster_path) as first_src:
        # Read the raster data
        first_data = first_src.read(1)

        # Create a mask for non-zero values
        mask_array = first_data > 0

        # Convert the mask array to shapes (polygons)
        shapes_gen = shapes(mask_array.astype(np.int16), mask=mask_array, transform=first_src.transform)
        geoms = [shape for shape, value in shapes_gen if value == 1]

        # If no geometries are found, skip to the next iteration
        if not geoms:
            print(f"No non-zero areas found for return period {rp}. Skipping.")
            continue

        # Open the second raster
        with rasterio.open(second_raster_path) as second_src:
            # Extract the values from the second raster based on the mask polygons
            out_image, out_transform = mask(second_src, geoms, crop=True, nodata=0)

            # Get metadata from the second raster
            out_meta = second_src.meta.copy()

            # Update the metadata to reflect the new shape and transform
            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform
            })

            # Write the extracted values to the output raster
            with rasterio.open(output_raster_path, "w", **out_meta) as dest:
                dest.write(out_image)

            # Count the total number of non-zero pixels and their sum
            # Using the number of non-zero pixels, we can calculate the built-up areas
            # The total value of pixels gives us the total number of buildings 
            non_zero_pixels = np.count_nonzero(out_image)
            total_value = np.sum(out_image)

            print(f"Return period {rp}:")
            print(f"  - Non-zero pixels count: {non_zero_pixels}")
            print(f"  - Total value of pixels: {total_value}")

print("All extractions completed successfully.")

