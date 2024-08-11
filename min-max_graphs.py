import pandas as pd
import matplotlib.pyplot as plt

# Define file paths for new data
# sea files
new_files = {
    'north': {'lightnings': 'exel/north_above50k_Half_Map_lightnings.csv',
              'pollutants': 'exel/north_Half_Map_pollutants.csv'},
    'south': {'lightnings': 'exel/south_above50k_Half_Map_lightnings.csv',
              'pollutants': 'exel/south_Half_Map_pollutants.csv'}
}
# land files
#new_files = {
#    'center': {'lightnings': 'exel/center_lightnings.csv',
#               'pollutants': 'exel/center_pollutants.csv'},
#    'north': {'lightnings': 'exel/north_lightnings.csv',
#              'pollutants': 'exel/north_pollutants.csv'},
#    'south': {'lightnings': 'exel/south_lightnings.csv',
#              'pollutants': 'exel/south_pollutants.csv'}
#}



# Load all data into dictionaries
lightning_data = {}
pollution_data = {}

for region, paths in new_files.items():
    lightning_data[region] = pd.read_csv(paths['lightnings'])
    pollution_data[region] = pd.read_csv(paths['pollutants'])


    # Process lightning data
    lightning_data[region]['DATE AND TIME'] = pd.to_datetime(lightning_data[region]['DATE AND TIME'],
                                                             format='%Y%m%dT%H%M%S.%f')
    lightning_data[region]['Hour'] = lightning_data[region]['DATE AND TIME'].dt.hour
    lightning_data[region]['abs_peak_current'] = lightning_data[region]['peak current'].abs()

    # Min-Max normalization
    min_peak = lightning_data[region]['abs_peak_current'].min()
    max_peak = lightning_data[region]['abs_peak_current'].max()
    lightning_data[region]['Min-Max'] = (lightning_data[region]['abs_peak_current'] - min_peak) / (max_peak - min_peak)

    # Aggregate the normalized values by hour
    lightning_data[region] = lightning_data[region].groupby('Hour')['Min-Max'].mean()

    # Process pollution data
    pollution_data[region]['Date'] = pd.to_datetime(pollution_data[region]['Date'], errors='coerce')
    pollution_data[region] = pollution_data[region].dropna(subset=['Date'])
    pollution_data[region]['Hour'] = pollution_data[region]['Date'].dt.hour

# Plotting all combinations of lightnings and pollutants
for lightning_region, lightning_df in lightning_data.items():
    for pollution_region, pollution_df in pollution_data.items():
        pollutants = pollution_df['pollutant'].unique()

        for pollutant in pollutants:
            # Create a copy to avoid SettingWithCopyWarning
            pollutant_data = pollution_df[pollution_df['pollutant'] == pollutant].copy()

            # Min-Max normalization
            min_value = pollutant_data['Value'].min()
            max_value = pollutant_data['Value'].max()
            pollutant_data['Min-Max'] = (pollutant_data['Value'] - min_value) / (max_value - min_value)

            # Aggregate the normalized values by hour
            hourly_pollution = pollutant_data.groupby('Hour')['Min-Max'].mean()

            # Plot the data with two y-axes
            fig, ax1 = plt.subplots(figsize=(12, 6))
            ax1.set_xlabel('Hour of the Day')
            ax1.set_ylabel('Normalized Lightning Peak Current (Min-Max)', color='tab:red')
            ax1.plot(lightning_df.index, lightning_df.values, marker='o', linestyle='-', color='tab:red',
                     label='Lightning')
            ax1.tick_params(axis='y', labelcolor='tab:red')

            ax2 = ax1.twinx()
            ax2.set_ylabel(f'Normalized {pollutant} Values (Min-Max)', color='tab:blue')
            ax2.plot(hourly_pollution.index, hourly_pollution.values, marker='o', linestyle='-', color='tab:blue',
                     label=pollutant)
            ax2.tick_params(axis='y', labelcolor='tab:blue')

            fig.tight_layout(rect=[0, 0, 1, 0.95])
            plt.title(
                f'Normalized: {lightning_region.capitalize()} lightnings with {pollution_region.capitalize()} {pollutant}')
            plt.grid(True)
            plt.xticks(range(0, 24))
            # plt.show()
            # Save the plot as an image file
            label = f'{lightning_region.capitalize()} Lightnings with {pollution_region.capitalize()} {pollutant} min-max'
            #change the path accordingly to land or sea
            filename = fr'graphs\normalHour_sea_above50k\{label}.png'.replace(' ', '_')
            plt.savefig(filename)

            plt.close(fig)  # Close the figure to free up memory

            # Check if the data is correct
            print(f"Region: {lightning_region}, Pollutant: {pollutant}")
            print(lightning_df.head())
            print(hourly_pollution.head())
