import pandas as pd
import matplotlib.pyplot as plt
import calendar
import glob
import os
import numpy as np
import plotly.express as px
import plotly.graph_objects as go




#the number of lightnings from land vs sea
def landVSseaNumber(data):
    # Convert the 'DATE AND TIME' column to datetime format and extract the month
    data['DATE AND TIME'] = pd.to_datetime(data['DATE AND TIME'], format='%Y%m%dT%H%M%S.%f')
    data['Month'] = data['DATE AND TIME'].dt.month

    # Group by month and 'on_land' status and count the number of events
    monthly_counts = data.groupby(['Month', 'on_land']).size().unstack(fill_value=0)

    # Use month names instead of numbers, reordering for December, January, and February
    ordered_months = ['December', 'January', 'February']
    ordered_month_numbers = [12, 1, 2]

    # Create a reordered DataFrame
    monthly_counts_reordered = monthly_counts.reindex(ordered_month_numbers)
    monthly_counts_reordered.index = ordered_months

    # Plot the results with separate bars for land and sea
    fig, ax = plt.subplots(figsize=(12, 6))

    # Define bar width and positions
    bar_width = 0.35
    months = monthly_counts_reordered.index
    land_counts = monthly_counts_reordered[1]
    sea_counts = monthly_counts_reordered[0]

    bar_positions = range(len(months))
    ax.bar(bar_positions, sea_counts, bar_width, label='Sea', color='blue')
    ax.bar([p + bar_width for p in bar_positions], land_counts, bar_width, label='Land', color='orange')

    # Add titles and labels
    ax.set_title('Number of Lightnings on Land vs Sea for December, January, and February')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Lightnings')
    ax.set_xticks([p + bar_width / 2 for p in bar_positions])
    ax.set_xticklabels(months, rotation=45)
    ax.legend(title='Location')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Show the plot
    plt.show()

#the average number of lightnings from land vs sea
def landVSseaAverage(data):
    # Convert the 'DATE AND TIME' column to datetime format and extract the month and year
    data['DATE AND TIME'] = pd.to_datetime(data['DATE AND TIME'], format='%Y%m%dT%H%M%S.%f')
    data['Month'] = data['DATE AND TIME'].dt.month
    data['Year'] = data['DATE AND TIME'].dt.year

    # Group by month, year, and 'on_land' status and count the number of events
    monthly_yearly_counts = data.groupby(['Year', 'Month', 'on_land']).size().unstack(fill_value=0)

    # Calculate the average number of events per month across all years
    monthly_avg_counts = monthly_yearly_counts.groupby(['Month']).mean()

    # Reorder months
    ordered_months = ['December', 'January', 'February']
    ordered_month_numbers = [12, 1, 2]
    monthly_avg_counts = monthly_avg_counts.reindex(ordered_month_numbers)
    monthly_avg_counts.index = ordered_months

    # Plot the results with separate bars for land and sea
    fig, ax = plt.subplots(figsize=(12, 6))

    # Define bar width and positions
    bar_width = 0.35
    months = monthly_avg_counts.index
    land_avg_counts = monthly_avg_counts[1]
    sea_avg_counts = monthly_avg_counts[0]

    bar_positions = range(len(months))
    ax.bar(bar_positions, sea_avg_counts, bar_width, label='Sea', color='blue')
    ax.bar([p + bar_width for p in bar_positions], land_avg_counts, bar_width, label='Land', color='orange')

    # Add titles and labels
    ax.set_title('Average Number of Lightnings on Land vs Sea for Each Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Number of Lightnings')
    ax.set_xticks([p + bar_width / 2 for p in bar_positions])
    ax.set_xticklabels(months, rotation=45)
    ax.legend(title='Location')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Show the plot
    plt.show()

