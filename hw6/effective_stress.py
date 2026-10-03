import numpy as np
import matplotlib.pyplot as plt


depths = {'A': 0,'B': 5, 'C': 7, 'D': 12} # depths in meters

sand = {'gamma_t': 17,
        'gamma_sat': 19}
silt = {'gamma_sat': 19}

soil_profile = {'sand': (0, 7),
                'silt': (7, 12)}

water_table = 5

# determine which soil each location in depths is in


def soil_at(z):
    ''' Helper function to determine where in the soil profile a location at depth z is at'''
    for name, (top, bottom) in soil_profile.items():
        if top <= z <= bottom:
            return name

# Test
{pt: soil_at(z) for pt, z in depths.items()}

# Divide into sublayers
sublayers = [ # (top, bottom, unit weight in kN/m3)
    (0, 5, 17), # sand above WT
    (5, 7, 19) , # sand below WT
]