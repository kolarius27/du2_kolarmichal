# open GeoJSON
# cluster points with quadtree
# if cluster has more than 50 points, quadtree
# ad cluster_id
# draw algorithm
# ad extra algorithms
import json, quadtree

with open('input.geojson', encoding='utf-8', mode='r') as f:
    data = json.load(f)


features = data["features"]
for feat in features:
    feat['properties']['cluster_ID'] = "1"

features_test = features
features_new = quadtree.quadtree(features_test)

data_NEW = {"type": "FeatureCollection"}
data_NEW["features"] = features_new


with open('output.geojson', encoding='utf-8', mode='w') as f:
    json.dump(data_NEW, f, indent=2, ensure_ascii=False)