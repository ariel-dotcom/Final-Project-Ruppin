import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from shapely.geometry import Polygon
import my_func
from global_land_mask import globe


polygon_coordinates = pd.read_csv(r'exel\split land coordinates.csv')
# Extract latitude and longitude coordinates
latitudes = polygon_coordinates['Latitude'].tolist()
longitudes = polygon_coordinates['Longitude'].tolist()
coordinates = [(Latitude, Longitude) for Latitude, Longitude in zip(latitudes, longitudes)] # Create pairs of lon and lat
polygon = Polygon(coordinates) # Create the polygon itself

lightning_df = pd.read_csv(r'exel\all data filtered.csv')


"""
lightning_df = lightning_df[lightning_df["Latitude"]> 32.518]
lightning_df.to_csv("North_check.csv", index=False)
"""


# Define latitude ranges and corresponding area names
latitude_ranges = [(32.518, float('inf')), (32.027, 32.518), (-float('inf'), 32.027)]
area_names = ['North', 'Center', 'South']

# Create an empty DataFrame to store the result
area_lightnings_count = pd.DataFrame(columns=["area", "num_of_lightnings"])

# Iterate over latitude ranges and area names
for latitude_range, area_name in zip(latitude_ranges, area_names):
    # Filter the DataFrame for lightnings within the latitude range
    filtered_lightnings = lightning_df[
        (latitude_range[0] < lightning_df['Latitude']) & (lightning_df['Latitude'] <= latitude_range[1])
        ]

    # Count the number of lightnings in the current area
    num_of_lightnings = len(filtered_lightnings)

    # Append the data to the result DataFrame
    area_lightnings_count = area_lightnings_count._append({'area': area_name, 'num_of_lightnings': num_of_lightnings},ignore_index=True)


print(area_lightnings_count)
#area_lightnings_count.to_csv(r'exel\area_lightnings_count_all_data.csv', index=False)


# Validate and fix polygon geometry
polygon = my_func.validate_polygon(polygon)

# Validate and fix lightning points
valid_lightning_points = my_func.validate_points(zip(lightning_df['Longitude'], lightning_df['Latitude']))


#Filter lightning occurrences inside the territory
polygon_lightning = lightning_df[lightning_df.apply(
    lambda row: my_func.is_inside_territory((row['Latitude'], row['Longitude']), polygon), axis=1)].copy()

polygon_lightning['on_land'] = polygon_lightning.apply(lambda row: 1 if globe.is_land(row['Latitude'], row['Longitude']) else 0, axis=1)


# Create a Plotly figure with Scattermapbox
fig = go.Figure(go.Scattermapbox(
    lat=latitudes,  # Latitude coordinates
    lon=longitudes,  # Longitude coordinates
    mode='lines',  # Draw lines to connect the coordinates
    line=dict(width=5, color='black'),  # Line properties
))

# Update layout to use mapbox
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=3,
    mapbox_center={"lat": 31.771959, "lon": 35.217018},
    title="Lightnings Distribution By Zone(all data)",
    title_font=dict(size=25),  # Set title size here
    legend=dict(font=dict(size=25)),  # Set legend text size here
    hoverlabel=dict(font=dict(size=30))  # Set hover text size here
)

# Create a trace for the density map
fig2 = px.scatter_mapbox(
    polygon_lightning, lat='Latitude', lon='Longitude', #z='peak current',
    #radius=10,
    zoom=0, mapbox_style="open-street-map", title='heatmap israel'
)

# Update marker size for the Scattermapbox trace
fig.update_traces(marker=dict(size=20))

# Combine both traces into one figure
for data in fig2.data:
    fig.add_trace(data)

# Show the plot
fig.show()

# Save the plot as HTML
#fig.write_html(r"links\land_lightnings all data.html")
