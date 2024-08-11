from shapely.validation import explain_validity
from shapely.geometry import Polygon, Point

def validate_polygon(polygon):
    if not polygon.is_valid:
        print("Invalid polygon detected. Attempting to fix...")
        explanation = explain_validity(polygon)
        print("Explanation:", explanation)
        # Attempt to fix the invalid polygon
        fixed_polygon = polygon.buffer(0)
        if fixed_polygon.is_valid:
            print("Polygon fixed successfully.")
            return fixed_polygon
        else:
            print("Unable to fix the polygon. Please check the data.")
            return None
    else:
        print("Polygon is valid.")
        return polygon

# Function to validate and fix points
def validate_points(points):
    validated_points = []
    for point in points:
        shapely_point = Point(point)
        if not shapely_point.is_valid:
            print("Invalid point detected:", point)
            # You can choose to handle invalid points as per your requirement
            # For example, skip invalid points or attempt to fix them
        else:
            validated_points.append(point)
    return validated_points

#Function to check if a point (latitude, longitude) is within the territory
def is_inside_territory(point, territory_polygon):
    point = Point(point)
    return territory_polygon.contains(point)
