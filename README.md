# Dynamic Risk - Jakarta 

This is a code repository for the project:
Coastal flood risk analysis for Jakarta, Indonesia
URECA Project by Bernadette Chuah
July 2024


This risk analysis framework is done step by step. More detailed instructions are included in each Python code.

1. Combine_hazard_tiles.py (merging spatially different hazard tiles, 2 in this case)

   Input: Original Hazard folders (2)

   Output: Merged Hazard folder (1)
   
3. Assign_damage_to_flood_depths.py (assigning % damage values to corresponding flood depths in m)

   Input: Merged Hazard folder (1), Damage and flood depth values for the original and with policy curves (in an array, hard coding)

   Output: Merged damage folder (3)
   
5. Revised_dmg_curve_elevation.py (plotting damage-flood depth curve and adjusting it for policy of elevating building heights)

   Input: Damage and flood depth values in an array (2) 

   Output: Plots of curves (original, with policy, combined)
   
7. threshold_above_50.py (filtering pixels with significant damage; set a threshold)

   Input: Merged damage folder 

   Output: Threshold above 50 folder
   
9. part 5 of analysis (not a Python code, done in QGIS using raster calculator)

   Input: Threshold above 50 folder 

   Output: Urbanised, above 50 folder
   
11. assign_bc_to_urban_extent.py (assigns present day building count)

    Input: Building count raster (from Google Open Buildings) 

    Output: Building count folder
    
13. assign_bc_2018_2030.py (assigns values to future urban extent rasters)

    Input: Building count raster (assign values) 

    Output: Building count folder
   
*Change the file and folder paths accordingly!


Others:
final_buildingcount (google open buildings) with alignment.py (Converting coordinates from Google Open Buildings (in csv) to a building count raster. Firstly, run step 1 and step 2 when obtaining the CSV, and use 7-zip (Windows) or Keka (iOS) to extract compressed archive folder obtained from step 2) 