#graph that contains all power ranges for a specific month
def lightningsPowerMonths():
    # Define the path where the CSV files are located
    path = r'exel\months df'

    # Get all CSV files in the directory
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    # Define the power ranges
    power_bins = [0, 50000, 100000, 150000, 200000, float('inf')]
    power_labels = ['Up to 50k', '50k-100k', '100k-150k', '150k-200k', 'Above 200k']

    for file in csv_files:
        # Extract the month from the file name
        month = os.path.basename(file).split('.')[0]

        # Load the data
        data = pd.read_csv(file)

        # Classify the peak current values into bins
        data['Power Range'] = pd.cut(data['peak current'].abs(), bins=power_bins, labels=power_labels)

        # Count the number of events in each range
        power_counts = data['Power Range'].value_counts().reindex(power_labels).fillna(0)

        # Plot the results
        plt.figure(figsize=(10, 6))
        power_counts.plot(kind='bar', color='skyblue')
        plt.title(f'Number of Lightnings in {month}')
        plt.xlabel('Peak Current Range')
        plt.ylabel('Number of Lightnings')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Save the figure
        image_path = f'lightnings_power_{month}.png'
        plt.savefig(fr'graphs\{image_path}')
        plt.close()

    print("Graphs generated and saved successfully.")

#power ranges for all months - land vs sea
def powerRangesLandVsSea(data):
    # Parse the 'DATE AND TIME' column to extract month and year
    data['DATE AND TIME'] = pd.to_datetime(data['DATE AND TIME'], format='%Y%m%dT%H%M%S.%f')
    data['Month'] = data['DATE AND TIME'].dt.month

    # Define the power ranges and labels
    power_bins = [0, 50000, 100000, 150000, 200000, 500000]
    power_labels = ['0-50k', '50k-100k', '100k-150k', '150k-200k', '200k-500k']

    # Reorder month names
    month_order = ['December', 'January', 'February']

    # Function to filter data by power range and plot
    def filter_and_plot(data, power_range, label):
        filtered_land = data[(data['peak current'].abs() >= power_range[0]) &
                             (data['peak current'].abs() < power_range[1]) &
                             (data['on_land'] == 1)]

        filtered_sea = data[(data['peak current'].abs() >= power_range[0]) &
                            (data['peak current'].abs() < power_range[1]) &
                            (data['on_land'] == 0)]

        # Group by month and count lightning events
        monthly_counts_land = filtered_land.groupby('Month').size().reset_index(name='Land_Count')
        monthly_counts_sea = filtered_sea.groupby('Month').size().reset_index(name='Sea_Count')

        # Merge land and sea counts on month and fill missing values with 0
        monthly_counts = pd.merge(monthly_counts_land, monthly_counts_sea, on='Month', how='outer').fillna(0)

        # Convert month numbers to month names and reorder
        monthly_counts['Month'] = monthly_counts['Month'].apply(lambda x: calendar.month_name[x])
        monthly_counts = monthly_counts.set_index('Month').reindex(month_order).reset_index()

        # Calculate the total count of lightning events
        total_count = monthly_counts[['Land_Count', 'Sea_Count']].sum().sum()

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))

        # Define bar width and locations for land and sea bars
        bar_width = 0.35
        index = np.arange(len(monthly_counts))

        # Plot the monthly sums for filtered data
        land_bar = ax.bar(index - bar_width / 2, monthly_counts['Land_Count'], bar_width, color='orange',
                          label='Land Lightning')
        sea_bar = ax.bar(index + bar_width / 2, monthly_counts['Sea_Count'], bar_width, color='blue',
                         label='Sea Lightning')

        # Annotate the plot with the highest peak current values
        if label == '200k-500k':
            # Find the highest peak current for land and sea for each month
            highest_land = filtered_land.groupby('Month')['peak current'].apply(lambda x: x.abs().max()).reset_index(
                name='Highest_Land')
            highest_sea = filtered_sea.groupby('Month')['peak current'].apply(lambda x: x.abs().max()).reset_index(
                name='Highest_Sea')

            # Convert month numbers to month names and reorder
            highest_land['Month'] = highest_land['Month'].apply(lambda x: calendar.month_name[x])
            highest_sea['Month'] = highest_sea['Month'].apply(lambda x: calendar.month_name[x])
            highest_land = highest_land.set_index('Month').reindex(month_order).reset_index()
            highest_sea = highest_sea.set_index('Month').reindex(month_order).reset_index()

            # Merge highest peak current data with the monthly counts
            monthly_counts = monthly_counts.merge(highest_land, on='Month', how='left')
            monthly_counts = monthly_counts.merge(highest_sea, on='Month', how='left')

            # Annotate each bar with the highest peak current value
            for i in range(len(monthly_counts)):
                month = monthly_counts.iloc[i]['Month']
                land_count = monthly_counts.iloc[i]['Land_Count']
                sea_count = monthly_counts.iloc[i]['Sea_Count']
                highest_land_val = monthly_counts.iloc[i]['Highest_Land']
                highest_sea_val = monthly_counts.iloc[i]['Highest_Sea']

                if not np.isnan(highest_land_val):
                    ax.text(i - bar_width / 2, land_count + 1, f'{highest_land_val:.0f}', ha='center', va='bottom',
                            fontsize=8, color='red')

                if not np.isnan(highest_sea_val):
                    ax.text(i + bar_width / 2, sea_count + 1, f'{highest_sea_val:.0f}', ha='center', va='bottom',
                            fontsize=8, color='blue')

        ax.set_xlabel('Month')
        ax.set_ylabel(f'Total Lightning Events ({label})')
        ax.set_title(f'Monthly Lightning Events in Israel ({label})\nTotal Count: {total_count}')
        ax.set_xticks(index)
        ax.set_xticklabels(monthly_counts['Month'])
        ax.legend()

        # Save the figure with the same name as the graph
        graph_file_path = fr'graphs\power_{label}_land_sea.png'
        plt.tight_layout()
        plt.savefig(graph_file_path)
        plt.close(fig)  # Close the figure to free up memory

        # Create a map showing the locations of lightning strikes
        map_file_path = fr'links\lightning_{label}.html'
        create_scattermapbox(filtered_land, filtered_sea, label, map_file_path)

    def create_scattermapbox(filtered_land, filtered_sea, label, map_file_path):
        # Initialize the map
        fig = go.Figure()

        # Add traces for land lightning
        # Add traces for land lightning with hover information
        fig.add_trace(go.Scattermapbox(
            lat=filtered_land['Latitude'],
            lon=filtered_land['Longitude'],
            mode='markers',
            marker=dict(size=4, color='red'),
            name='Land Lightning',
            text=filtered_land['peak current'],
            hoverinfo='text+lat+lon',
            showlegend=True  # Show in legend
        ))

        # Add traces for sea lightning
        fig.add_trace(go.Scattermapbox(
            lat=filtered_sea['Latitude'],
            lon=filtered_sea['Longitude'],
            mode='markers',
            marker=dict(size=4, color='blue'),
            name='Sea Lightning',
            text=filtered_sea['peak current'],
            hoverinfo='text+lat+lon',
            showlegend=True  # Show in legend
        ))

        # Add the polygon border
        polygon_coordinates = pd.read_csv(r'exel\coordinates no shore.csv')
        fig.add_trace(go.Scattermapbox(
            lat=polygon_coordinates['Latitude'],
            lon=polygon_coordinates['Longitude'],
            mode='lines',
            line=dict(width=2, color='black'),
            name='Border'
        ))

        # Set the layout of the map
        fig.update_layout(
            mapbox=dict(
                style='open-street-map',
                center=dict(lat=data['Latitude'].mean(), lon=data['Longitude'].mean()),
                zoom=8
            ),
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            title=f'Lightning Events ({label})'
        )

        # Save the map as an HTML file
        fig.write_html(map_file_path)

    # Iterate over power ranges and labels to create and save plots
    for i in range(len(power_bins) - 1):
        filter_and_plot(data, power_range=(power_bins[i], power_bins[i + 1]), label=power_labels[i])

