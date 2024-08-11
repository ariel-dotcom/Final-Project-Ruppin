import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

# Define file paths for new data

# CHOOSE THE FILES TO WORK ON - SEA OR LAND
# sea files
new_files = {
    'north': {'lightnings': 'exel/north_above50k_Half_Map_lightnings.csv',
              'pollutants': 'exel/north_Half_Map_pollutants.csv'},
    'south': {'lightnings': 'exel/south_above50k_Half_Map_lightnings.csv',
              'pollutants': 'exel/south_Half_Map_pollutants.csv'}
}

# land files
new_files = {
    'center': {'lightnings': 'exel/center_lightnings.csv',
               'pollutants': 'exel/center_pollutants.csv'},
    'north': {'lightnings': 'exel/north_lightnings.csv',
              'pollutants': 'exel/north_pollutants.csv'},
    'south': {'lightnings': 'exel/south_lightnings.csv',
              'pollutants': 'exel/south_pollutants.csv'}
}


# Load all new data into dictionaries and count the number of rows
new_lightning_data = {}
new_pollution_data = {}
n_light = {}
n_poll = {}

for region, paths in new_files.items():
    new_lightning_data[region] = pd.read_csv(paths['lightnings'])
    new_pollution_data[region] = pd.read_csv(paths['pollutants'])

    # Count the number of rows in the original CSV files for pollutants
    n_poll[region] = len(new_pollution_data[region])

    # Process lightning data
    new_lightning_data[region]['DATE AND TIME'] = pd.to_datetime(new_lightning_data[region]['DATE AND TIME'],
                                                                 format='%Y%m%dT%H%M%S.%f')
    new_lightning_data[region]['Hour'] = new_lightning_data[region]['DATE AND TIME'].dt.hour
    new_lightning_data[region]['abs_peak_current'] = new_lightning_data[region]['peak current'].abs()

    # Count the number of rows after filtering
    n_light[region] = len(new_lightning_data[region])

    # Min-Max normalization
    min_peak = new_lightning_data[region]['abs_peak_current'].min()
    max_peak = new_lightning_data[region]['abs_peak_current'].max()
    new_lightning_data[region]['Min-Max'] = (new_lightning_data[region]['abs_peak_current'] - min_peak) / (
                max_peak - min_peak)

    # Aggregate the normalized values by hour
    new_lightning_data[region] = new_lightning_data[region].groupby('Hour')['Min-Max'].mean().reset_index()

    # Process pollution data
    new_pollution_data[region]['Date'] = pd.to_datetime(new_pollution_data[region]['Date'], errors='coerce')
    new_pollution_data[region] = new_pollution_data[region].dropna(subset=['Date'])
    new_pollution_data[region]['Hour'] = new_pollution_data[region]['Date'].dt.hour

    # Min-Max normalization for pollutants
    new_pollution_data[region]['Min-Max'] = new_pollution_data[region].groupby('pollutant')['Value'].transform(
        lambda x: (x - x.min()) / (x.max() - x.min())
    )

    # Aggregate the normalized values by hour
    new_pollution_data[region] = new_pollution_data[region].groupby(['Hour', 'pollutant'])[
        'Min-Max'].mean().reset_index()


# Function to calculate cross-region correlation between lightning and pollutants with an optional time shift
def calculate_cross_region_correlation(lightning_data, pollution_data, lightning_region, pollution_region, shift=0):
    correlation_results = {}
    lightning_df = lightning_data[lightning_region]
    pollution_df = pollution_data[pollution_region]

    for pollutant in pollution_df['pollutant'].unique():
        pollutant_data = pollution_df[pollution_df['pollutant'] == pollutant].copy()
        if shift != 0:
            pollutant_data['Hour'] = pollutant_data['Hour'] + shift
            pollutant_data = pollutant_data[(pollutant_data['Hour'] >= 0) & (pollutant_data['Hour'] < 24)]

        merged_data = pd.merge(lightning_df, pollutant_data, on='Hour', suffixes=('_lightning', '_pollution'))

        # Calculate Spearman correlation coefficient and P-value
        if not merged_data.empty:
            corr, p_value = spearmanr(merged_data['Min-Max_lightning'], merged_data['Min-Max_pollution'])
            n_samples = len(merged_data)
            r_squared = corr ** 2
            correlation_results[pollutant] = {'correlation': corr, 'p_value': p_value, 'n_samples': n_samples,
                                              'r_squared': r_squared}
    return correlation_results


