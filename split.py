import json, quadtree

# open GeoJSON
with open('input.geojson', encoding='utf-8', mode='r') as f:
    data = json.load(f)

# new list of features
features = data["features"]

# setting up new attribute "cluster_ID" with base value
for feat in features:
    feat['properties']['cluster_ID'] = "1"

# quadtree
features_new = quadtree.quadtree(features)

# quadtree_turtle(features, resolution, line, dot_size)
# is possible to change 2nd to 4th argument
# resolution = side of a rescaling scale (recommended values: 300-1000), depends on points length
# line = size of bounding box line, is reduced by half with every recursion
# dot_size = size of dot symbolizing address point (recommended values: 3-10), depends on points length and resolution
quadtree.quadtree_turtle(features, 700, 10, 5)

# export preparation
data_NEW = {"type": "FeatureCollection"}
data_NEW["features"] = features_new

# new GeoJSON
with open('output.geojson', encoding='utf-8', mode='w') as f:
    json.dump(data_NEW, f, indent=2, ensure_ascii=False)