#show average number of lightnings of each hour from the entire data
def avergaeLightningsByHour(data):
    # Convert the 'DATE AND TIME' column to datetime format and extract the month and hour
    data['DATE AND TIME'] = pd.to_datetime(data['DATE AND TIME'], format='%Y%m%dT%H%M%S.%f')
    data['Month'] = data['DATE AND TIME'].dt.month
    data['Hour'] = data['DATE AND TIME'].dt.hour

    # Filter data for months 1, 2, and 12
    data_filtered = data[data['Month'].isin([1, 2, 12])]

    # Group by month, hour, and 'on_land' status and calculate the average number of events
    hourly_counts = data_filtered.groupby(['Month', 'Hour', 'on_land']).size().unstack(fill_value=0)
    hourly_counts = hourly_counts.groupby(level=[0, 1]).mean()

    # Plot the results with separate bars for land and sea
    fig, ax = plt.subplots(figsize=(12, 6))

    # Define bar width and positions
    bar_width = 0.4
    bar_positions = range(24)

    # Plot bars for land and sea
    for hour in range(24):
        sea_lightnings = hourly_counts.loc[(slice(None), hour), 0].values
        land_lightnings = hourly_counts.loc[(slice(None), hour), 1].values

        ax.bar([hour - bar_width / 4], sea_lightnings, bar_width / 2, color='blue')
        ax.bar([hour + bar_width / 4], land_lightnings, bar_width / 2, color='orange')

    # Add titles and labels
    ax.set_title('Average Number of Lightnings on Land vs Sea for Each Hour of the Day')
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Average Number of Lightnings')
    ax.set_xticks(range(24))
    ax.set_xticklabels(range(24))
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Show the legend
    ax.legend(['Sea', 'Land'], title='Location')

    plt.tight_layout()

    # Show the plot
    plt.show()