# Function to calculate and store same-region and cross-region correlations with a specified shift
def calculate_all_correlations(shift=0):
    same_region_correlation_data = {}
    for region in new_files.keys():
        same_region_correlation_data[region] = calculate_cross_region_correlation(
            new_lightning_data, new_pollution_data, region, region, shift)

    cross_region_correlation_data = {}
    for lightning_region in new_files.keys():
        cross_region_correlation_data[lightning_region] = {}
        for pollution_region in new_files.keys():
            if lightning_region != pollution_region:
                cross_region_correlation_data[lightning_region][pollution_region] = calculate_cross_region_correlation(
                    new_lightning_data, new_pollution_data, lightning_region, pollution_region, shift)

    combined_correlation_data = {region: {**cross_region_correlation_data.get(region, {}),
                                          region: same_region_correlation_data.get(region, {})}
                                 for region in new_files.keys()}
    return combined_correlation_data


# Plot the significant correlations with time shift
def plot_combined_correlations_with_shift(combined_correlation_data, n_light, n_poll, shift=0):
    regions = list(combined_correlation_data.keys())
    pollutants = list(next(iter(combined_correlation_data.values())).values())[0].keys()
    num_plots = len(regions) * len(regions)

    fig, axes = plt.subplots(len(regions), len(regions), figsize=(15, 15), sharey=True)
    shift_text = f'{shift}-Hour Shift' if shift != 0 else 'No Shift'
    plt.suptitle(
        f'Same-Region and Cross-Region Correlations between Lightning and Pollutants ({shift_text})',
        fontsize= 10)

    for i, lightning_region in enumerate(regions):
        for j, pollution_region in enumerate(regions):
            ax = axes[i, j]
            correlations = combined_correlation_data[lightning_region].get(pollution_region, {})
            correlation_values = [correlations.get(pollutant, {}).get('correlation', 0) for pollutant in pollutants]
            p_values = [correlations.get(pollutant, {}).get('p_value', 1) for pollutant in pollutants]
            r_squared_values = [correlations.get(pollutant, {}).get('r_squared', 0) for pollutant in pollutants]
            n_samples_values = [correlations.get(pollutant, {}).get('n_samples', 0) for pollutant in pollutants]

            bar_colors = ['red' if p < 0.05 else 'skyblue' for p in p_values]
            bars = ax.bar(pollutants, correlation_values, color=bar_colors)

            for bar, corr, r_squared, p_val in zip(bars, correlation_values, r_squared_values, p_values):
                offset = 5
                ax.annotate(f'{corr:.2f}\nR²={r_squared:.2f}\nP={p_val:.3f}',
                            xy=(bar.get_x() + bar.get_width() / 2, 0),
                            xytext=(0, offset),
                            textcoords="offset points",
                            ha='center', va='bottom',
                            fontsize=14 )

            ax.set_title(f'{lightning_region.capitalize()} Lightning with {pollution_region.capitalize()} Pollutants\n'
                         f'N_light: {n_light[lightning_region]} N_poll: {n_poll[pollution_region]}',
                         fontsize=10)
            ax.set_xlabel('Pollutants', fontsize= 18)
            ax.set_ylabel('Correlation', fontsize= 18)
            ax.set_ylim(-1, 1)
            ax.axhline(0, color='black', linewidth=0.8)
            ax.grid(True)

            # Adjust x-axis and y-axis tick label fonts
            ax.tick_params(axis='x', labelsize=13)  # X-axis tick label font size
            ax.tick_params(axis='y', labelsize=13)  # Y-axis tick label font size
            # Ensure all y-ticks are visible even when shared
            if j > 0:
                ax.tick_params(labelleft=True)  # Force left labels to show

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


# Calculate correlations with desired shift
combined_correlation_data = calculate_all_correlations(shift=0)

# Plot the correlations
plot_combined_correlations_with_shift(combined_correlation_data, n_light, n_poll, shift=0)

# Calculate correlations with desired shift
combined_correlation_data = calculate_all_correlations(shift=1)

# Plot the correlations
plot_combined_correlations_with_shift(combined_correlation_data, n_light, n_poll, shift=1)

# Calculate correlations with desired shift
combined_correlation_data = calculate_all_correlations(shift=2)

# Plot the correlations
plot_combined_correlations_with_shift(combined_correlation_data, n_light, n_poll, shift=2)


