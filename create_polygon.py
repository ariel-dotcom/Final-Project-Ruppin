import pandas as pd

# Read the data from the text file
polygon_coordinates = pd.read_csv(r'exel\polygon2.txt', header=None, names=['FID', 'Id', 'ORIG_FID', 'Lat', 'Lon'])

# Extract latitude and longitude coordinates
latitudes = polygon_coordinates['Lat']
longitudes = polygon_coordinates['Lon']

# Create a DataFrame with latitude and longitude columns
coordinates_df = pd.DataFrame({'Latitude': latitudes, 'Longitude': longitudes})

# Save the DataFrame to a CSV file
coordinates_df.to_csv(r'exel\coordinates.csv', index=False)

print("Extraction completed. Output saved to 'coordinates.csv'.")
