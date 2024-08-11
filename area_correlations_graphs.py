import pandas as pd
import matplotlib.pyplot as plt

def load_and_prepare_data(lightning_file, pollutant_file):
    # Load the CSV files
    lightnings_df = pd.read_csv(lightning_file)
    pollutants_df = pd.read_csv(pollutant_file)

    # Convert the date columns to datetime format
    lightnings_df['DATE AND TIME'] = pd.to_datetime(lightnings_df['DATE AND TIME'], format='%Y%m%dT%H%M%S.%f')
    pollutants_df['Date'] = pd.to_datetime(pollutants_df['Date'])

    # Round the timestamps to the nearest hour for merging
    lightnings_df['DATE AND TIME'] = lightnings_df['DATE AND TIME'].dt.round('h')
    pollutants_df['Date'] = pollutants_df['Date'].dt.round('h')

    # Merge the dataframes on the rounded date columns
    merged_df = pd.merge_asof(
        lightnings_df.sort_values('DATE AND TIME'),
        pollutants_df.sort_values('Date'),
        left_on='DATE AND TIME',
        right_on='Date',
        direction='nearest',
        tolerance=pd.Timedelta('1h')
    )

    return merged_df

def plot_data(merged_df, region_label, pollutant_mean_data):
    # Convert date and time to just the hour for grouping
    merged_df['Hour'] = merged_df['DATE AND TIME'].dt.hour
    merged_df['abs_peak_current'] = merged_df['peak current'].abs()  # Calculate the absolute peak current

    # Calculate the mean absolute peak current by hour
    mean_lightning_data = merged_df.groupby('Hour')['abs_peak_current'].mean()

    fig, ax1 = plt.subplots(figsize=(14, 7))

    ax1.set_xlabel('Hour of the Day')
    ax1.set_ylabel('Mean Absolute Peak Current', color='tab:red')
    ax1.plot(mean_lightning_data.index, mean_lightning_data, color='tab:red', label='Mean Absolute Peak Current')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Mean Pollutant Value', color='tab:blue')
    ax2.plot(pollutant_mean_data.index, pollutant_mean_data['Value'], color='tab:blue', label='Mean Pollutant Value')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    plt.title(f'Mean Absolute Lightning Peak Current vs Pollutant Value by Hour in {region_label}')
    fig.tight_layout()

    # Ensure x-axis covers all 24 hours
    ax1.set_xticks(range(24))

    # Save the plot as an image file
    filename = fr'graphs\above50k\{region_label}.png'.replace(' ', '_')
    plt.savefig(filename)

    plt.close(fig)  # Close the figure to free up memory

# File paths for all regions
# Exclude center when working on sea
files = {
    #'center': {'lightnings': r'exel\center_lightnings.csv', 'pollutants': r'exel\center_pollutants.csv'},
    'north': {'lightnings': r'exel\north_above50k_Half_Map_lightnings.csv', 'pollutants': r'exel\north_Half_Map_pollutants.csv'},
    'south': {'lightnings': r'exel\south_above50k_Half_Map_lightnings.csv', 'pollutants': r'exel\south_Half_Map_pollutants.csv'}
}

# Generate mean pollutant data for each region and pollutant
pollutant_means = {}
for region, fileset in files.items():
    pollutants_df = pd.read_csv(fileset['pollutants'])
    pollutants_df['Date'] = pd.to_datetime(pollutants_df['Date']).dt.round('h')
    pollutants_df['Hour'] = pollutants_df['Date'].dt.hour
    for pollutant in pollutants_df['pollutant'].unique():
        pollutant_data = pollutants_df[pollutants_df['pollutant'] == pollutant]
        mean_pollutant_data = pollutant_data.groupby('Hour').mean(numeric_only=True)
        pollutant_means[f"{region}_{pollutant}"] = mean_pollutant_data

# Generate all combinations of lightning and pollutant data
for lightning_region, lightning_files in files.items():
    for pollutant_region, pollutant_files in files.items():
        for pollutant in pd.read_csv(pollutant_files['pollutants'])['pollutant'].unique():
            # Merge and plot data for all region combinations, including the same regions
            merged_data = load_and_prepare_data(lightning_files['lightnings'], pollutant_files['pollutants'])
            mean_pollutant_data = pollutant_means[f"{pollutant_region}_{pollutant}"]
            plot_data(merged_data, f'{lightning_region.capitalize()} Lightnings with {pollutant_region.capitalize()} {pollutant}', mean_pollutant_data)