#show for each month the average number of lightnings of each hour
def avergaeLightningsByHour2(data):
    # Convert the 'DATE AND TIME' column to datetime format and extract the hour and month
    data['DATE AND TIME'] = pd.to_datetime(data['DATE AND TIME'], format='%Y%m%dT%H%M%S.%f')
    data['Hour'] = data['DATE AND TIME'].dt.hour
    data['Month'] = data['DATE AND TIME'].dt.month

    months = [1,2,12]
    labels = {1: "January", 2: "February", 12: "December"}
    for i in months:
        # Filter the data to include only January (Month == 1)
        january_data = data[data['Month'] == i]

        # Group by hour and 'on_land' status and count the number of events
        hourly_counts = january_data.groupby(['Hour', 'on_land']).size().unstack(fill_value=0)

        # Calculate the average number of events per hour
        # Since we are only considering January, the number of years can be found by the number of unique years in the data
        num_years = january_data['DATE AND TIME'].dt.year.nunique()
        hourly_averages = hourly_counts / num_years

        # Plot the results with separate bars for land and sea
        fig, ax = plt.subplots(figsize=(12, 6))

        # Define bar width and positions
        bar_width = 0.35
        hours = hourly_averages.index
        land_counts = hourly_averages[1]
        sea_counts = hourly_averages[0]

        bar_positions = range(len(hours))
        ax.bar(bar_positions, sea_counts, bar_width, label='Sea', color='blue')
        ax.bar([p + bar_width for p in bar_positions], land_counts, bar_width, label='Land', color='orange')

        # Add titles and labels
        ax.set_title(f'Average Number of Lightnings on Land vs Sea for Each Hour in {labels[i]}')
        ax.set_xlabel('Hour of the Day')
        ax.set_ylabel('Average Number of Lightnings')
        ax.set_xticks([p + bar_width / 2 for p in bar_positions])
        ax.set_xticklabels(hours, rotation=45)
        ax.legend(title='Location')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Show the plot
        plt.show()

#shows the average power for each month from the entire data
def averagePowerByMonth(data):
    # Convert the 'DATE AND TIME' column to datetime format and extract the month
    data['DATE AND TIME'] = pd.to_datetime(data['DATE AND TIME'], format='%Y%m%dT%H%M%S.%f')
    data['Month'] = data['DATE AND TIME'].dt.month

    # Ensure 'peak current' column is in the correct numeric format and take absolute values
    data['peak current'] = pd.to_numeric(data['peak current'], errors='coerce').abs()

    # Group by month and 'on_land' status and calculate the average peak current
    monthly_avg_peak_current = data.groupby(['Month', 'on_land'])['peak current'].mean().unstack(fill_value=0)

    # Reorder months
    ordered_months = ['December', 'January', 'February']
    ordered_month_numbers = [12, 1, 2]
    monthly_avg_peak_current = monthly_avg_peak_current.reindex(ordered_month_numbers)
    monthly_avg_peak_current.index = ordered_months

    # Plot the results with separate bars for land and sea
    fig, ax = plt.subplots(figsize=(12, 6))

    # Define bar width and positions
    bar_width = 0.35
    months = monthly_avg_peak_current.index
    land_avg_peak_current = monthly_avg_peak_current[1]
    sea_avg_peak_current = monthly_avg_peak_current[0]

    bar_positions = range(len(months))
    ax.bar(bar_positions, sea_avg_peak_current, bar_width, label='Sea', color='blue')
    ax.bar([p + bar_width for p in bar_positions], land_avg_peak_current, bar_width, label='Land', color='orange')

    # Add titles and labels
    ax.set_title('Average Peak Current of Lightnings on Land vs Sea for Each Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Peak Current of Lightnings')
    ax.set_xticks([p + bar_width / 2 for p in bar_positions])
    ax.set_xticklabels(months, rotation=45)
    ax.legend(title='Location')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Show the plot
    plt.show()

