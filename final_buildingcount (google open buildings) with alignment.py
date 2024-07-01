 # -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 17:13:58 2024

@author: bern
Get building count from all the individual points and then make my own building count layer (data obtained is from Google Open Buildings).
The CSV file contains coordinates of different buildings. By syncing through the different buildings and categorizing them into 30m x 30m pixels,
each pixel will have the number of buildings in that area.

Input file( obtained from Google Open Buildings (https://sites.research.google/open-buildings/)) 
    World Bank (High Res 10m)
    Select Region
    Select Points
    Use the generated csv file
    Remove the other columns, you just need longitude and latitude columns
    
For alignment (in later part of this code):
Input file: one merged flood return period
    
Output file (TIF of building count for 30m by 30m pixel) that is aligned to projection of CRS EPSG:4326 - WGS 84

Change the input and output file paths in this code

"""

import pandas as pd
import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.warp import calculate_default_transform, reproject, Resampling
import logging
from tqdm import tqdm

# Setup logging
# helps log the process steps and with debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the CSV file obtained from Google Open Buildings
# Edit the csv input path accordingly
csv_path = "C:/Users/alexa/OneDrive/Desktop/SLEUTH/Input/open_buildings_v3_points_your_own_wkt_polygon 3.csv"
df = pd.read_csv(csv_path)

# Print column names to debug
logger.info("Column names in the CSV file: %s", df.columns)

# Adjust these column names as per your CSV file
longitudes = df['longitude'].values
latitudes = df['latitude'].values

# Define the raster resolution
# Can adjust based on resolution 
pixel_size = 0.0003  # Approximately 30m x 30m pixels (in decimal degrees)

# Determine the extent of the raster (min and max longitude and latitudes)
lon_min, lon_max = np.nanmin(longitudes), np.nanmax(longitudes)
lat_min, lat_max = np.nanmin(latitudes), np.nanmax(latitudes)

# Log extent values
logger.info("Extent of raster - lon_min: %f, lon_max: %f, lat_min: %f, lat_max: %f", lon_min, lon_max, lat_min, lat_max)

# Calculate the number of pixels in x and y directions
x_pixels = int((lon_max - lon_min) / pixel_size) + 1
y_pixels = int((lat_max - lat_min) / pixel_size) + 1

# Log number of pixels
logger.info("Number of pixels - x_pixels: %d, y_pixels: %d", x_pixels, y_pixels)

# Create an empty array for the raster
raster = np.zeros((y_pixels, x_pixels), dtype=np.uint32)

# Define the transform for the raster
# from_origin shows a georeferenced corner (west, north, x pixel size, y pixel size)
transform = from_origin(lon_min, lat_max, pixel_size, pixel_size)

# Populate the raster with counts of points in each pixel
# enumerate provides an index i along with each pair
# tqdm provides a progress bar to show how many points it has been
for i, (lon, lat) in enumerate(tqdm(zip(longitudes, latitudes), total=len(longitudes))):
    col = int((lon - lon_min) / pixel_size)
    row = int((lat_max - lat) / pixel_size)
    raster[row, col] += 1
    if i % 100 == 0:
        logger.info("Processed %d/%d points", i, len(longitudes))

# Align the new raster with other layers 

# Path to the reference raster for alignment
# Selected one of the return periods (from the coastal flooding model) for reference
# Change the path
reference_raster_path = 'C:/Users/alexa/OneDrive/Desktop/SLEUTH/Hazard/New Outputs/2020_merged_flood_hazard/merged_RP1.tif'

# Read the reference raster to get the target CRS, transform, and shape
with rasterio.open(reference_raster_path) as ref:
    target_crs = ref.crs
    target_transform = ref.transform
    target_width = ref.width
    target_height = ref.height

# Reproject the output raster to align with the reference raster
# This is the path for the final aligned building count
aligned_raster_path = 'C:/Users/alexa/OneDrive/Desktop/SLEUTH/Hazard/New Outputs/building counts/Aligned_Building_Count.tif'

# Create an empty array for the aligned raster
aligned_raster = np.zeros((target_height, target_width), dtype=np.uint32)

# Reproject the raster
reproject(
    source=raster,
    destination=aligned_raster,
    src_transform=transform,
    src_crs='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs',
    dst_transform=target_transform,
    dst_crs=target_crs,
    resampling=Resampling.nearest
)

# Save the aligned raster to a file
with rasterio.open(
    aligned_raster_path,
    'w',
    driver='GTiff',
    height=aligned_raster.shape[0],
    width=aligned_raster.shape[1],
    count=1,
    dtype=aligned_raster.dtype,
    crs=target_crs,
    transform=target_transform,
) as dst:
    dst.write(aligned_raster, 1)

logger.info("Aligned raster saved as %s", aligned_raster_path)