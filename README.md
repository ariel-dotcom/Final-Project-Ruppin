
# Lightning and Pollutant Correlation in Israel

## Overview

This project is part of my final work as a Computer Science student, where I analyzed the correlation between lightning occurrences and pollutant levels in Israel. The project involved processing large datasets, filtering and validating geographic data, and generating various visualizations and correlations to understand the relationship between environmental factors and lightning activity.

## Project Structure

### 1. Data Acquisition and Preparation

- **`taking_raw_data.py`**: This script processes raw data from zipped text files, extracting and filtering relevant information about lightning occurrences. It outputs a consolidated CSV file with the required data fields.

- **`split_to_month.py`**: This script organizes the filtered lightning data by splitting it into monthly files, making it easier to analyze trends and correlations on a month-by-month basis.

### 2. Geographic Data Handling

- **`create_polygon.py`**: Converts polygon coordinates from a text file into a CSV format, which is later used to define geographic boundaries in the analysis.

- **`my_func.py`**: Contains utility functions to validate and fix geographic polygons and points. It also includes a function to determine if a point is within a specified geographic boundary.

### 3. Data Processing and Filtering

- **`separate_areas.py`**: Filters and categorizes lightning data based on geographic regions (North, Center, South) and removes data points outside of the specified polygon. It also processes pollutant data to focus on specific cities.

- **`demarcation.py`**: Filters and processes data to focus on specific geographic areas, such as Tel Aviv, and validates the lightning data within these boundaries.

- **`all_data.py`**: Processes the complete dataset, filtering lightning points that fall within specific geographic boundaries.

### 4. Visualization

- **`timeline_map.py`**: Generates interactive maps showing lightning density and intensity over time. It creates a timeline animation of lightning occurrences across Israel.

- **`graph_func.py`**: Contains various functions used across the project for plotting and analyzing lightning data, including visualizations for land vs sea lightning occurrences, average power, and hourly distributions.

- **`graph.py`**: Utilizes the functions in `graph_func.py` to generate specific plots and analyses based on the prepared data.

- **`in_land.py`**: Visualizes the distribution of lightning occurrences specifically over land within Israel's territory.

- **`land&sea_lightnings.py`**: Visualizes the distribution and intensity of lightning occurrences over land versus sea across Israel.

- **`land_lightnings.py`**: Analyzes the distribution of lightning occurrences specifically over land, categorizing them by geographic zones (North, Center, South).

### 5. Correlation Analysis

- **`min-max_correlation_with_shift_option.py`**: Analyzes the correlation between lightning activity and pollutant levels with an optional time shift. It generates visualizations to display these correlations.

- **`heat_map.py`**: Generates a comprehensive correlation heatmap between lightning occurrences and pollutant levels across different regions.

- **`area_correlations_graphs.py`**: Produces graphs showing the correlation between lightning activity and pollutants for different regions, highlighting trends over different hours of the day.

- **`min-max_graphs.py`**: Generates graphs comparing the min-max normalized values of lightning peak currents and pollutant levels across different regions.
