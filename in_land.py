import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


coordinates = pd.read_csv(r'exel\split land coordinates.csv')
polygon_lightning = pd.read_csv(r'exel\all data filtered.csv')

# Create a Plotly figure with Scattermapbox
fig = go.Figure(go.Scattermapbox(
    lat=coordinates.Latitude,  # Latitude coordinates
    lon=coordinates.Longitude,  # Longitude coordinates
    mode='lines',  # Draw lines to connect the coordinates
    line=dict(width=5, color='black'),  # Line properties
))

# Update layout to use mapbox
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=3,
    mapbox_center={"lat":31.771959, "lon":35.217018},
    title="Land and Sea Lightnings Distribution(all data)",
    title_font=dict(size=35),  # Set title size here
    legend=dict(font=dict(size=25)),  # Set legend text size here
    hoverlabel=dict(font=dict(size=30))  # Set hover text size here
)

fig2 = px.scatter_mapbox(
    polygon_lightning, lat='Latitude', lon='Longitude', size_max=10,
    zoom=0, mapbox_style="open-street-map"
)

# Update marker colors based on the 'on_land' values
fig2.update_traces(marker=dict(color=polygon_lightning['on_land'].map({0: 'red', 1: 'blue'})))

# Add legend for red markers
fig2.add_trace(go.Scattermapbox(
    lat=[None], lon=[None],
    mode='markers',
    marker=dict(size=20, color='red'),
    name='Lightnings over sea'
))

# Add legend for blue markers
fig2.add_trace(go.Scattermapbox(
    lat=[None], lon=[None],
    mode='markers',
    marker=dict(size=20, color='blue'),
    name='Lightnings over land'
))

fig.update_traces(marker=dict(size=20), showlegend=False)

for data in fig2.data:
    fig.add_trace(data)

#fig.write_html(r'links\blue&red-Tel Aviv.html')

# Show the plot
fig.show()
