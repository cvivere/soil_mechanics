import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# determine which soil each location in depths is in
gamma_w = 9.81 # kN/m3



# Calculate effective stress at each depth

def vertical_stress(z, sublayers):
    ''' Calculate the vertical stress at depth z in kPa'''
    sigma = 0
    for top, bottom, gamma in sublayers:
        thickness = max(0, min(bottom, z) - top)
        sigma += gamma * thickness
    return sigma

def pore_pressure(z, water_table):
    ''' Calculate pore pressure at depth z in kPa'''
    return gamma_w * max(0, z - water_table)


def effective_stress(z, water_table, sublayers):
    return vertical_stress(z, sublayers) - pore_pressure(z, water_table)

def effective_horizontal(z, k0, water_table, sublayers):
    return k0*effective_stress(z, water_table, sublayers)

def horizontal_stress(z, water_table, k0, sublayers):
    u = pore_pressure(z, water_table)
    return effective_horizontal(z, k0, water_table, sublayers) + u


def plot_stresses_plain(depths, water_table, k0):
    ''' Simple plot for submitting hw. '''
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
    plt.show())

def plot_stresses(depths, water_table, k0, sublayers, soils):
    '''Plot for writeup. Displays water table and soil layers, including shading. '''
    z = list(depths.values())

    quantities = [
        ([vertical_stress(d, sublayers) for d in z],                        'σv'),
        ([pore_pressure(d, water_table) for d in z],                        'u'),
        ([effective_stress(d, water_table, sublayers) for d in z],          "σ'v"),
        ([effective_horizontal(d, k0, water_table, sublayers) for d in z],  "σ'h"),
        ([horizontal_stress(d, water_table, k0, sublayers) for d in z],     'σh'),
    ]

    fig, axes = plt.subplots(1, 5, sharey=True, figsize=(14, 5))

    for ax, (values, label) in zip(axes, quantities):
        # soil layer bands
        for name, top, bottom, color in soils:
            ax.axhspan(top, bottom, color=color, alpha=0.25, zorder=0)
        # layer boundaries (skip the ground surface)
        for _, top, _, _ in soils[1:]:
            ax.axhline(top, color='black', linewidth=0.8, zorder=1)
        # water table
        ax.axhline(water_table, linestyle='--', color='tab:blue', linewidth=1.2, zorder=1)

        ax.plot(values, z, marker='o', color='black', zorder=2)
        ax.set_title(label)
        ax.set_xlabel('kPa')
        ax.grid(True, alpha=0.3)

    # label layers and water table on the first panel only
    for name, top, bottom, _ in soils:
        axes[0].text(0.97, (top + bottom) / 2, name, transform=axes[0].get_yaxis_transform(),
                     ha='right', va='center', fontsize=9, style='italic')
    axes[0].text(0.03, water_table, '▽ WT', transform=axes[0].get_yaxis_transform(),
                 ha='left', va='bottom', color='tab:blue', fontsize=9)

    axes[0].set_ylabel('Depth (m)')
    axes[0].set_ylim(soils[-1][2], 0)  # puts ground surface at top
    fig.tight_layout()
    return fig

def main(depths, k0, water_table, sublayers, soils, save_plot=False, filename='stresses_plot.png'):

    print(f"{'Pt':<4}{'z (m)':>6}{'σ (kPa)':>10}{'u (kPa)':>10}{'σ\' (kPa)':>11}{'σ\'h (kPa)':>11}{'σh (kPa)':>10}")
    for location, z in depths.items():
        print(f"{location:<4}{z:>6}{vertical_stress(z, sublayers):>10.2f}"
              f"{pore_pressure(z, water_table):>10.2f}{effective_stress(z, water_table, sublayers):>11.2f}"
              f"{effective_horizontal(z, k0, water_table, sublayers):>11.2f}{horizontal_stress(z, water_table, k0, sublayers):>10.2f}")

    fig = plot_stresses(depths, water_table, k0, sublayers, soils)

    if save_plot:
        out_dir = Path('figures')
        out_dir.mkdir(exist_ok=True)
        fig.savefig(out_dir / filename, dpi=200, bbox_inches='tight')

    plt.show()


    
if __name__ == "__main__":
    depths = {'A': 0,'B': 5, 'C': 7, 'D': 12} # depths in meters
    k0 = 0.5 # coefficient of lateral earth pressure
    water_table = 5 # depth of water table in meters
    sublayers = [
        (0, 5, 17),
        (5, 7, 19),
        (7, 12, 19)
    ]
    soils = [  # (name, top, bottom, color) for shading
    ('Sand', 0, 7, 'tan'),
    ('Silt', 7, 12, 'lightgray')]

    main(depths, k0, water_table, sublayers, soils, save_plot=True, filename='problem1_stresses.png')
