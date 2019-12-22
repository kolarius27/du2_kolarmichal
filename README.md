# Clustering adress points

## What does this code do?

This code opens a GeoJSON file and runs quadtree algorithm over the loaded file. The algorithm divides adress points to clusters with less than 50 points. It generates bounding box, which is repeatedly sliced to 4 quadrants if the length of points list is bigger than 50. Thanks to turtle.py run of algorithm is reconstructed. The output is a GeoJSON file with new property attribute "cluster_ID".

************

## How does this code work?

This code consists of two python files. "quadtree.py" contains functions to run the quad tree algorithm and to draw the algorithm. "split.py" loads a GeoJSON file named "input.geojson", calls functions from "quadtree.py" and exports new GeoJSON file "output.geojson".

Quad tree algorithm itself is represented by three functions: "quadtree", "quadtree_bbox" and "quadtree_clustering". Function "quadtree" has one argument: features. This argument is a list of features from GeoJSON file. Before using this function new atribute is added to "properties" (key "cluster_ID", value "1"). Function "quadtree_bbox", which is called within the main fuction, generates values defining tops of bounding box: x_min, x_max, y_min and y_max. Than "quadtree_clustering" function is called.

"quadtree_clustering" has five arguments: features, x_min, x_max, y_min, y_max. This function is testing length of list "features". If there is more than 50 points, the list is divided to four new lists: NW, NE, SW and SE (NW = North-West quadrant, NE = North-East quadrant, SW = South-West quadrant, SE = South-East quadrant). X and Y coordinates of point are compared to mid X and Y coordinates. Then point is appended to corresponding list and value of "cluster_ID" is edited (NW = 1.1, NE = 1.2, SW = 1.3, SE = 1.4). After that function calls itself with new 4 lists as arguments and correct tops of bounding box (f. e. quadtree_clustering(NW, x_min, x_mid, y_mid, y_max)). When the length of "features" argument is smaller that 50, values are appended to new list called "final_features". This list is used to export output GeoJSON file.

Drawing quad tree algorithm consists of three functions: "quadtree_turtle_points", "quadtree_turtle_draw" and "quadtree_turtle". "quadtree_turtle" rescales point coordinates to fit pre-defined square by argument "resolution". Bounding box is then calculated and drawn. In the end "quadtree_turtle_draw" is called. 

Within "quadtree_turtle_draw" function "quadtree_turtle point" is called. It generates random color and draws dots symbolizing address points, so every cluster has different color thanks to it. It is possible to change dot size depending on length of point list and "resolution" argument. After that number of points in list is tested. If it is lower than 50, points are divided to 4 new lists as in the main quadtree function, bounding box is sliced to 4 quadrants and function calls itself with 4 new lists as arguments. Line size is editable as well, with every recusion the size is reduced by half. 

### Turtle graphics: 
![alt text](https://github.com/kolarius27/du2_kolarmichal/blob/master/test_draw.png)

### QGIS: 
![alt text](https://github.com/kolarius27/du2_kolarmichal/blob/master/test_qgis.png)
