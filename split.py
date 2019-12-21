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
quadtree.quadtree_turtle(features, 700, 10, 5)

# export preparation
data_NEW = {"type": "FeatureCollection"}
data_NEW["features"] = features_new

# new GeoJSON
with open('output.geojson', encoding='utf-8', mode='w') as f:
    json.dump(data_NEW, f, indent=2, ensure_ascii=False)