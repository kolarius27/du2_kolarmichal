# Clustering adress points

## What does this code do?

This code opens a GeoJSON file and runs quadtree algorithm over the loaded file. The algorithm divides adress points to clusters with less than 50 points. It generates bounding box, which is repeatedly sliced to 4 quadrants if the length of points list is bigger than 50. Thanks to turtle.py run of algorithm is reconstructed. The output is a GeoJSON file with new property attribute "cluster_ID".

************

## How does this code work?

This code 
