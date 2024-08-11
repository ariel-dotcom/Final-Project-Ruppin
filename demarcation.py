import pandas as pd
from shapely.geometry import Polygon
from global_land_mask import globe
import my_func
import time
import os

# Record the starting time
start_time = time.time()

def print_elapsed_time(start_time):
    elapsed_time = time.time() - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds), "elapsed.")

# Define the file paths
coordinates_file = r'exel\polygon-Tel Aviv.csv'
lightning_data_file = r'exel\all data filtered.csv'
output_file = r'exel\Tel-Aviv filtered.csv'

# Define chunk size for reading data
chunk_size = 10000

# Read polygon coordinates
polygon_coordinates_chunks = pd.read_csv(coordinates_file, chunksize=chunk_size)
for chunk in polygon_coordinates_chunks:
    latitudes = chunk['Latitude'].tolist()
    longitudes = chunk['Longitude'].tolist()
    coordinates = [(lat, lon) for lat, lon in zip(latitudes, longitudes)]
    polygon = Polygon(coordinates)

print("Time after creating polygon:")
print_elapsed_time(start_time)

# Initialize DataFrame to store filtered lightning data
filtered_lightning_data = pd.DataFrame()

# Read lightning data in chunks
lightning_data_chunks = pd.read_csv(lightning_data_file, chunksize=chunk_size)
for chunk in lightning_data_chunks:
    # Validate and fix lightning points
    valid_lightning_points = my_func.validate_points(zip(chunk['Longitude'], chunk['Latitude']))

    # Filter lightning occurrences inside the territory
    chunk_lightning = chunk[chunk.apply(
        lambda row: my_func.is_inside_territory((row['Latitude'], row['Longitude']), polygon), axis=1)].copy()

    filtered_lightning_data = pd.concat([filtered_lightning_data, chunk_lightning])

print("Time after filtering:")
print_elapsed_time(start_time)


# Print the filtered lightning data
print(filtered_lightning_data)

# Add a column indicating whether the lightning occurrence is on land
#filtered_lightning_data['on_land'] = filtered_lightning_data.apply(
#    lambda row: 1 if globe.is_land(row['Latitude'], row['Longitude']) else 0, axis=1)

#print("Time after adding on_land column:")
#print_elapsed_time(start_time)

# Save the filtered lightning data to a CSV file
if not filtered_lightning_data.empty:
    filtered_lightning_data.to_csv(output_file, index=False)
else:
    print("No lightning occurrences found inside the territory.")

# Record the ending time
end_time = time.time()

# Total time elapsed
total_time = end_time - start_time
hours, rem = divmod(total_time, 3600)
minutes, seconds = divmod(rem, 60)
print("Total time:", "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds), "elapsed.")

#os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")