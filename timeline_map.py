import pandas as pd
import plotly.express as px
from shapely.geometry import Polygon, Point
import plotly.graph_objects as go
import my_func


# Function to adjust intensity
def adjust_intensity(power):
    return min(power, 30000)  # Cap intensity at 30K for visualization purposes

# Read the CSV file
result = pd.read_csv(r"exel\all data filtered.csv")

# Extract month from 'Date' and create 'Month' column
result['Month'] = result['DATE AND TIME'].str[:4] + '-' + result['DATE AND TIME'].str[4:6]
result['Month'] = result['Month'].str.replace('/', '')
result = result.sort_values(by='Month')


# Apply adjust_intensity to 'peak current' column
result['peak current'] = result['peak current'].apply(adjust_intensity)


# Drop the 'Date' column as it is no longer needed
result = result.drop(columns=["DATE AND TIME"])


polygon_coordinates = pd.read_csv(r'exel\coordinates no shore.csv')
# Extract latitude and longitude coordinates
latitudes = polygon_coordinates['Lat'].tolist()
longitudes = polygon_coordinates['Lon'].tolist()
coordinates = [(lat, lon) for lat, lon in zip(latitudes, longitudes)] # Create pairs of lon and lat
polygon = Polygon(coordinates) # Create the polygon itself

# Validate and fix polygon geometry
polygon = my_func.validate_polygon(polygon)

# Validate and fix lightning points
valid_lightning_points = my_func.validate_points(zip(result['Longitude'], result['Latitude']))


# Filter lightning occurrences inside the territory
polygon_lightning = result[result.apply(
    lambda row: my_func.is_inside_territory((row['Latitude'], row['Longitude']), polygon), axis=1)]


# Plotting the density map
fig_density = px.density_mapbox(polygon_lightning, lat='Latitude', lon='Longitude', z='peak current', radius=7,
                                center=dict(lat=30, lon=0),
                                title="Lightning density | 2017-2021",
                                hover_name='peak current',
                                zoom=1,
                                hover_data={"Month": False, "peak current": False, 'Latitude': False,
                                            'Longitude': False, "Month": False},
                                mapbox_style="open-street-map",
                                width=1400,
                                height=800,
                                opacity=1,
                                range_color=[1, result["peak current"].max()],
                                labels={'peak current': 'Strongest Lightning (J)'},
                                animation_frame='Month')



# Create a Plotly figure with Scattermapbox
fig = go.Figure(go.Scattermapbox(
    lat=latitudes,  # Latitude coordinates
    lon=longitudes,  # Longitude coordinates
    mode='lines',  # Draw lines to connect the coordinates
    line=dict(width=1, color='blue'),  # Line properties
))
for data in fig.data:
    fig_density.add_trace(data)

fig_density.write_html(r'links\timeline.html')
#fig_density.show()


# Plotting the scatter geo map
fig_intensity = px.scatter_geo(polygon_lightning, lat='Latitude', lon='Longitude', color="peak current",
                               hover_name="peak current", size="multiplicity",
                               animation_frame="Month",
                               projection="winkel tripel",
                               hover_data={"Month": False, "peak current": False, 'Latitude': False,
                                           'Longitude': False, "Month": False},
                               center=dict(lat=31.771959, lon=35.217018),
                               width=1400,
                               height=800,
                               size_max=25,
                               range_color=[0, result["peak current"].max()],
                               title="Lightning intensity  | Dec.,Jan.,Feb. 2017-2021",
                               labels={'peak current': 'Strongest Lightning'})

fig_intensity.write_html(r'links\Worldwide Intensity over water.html')
#fig_intensity.show()