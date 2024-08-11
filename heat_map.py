import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

# Define file paths for new data

# CHOOSE THE FILES TO WORK ON - SEA OR LAND
# land files
new_files = {
    'center': {'lightnings': 'exel/center_lightnings.csv',
               'pollutants': 'exel/center_pollutants.csv'},
    'north': {'lightnings': 'exel/north_lightnings.csv',
              'pollutants': 'exel/north_pollutants.csv'},
    'south': {'lightnings': 'exel/south_lightnings.csv',
              'pollutants': 'exel/south_pollutants.csv'}
}

# sea files
#new_files = {
#    'north': {'lightnings': 'exel/north_above50k_Half_Map_lightnings.csv',
#              'pollutants': 'exel/north_Half_Map_pollutants.csv'},
#    'south': {'lightnings': 'exel/south_above50k_Half_Map_lightnings.csv',
#              'pollutants': 'exel/south_Half_Map_pollutants.csv'}
#}



# Load all new data into dictionaries
new_lightning_data = {}
new_pollution_data = {}

for region, paths in new_files.items():
    new_lightning_data[region] = pd.read_csv(paths['lightnings'])
    new_pollution_data[region] = pd.read_csv(paths['pollutants'])


# Function to preprocess lightning data
def preprocess_lightning_data(df, region):
    df['DATE AND TIME'] = pd.to_datetime(df['DATE AND TIME'], format='%Y%m%dT%H%M%S.%f')
    df['Hour'] = df['DATE AND TIME'].dt.hour
    df['abs_peak_current'] = df['peak current'].abs()

    # Min-Max normalization
    min_peak = df['abs_peak_current'].min()
    max_peak = df['abs_peak_current'].max()
    df['Min-Max'] = (df['abs_peak_current'] - min_peak) / (max_peak - min_peak)

    # Aggregate the normalized values by hour
    df = df.groupby('Hour')['Min-Max'].mean().reset_index()
    df['Region'] = region
    return df


# Function to preprocess pollution data
def preprocess_pollution_data(df, region):
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df['Hour'] = df['Date'].dt.hour

    # Min-Max normalization for pollutants
    df['Min-Max'] = df.groupby('pollutant')['Value'].transform(lambda x: (x - x.min()) / (x.max() - x.min()))

    # Aggregate the normalized values by hour
    df = df.groupby(['Hour', 'pollutant'])['Min-Max'].mean().reset_index()
    df['Region'] = region
    return df


# Preprocess all data

# DELETE center_lightnings IF USING SEA FILES
center_lightnings = preprocess_lightning_data(new_lightning_data['center'], 'center')
center_pollutants = preprocess_pollution_data(new_pollution_data['center'], 'center')

north_lightnings = preprocess_lightning_data(new_lightning_data['north'], 'north')
north_pollutants = preprocess_pollution_data(new_pollution_data['north'], 'north')

south_lightnings = preprocess_lightning_data(new_lightning_data['south'], 'south')
south_pollutants = preprocess_pollution_data(new_pollution_data['south'], 'south')


# Function to calculate cross-region correlations
def calculate_cross_region_correlations(lightning_data, pollution_data):
    correlation_results = {}

    for lightning_region in lightning_data['Region'].unique():
        correlation_results[lightning_region] = {}
        for pollution_region in pollution_data['Region'].unique():
            for pollutant in pollution_data['pollutant'].unique():
                lightnings = lightning_data[lightning_data['Region'] == lightning_region]['Min-Max']
                pollutants = pollution_data[
                    (pollution_data['Region'] == pollution_region) & (pollution_data['pollutant'] == pollutant)][
                    'Min-Max']

                if len(lightnings) == len(pollutants) and len(lightnings) > 0:
                    corr, _ = spearmanr(lightnings, pollutants)
                    correlation_results[lightning_region][f'{pollution_region} {pollutant}'] = corr
                else:
                    correlation_results[lightning_region][f'{pollution_region} {pollutant}'] = np.nan

    return pd.DataFrame(correlation_results)


# Calculate cross-region correlations
# DELETE center_lightnings IF USING SEA FILES
cross_region_correlation_matrix = calculate_cross_region_correlations(
    pd.concat([center_lightnings,
               north_lightnings, south_lightnings]),
    pd.concat([center_pollutants,
               north_pollutants, south_pollutants])
)


# Set annotation and color bar font size
sns.heatmap(
    cross_region_correlation_matrix,
    annot=True,
    cmap='coolwarm',
    center=0,
    annot_kws={"size": 24},
    cbar_kws={"shrink": 1,"ticks": [-0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6], "format": "%.1f"}
)

plt.title('Comprehensive Correlation Matrix: Lightning and Pollutants Across Regions', fontsize=30)

# Access the current color bar
cbar = plt.gcf().axes[-1]  # Get the color bar's axis (last axis created)
cbar.tick_params(labelsize=25)  # Set font size for color bar tick labels

# Rotate y-axis labels
plt.yticks(rotation=0, fontsize=25)
plt.xticks(fontsize=25)

plt.figure(figsize=(16, 12))

# Save the figure
#plt.savefig('graphs/corr/heat map2', dpi=300)

plt.show()
