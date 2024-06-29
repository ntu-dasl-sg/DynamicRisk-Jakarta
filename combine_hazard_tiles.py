# -*- coding: utf-8 -*-
"""
@author: bern

over here i am merging the 2 hazard coastal flooding tiles according to 
the same year and return period (2020 and 2030) first. 

place all the tiles in the same year in a folder. e.g. for 2020, i will have
all of the return periods in that year present. 

change paths for input (2 in this case) and output folder
edit naming and number of return periods if needed

part 1 of analysis. 
"""
import os
import rasterio
from rasterio.merge import merge

# List of folders containing the rasters for different return periods
# Change paths based on years (these paths are the flood hazard tiles)
# These are 2 different folders for the same year, just spatially different
# Changed for 2020 and 2030
folder_path_1 = "C:/Users/alexa/OneDrive/Desktop/SLEUTH/Hazard/Y2030/N06E106_RCP85_2030/"
folder_path_2 = "C:/Users/alexa/OneDrive/Desktop/SLEUTH/Hazard/Y2030/N06E107_RCP85_2030/"

# List of return periods
# Edit according to naming 
return_periods = ["RP1", "RP2", "RP5", "RP10", "RP25", "RP50", "RP100", "RP250", "RP500", "RP1000", "RP2000", "RP10000"]

# Function to generate input raster paths for the 2 folder paths above and their correspondning return periods
def generate_input_raster_paths(folder_path_1, folder_path_2, return_periods):
    input_raster_paths = []
    for rp in return_periods:
        rp_path_1 = os.path.join(folder_path_1, f"{rp}.tif")
        rp_path_2 = os.path.join(folder_path_2, f"{rp}.tif")
        if os.path.exists(rp_path_1) and os.path.exists(rp_path_2):
            input_raster_paths.append((rp_path_1, rp_path_2))
        else:
            print(f"Raster not found for return period {rp} in one of the folders.")
    return input_raster_paths

# Generate input raster paths
input_raster_paths = generate_input_raster_paths(folder_path_1, folder_path_2, return_periods)

# Read and merge the input rasters
for rp_path_1, rp_path_2 in input_raster_paths:
    src_files_to_mosaic = []
    for rp_path in [rp_path_1, rp_path_2]:
        src = rasterio.open(rp_path)
        src_files_to_mosaic.append(src)
    
    # Merge the input rasters
    mosaic, out_trans = merge(src_files_to_mosaic)

    # Get metadata from the first input return period raster
    out_meta = src_files_to_mosaic[0].meta.copy()

    # Update metadata with the new dimensions and transform
    out_meta.update({"driver": "GTiff",
                      "height": mosaic.shape[1],
                      "width": mosaic.shape[2],
                      "transform": out_trans})

    # Extract the return period from the input raster path
    rp = os.path.basename(rp_path_1).split(".")[0]
    
    # Output path for the merged raster
    output_raster_path = f"C:/Users/alexa/OneDrive/Desktop/SLEUTH/Hazard/New Outputs/merged_{rp}.tif"

    # Write the merged raster to a new file
    with rasterio.open(output_raster_path, "w", **out_meta) as dest:
        dest.write(mosaic)
    
    print(f"Merged raster for return period {rp} created successfully at:", output_raster_path)
