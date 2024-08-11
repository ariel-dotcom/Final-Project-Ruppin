import pandas as pd
from shapely.geometry import Polygon, Point
import geopandas as gpd
import my_func


# Read the polygon coordinates from the CSV file
polygon_coordinates = pd.read_csv(r'exel\coordinates no shore.csv')

# Create a polygon geometry from the coordinates
polygon_geom = Polygon(zip(polygon_coordinates['Lon'], polygon_coordinates['Lat']))

polygon_geom = my_func.validate_polygon(polygon_geom)

# Create a GeoDataFrame with the polygon geometry
polygon_gdf = gpd.GeoDataFrame(geometry=[polygon_geom])

# Define batch size
batch_size = 10000
counter=0

# Initialize an empty DataFrame to store filtered lightning points
filtered_lightning_df = pd.DataFrame(columns=['Latitude', 'Longitude'])

# Iterate over lightning data in batches
for chunk in pd.read_csv(r'exel\combined_file.csv', chunksize=batch_size):
    counter+=1
    print(counter)

    # Convert chunk to GeoDataFrame
    chunk_gdf = gpd.GeoDataFrame(chunk, geometry=gpd.points_from_xy(chunk.Longitude, chunk.Latitude))

    # Filter lightning points inside the territory
    chunk_lightning = chunk_gdf[chunk_gdf.geometry.within(polygon_gdf.geometry.iloc[0])]

    # Append filtered lightning points to the DataFrame
    filtered_lightning_df = pd.concat([filtered_lightning_df, chunk_lightning], ignore_index=True)

# Save the filtered lightning coordinates to a new CSV file
filtered_lightning_df.to_csv(r'exel\all data.csv', index=False)