#show the number and average power of all lightnings for each hour
def numberAndPowerAllData(data):
    # Convert the 'DATE AND TIME' column to datetime format and extract the hour
    data['DATE AND TIME'] = pd.to_datetime(data['DATE AND TIME'], format='%Y%m%dT%H%M%S.%f')
    data['Hour'] = data['DATE AND TIME'].dt.hour

    # Take the absolute value of 'peak current'
    data['peak current'] = data['peak current'].abs()

    # Group by hour and calculate the number of lightnings and average peak current
    hourly_counts = data.groupby('Hour').size()
    hourly_peak_current = data.groupby('Hour')['peak current'].mean()

    # Plot the number of lightnings
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.bar(hourly_counts.index, hourly_counts.values, color='blue')
    ax1.set_title('Number of Lightnings by Hour')
    ax1.set_xlabel('Hour')
    ax1.set_ylabel('Number of Lightnings')
    ax1.set_xticks(hourly_counts.index)
    ax1.set_xticklabels(hourly_counts.index, rotation=45)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

    # Plot the average peak current
    fig, ax2 = plt.subplots(figsize=(12, 6))

    ax2.bar(hourly_peak_current.index, hourly_peak_current.values, color='orange')
    ax2.set_title('Average Peak Current by Hour')
    ax2.set_xlabel('Hour')
    ax2.set_ylabel('Average Peak Current')
    ax2.set_xticks(hourly_peak_current.index)
    ax2.set_xticklabels(hourly_peak_current.index, rotation=45)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

#correlat
# ion between number of lighnings and their power
def lightningCountVsPeakCurrent(data):
    max_peak_current = int(data['peak current'].abs().max())

    # Initialize peak current ranges
    peak_current_ranges = []
    if max_peak_current <= 200000:
        # Use jumps of 10,000
        peak_current_ranges = [(i, i + 10000) for i in range(0, max_peak_current + 1, 10000)]
    else:
        # Use jumps of 50,000 after reaching 200,000
        for i in range(0, 200000, 10000):
            peak_current_ranges.append((i, i + 10000))
        for i in range(200000, max_peak_current + 1, 50000):
            if i < 500000:
                peak_current_ranges.append((i, i + 50000))

    # Step 2: Count the number of lightning strikes in each range
    lightning_counts = []
    filtered_ranges = []
    for start, end in peak_current_ranges:
        count = ((data['peak current'].abs() >= start) & (data['peak current'].abs() < end)).sum()
        if count != 0:
            lightning_counts.append(count)
            filtered_ranges.append((start, end))

    # Create a DataFrame with filtered peak current ranges and corresponding lightning counts
    df = pd.DataFrame({'Peak Current Range': [f"{start}-{end}" for start, end in filtered_ranges],
                       'Number of Lightning Strikes': lightning_counts})

    # Step 3: Plotting with Plotly
    fig = px.bar(df, x='Peak Current Range', y='Number of Lightning Strikes',
                 title='Number of Lightning Strikes for Each Peak Current Range',
                 labels={'Number of Lightning Strikes': 'Number of Strikes'},
                 hover_data={'Number of Lightning Strikes': True},
                 color='Peak Current Range',
                 color_discrete_sequence=px.colors.qualitative.Light24)

    # Customize layout
    fig.update_layout(xaxis_title='Peak Current Range', yaxis_title='Number of Strikes',
                      xaxis_tickangle=-45, bargap=0.2)

    # Set a minimum height for the y-axis
    min_height = 5  # Adjust the minimum height of bars here
    fig.update_yaxes(range=[min_height, None])

    # Save as HTML
    fig.write_html(r'links\correlation.html')

    # Show plot
    fig.show()

