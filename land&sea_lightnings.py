import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


coordinates = pd.read_csv(r'exel\sea coordinates.csv')
polygon_lightning = pd.read_csv(r'exel\south_Half_Map_lightnings.csv')

# Create a Plotly figure with Scattermapbox
fig = go.Figure(go.Scattermapbox(
    lat=coordinates.Latitude,  # Latitude coordinates
    lon=coordinates.Longitude,  # Longitude coordinates
    mode='lines',  # Draw lines to connect the coordinates
    line=dict(width=1, color='blue'),  # Line properties
))

# Update layout to use mapbox
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=3,
    mapbox_center={"lat":31.771959, "lon":35.217018},
    title="Total Lightnings(all data)",
    title_font=dict(size=25),  # Set title size here
    legend=dict(font=dict(size=25)),  # Set legend text size here
    hoverlabel=dict(font=dict(size=30)),  # Set hover text size here
)

fig2 = px.density_mapbox(
    polygon_lightning, lat='Latitude', lon='Longitude', z='peak current',
    radius=10,
    zoom=0, mapbox_style="open-street-map", title='heatmap israel',
    color_continuous_scale="Viridis"  # Set color scale

)
fig.update_traces(marker=dict(size=20), showlegend=False)
fig2.update_coloraxes(colorbar=dict(title_font=dict(size=20)))

for data in fig2.data:
    fig.add_trace(data)

#Show the plot
fig.show()
#fig.write_html(r"links\land&sea all data.html")

