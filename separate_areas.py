import pandas as pd
from shapely.geometry import Point, Polygon

import my_func

# Step 1: Load the CSV files
lightnings_df = pd.read_csv(r'exel\all data filtered.csv')
pollutants_df = pd.read_csv(r'exel\concatationFiltered.csv')

# Use polygon of desired area - land or sea
polygon_coordinates = pd.read_csv(r'exel\sea coordinates.csv')

# Extract latitude and longitude coordinates
latitudes = polygon_coordinates['Latitude'].tolist()
longitudes = polygon_coordinates['Longitude'].tolist()
coordinates = [(lat, lon) for lat, lon in zip(latitudes, longitudes)]  # Create pairs of lat and lon
polygon = Polygon(coordinates)  # Create the polygon itself
polygon = my_func.validate_polygon(polygon)

# Validate and fix lightning points
validated_points = my_func.validate_points(zip(lightnings_df['Longitude'], lightnings_df['Latitude']))

# Convert the list of tuples back to a DataFrame
validated_points_df = pd.DataFrame(validated_points, columns=['Longitude', 'Latitude'])

# Debug: Check the first few rows of the validated_points_df
print("Validated Points DataFrame:")
print(validated_points_df.head())

# Merge the validated points with the original DataFrame to retain all columns
lightnings_df = pd.concat([lightnings_df.drop(columns=['Longitude', 'Latitude']), validated_points_df], axis=1)

# Taking only land or sea lightnings if needed
lightnings_df.drop(lightnings_df[lightnings_df['on_land'] == 1].index, inplace=True)

# Taking only lightnings that are above 50KA
# Using this line is only when working on sea lightnings
lightnings_df.drop(lightnings_df[lightnings_df['peak current'].abs() < 50000].index, inplace=True)


# Debug: Check the type of lightnings_df after conversion and merge
print("Type of lightnings_df after conversion and merge:", type(lightnings_df))
print(lightnings_df.head())


# Step 2: Filter lightnings data points inside the polygon
lightnings_df = lightnings_df[lightnings_df.apply(
    lambda row: my_func.is_inside_territory((row['Latitude'], row['Longitude']), polygon), axis=1)].copy()

# Step 3: Filter pollutants dataset to include specific cities
# Modify this list to include the cities you're interested in for the chosen area
selected_cities = ['תל אביב-יפו','אשקלון','אשדוד']  # Example list of cities in Hebrew

pollutants_filtered_df = pollutants_df[pollutants_df['City'].isin(selected_cities)]
pollutants_filtered_df.drop(pollutants_filtered_df[pollutants_filtered_df['Station'] == 'פארק הכרמל'].index, inplace=True)

# Step 4: Define function to categorize lightning data by latitude
def categorize_area(latitude):
    #if latitude >= 32.518:
    if latitude >= 32.325144:
        return 'North'
    # use this line when working on land
    #elif latitude >= 32.027:
    #   return 'Center'
    else:
        return 'South'

# Debug: Check the type and first few values of 'Latitude' column
print("Latitude column type:", type(lightnings_df['Latitude']))
print(lightnings_df['Latitude'].head())

# Apply the function to create a new 'Area' column in the lightning dataframe
lightnings_df['Area'] = lightnings_df['Latitude'].apply(categorize_area)

# Step 5: Filter the pollutants data for the chosen area
chosen_area = 'North'  # Modify this to choose which area you are checking

lightnings_area_df = lightnings_df[lightnings_df['Area'] == chosen_area]
pollutants_area_df = pollutants_filtered_df  # Since we filtered by city already

# Step 6: Save each dataframe as a new CSV file
lightnings_area_df.to_csv(fr'exel\{chosen_area.lower()}_above50k_Half_Map_lightnings.csv', index=False)
#pollutants_area_df.to_csv(fr'exel\{chosen_area.lower()}_Half_Map_pollutants.csv', index=False)
