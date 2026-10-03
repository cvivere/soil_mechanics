import numpy as np
import matplotlib.pyplot as plt


# determine which soil each location in depths is in
gamma_w = 9.81 # kN/m3

def soil_at(z, soil_profile):
    ''' Helper function to determine where in the soil profile a location at depth z is at'''
    for name, (top, bottom) in soil_profile.items():
        if top <= z <= bottom:
            return name

# Divide into sublayers
sublayers = [ # (top, bottom, gamma in kN/m3)
    (0, 5, 17), # sand above WT
    (5, 7, 19) , # sand below WT
    (7, 12, 19)  # silt below WT
]


# Calculate effective stress at each depth

def vertical_stress(z):
    ''' Calculate the vertical stress at depth z in kPa'''
    sigma = 0
    for top, bottom, gamma in sublayers:
        thickness = max(0, min(bottom, z) - top)
        sigma += gamma * thickness
    return sigma

def pore_pressure(z, water_table):
    ''' Calculate pore pressure at depth z in kPa'''
    return gamma_w * max(0, z - water_table)


def effective_stress(z, water_table):
    return vertical_stress(z) - pore_pressure(z, water_table)

def effective_horizontal(z, k0, water_table):
    return k0*effective_stress(z, water_table)

def horizontal_stress(z, water_table, k0):
    u = pore_pressure(z, water_table)
    return effective_horizontal(z, k0, water_table) + u

def plot_stresses(depths, water_table, k0):
    print("Plotting stresses...")
    z = list(depths.values())

    quantities = [
        ([vertical_stress(d) for d in z],                        'σv'),
        ([pore_pressure(d, water_table) for d in z],             'u'),
        ([effective_stress(d, water_table) for d in z],          "σ'v"),
        ([effective_horizontal(d, k0, water_table) for d in z],  "σ'h"),
        ([horizontal_stress(d, water_table, k0) for d in z],     'σh'),
    ]

    fig, axes = plt.subplots(1, 5, sharey=True, figsize=(14, 5))

    for ax, (values, label) in zip(axes, quantities):
        ax.plot(values, z, marker='o')
        ax.set_title(label)
        ax.set_xlabel('kPa')
        ax.axhline(water_table, linestyle='--', color='gray')
        ax.grid(True)

    axes[0].set_ylabel('Depth (m)')
    axes[0].invert_yaxis()
    fig.tight_layout()
    plt.show()



def main(depths, k0, water_table):

        print(f"{'Pt':<4}{'z (m)':>6}{'σ (kPa)':>10}{'u (kPa)':>10}{'σ\' (kPa)':>11}{'σ\'h (kPa)':>11}{'σh (kPa)':>10}")
        for location, z in depths.items():
            print(f"{location:<4}{z:>6}{vertical_stress(z):>10.2f}"
                f"{pore_pressure(z, water_table):>10.2f}{effective_stress(z, water_table):>11.2f}"
                f"{effective_horizontal(z, k0, water_table):>11.2f}{horizontal_stress(z, water_table, k0):>10.2f}")

        plot_stresses(depths, water_table, k0)


    
if __name__ == "__main__":
    depths = {'A': 0,'B': 5, 'C': 7, 'D': 12} # depths in meters
    k0 = 0.5 # coefficient of lateral earth pressure
    water_table = 5 # depth of water table in meters
    main(depths, k0, water_table)
