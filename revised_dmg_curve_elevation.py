# -*- coding: utf-8 -*-
"""
@author: bern
plotting the shifted flood damage curve (shifts to the right) which is the damage curve 
if policy gets enacted

part 3 of analysis (used for newer buildings built from 2020 to 2030, 
                    because older buildings are less likely to undergo policy)

"""
import matplotlib.pyplot as plt
import numpy as np

# Original data
# Flood depth values are in meters (converted from ft)
# Damage percentage values are in %
# New damage percentage values are placed for observation (no added purpose to plot)
flood_depth = np.array([0, 0.3048, 0.6096, 0.9144, 1.2192, 1.524, 1.8288, 2.1336, 2.4384, 2.7432, 3.048, 3.3528, 3.6576, 3.9624, 4.2672, 4.572, 4.8768, 5.1816, 5.4864, 5.7912, 6.096, 6.4008, 6.7056, 7.0104, 7.3152])
damage_percentage = np.array([0, 45, 57, 70, 75, 79, 80, 83, 83, 83, 83, 91, 94, 98, 98, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99])
new_damage_percentage = np.array([0, 0, 23.56, 51,28, 63.81, 72.62, 77.09, 79.52, 81.57, 83, 83, 83, 87.19, 92.57, 96.09, 98, 98.52, 99, 99, 99, 99, 99, 99, 99, 99])

# Shift amount to fit the elevation level people should raise new buildings
shift_amount = 0.45  # shift the curve to the right by 0.45 meters

# Adjusted flood depth values for interpolation
adjusted_flood_depth = flood_depth + shift_amount

# Interpolated new damage values for the original flood depths based on the shifted curve
new_damage_values = np.interp(flood_depth, adjusted_flood_depth, damage_percentage)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(flood_depth, damage_percentage, label='2-Storey residential building', marker='x', linestyle='--')
plt.plot(flood_depth, new_damage_values, label='2-Storey residential building elevated by 0.45m', marker='o', linestyle='-')

plt.xlabel('Flood Depth (m)')
plt.ylabel('Damage Percentage (%)')
plt.title('Depth-Damage Curve for a 2-Storey residential building in Jakarta')
plt.legend()
plt.grid(True)
plt.show()

# Print the new damage values
print("Revised Damage Values for the original flood depths:")
for depth, damage in zip(flood_depth, new_damage_values):
    print(f"Flood Depth: {depth:.2f} m, Damage Percentage: {damage:.2f} %")

