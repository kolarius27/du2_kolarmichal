from turtle import speed, penup, pendown, setpos, seth, forward, dot, pencolor, screensize, exitonclick, setworldcoordinates, colormode, pensize, tracer
from random import randint

# new list "final_features"
final_features = []


# function that returns x and y max/min values (bounding box)
def quadtree_bbox(points):
    # getting lists of x and y coordinates
    points_x = [pointx[0] for pointx in points]
    points_y = [pointy[1] for pointy in points]
    # calculation of max/min
    x_min = min(points_x)
    x_max = max(points_x)
    y_min = min(points_y)
    y_max = max(points_y)
    return x_min, x_max, y_min, y_max


# recursive function clustering points
def quadtree_clustering(features, x_min, x_max, y_min, y_max):
    print("Points count: ", len(features))

    # 4 new lists created symbolizing 4 quadrants
    NW = []  # north-west quadrant
    NE = []  # north-east quadrant
    SW = []  # south-west quadrant
    SE = []  # south-east quadrant

    # if list has less than 50 points, goes to "else"
    # and appends points with new "cluster_ID" number to "final_features"
    if len(features) > 50:
        x_mid = (x_max + x_min) / 2
        y_mid = (y_max + y_min) / 2
        # appending points with new cluster ids (based on X/Y values compared to mid values) to 4 quadrants NW/NE/SW/SE
        for feat in features:
            x, y = feat["geometry"]["coordinates"]
            if x < x_mid and y > y_mid:
                feat["properties"]["cluster_ID"] += ".1"
                NW.append(feat)
            elif x > x_mid and y > y_mid:
                feat["properties"]["cluster_ID"] += ".2"
                NE.append(feat)
            elif x < x_mid and y < y_mid:
                feat["properties"]["cluster_ID"] += ".3"
                SW.append(feat)
            else:
                feat["properties"]["cluster_ID"] += ".4"
                SE.append(feat)

        print("NW: ", NW)
        print("NE: ", NE)
        print("SW: ", SW)
        print("NE: ", NE)

        # recursion of the function with new 4 quadrant lists as attributes and corresponding new bounding box
        quadtree_clustering(NW, x_min, x_mid, y_mid, y_max)
        quadtree_clustering(NE, x_mid, x_max, y_mid, y_max)
        quadtree_clustering(SW, x_min, x_mid, y_min, y_mid)
        quadtree_clustering(SE, x_mid, x_max, y_min, y_mid)
    else:
        for feat in features:
            final_features.append(feat)
    return final_features


# quadtree main function that returns features with new property attribute "cluster_ID"
def quadtree(features):

    # creates list of xy coordinates
    points = []
    for feat in features:
        coordinates = feat["geometry"]["coordinates"]
        points.append(coordinates)

    # bounding box
    x_min, x_max, y_min, y_max = quadtree_bbox(points)

    return quadtree_clustering(features, x_min, x_max, y_min, y_max)


# draws adress points
def quadtree_turtle_points(xpoints, ypoints, dot_size):
    tracer(len(xpoints))
    colormode(255)
    # generates random color of dots
    randcolor = (randint(0, 255), randint(0, 225), randint(0, 255))
    for k in range(len(xpoints)):
        pencolor(randcolor)
        penup()
        setpos(xpoints[k], ypoints[k])
        pendown()
        dot(dot_size)
        penup()


# recursive function doing all the drawing business
def quadtree_turtle_draw(points, x_min, x_max, y_min, y_max, line, dot_size):
    # 2 new lists for x and y coordinates
    xpoints = [pointx[0] for pointx in points]
    ypoints = [pointy[1] for pointy in points]

    # draws adress points
    quadtree_turtle_points(xpoints, ypoints, dot_size)

    # 4 new lists symbolizing 4 quadrants
    NW = []  # north-west quadrant
    NE = []  # north-east quadrant
    SW = []  # south-west quadrant
    SE = []  # south-east quadrant

    # calculation of middle x/y coordinates of bounding box
    x_mid = (x_max + x_min) / 2
    y_mid = (y_max + y_min) / 2
    # reduces line width by half
    line = line / 2

    # if points length is bigger than 50, bounding box is sliced to 4 quadrants
    if len(points) > 50:
        # appending points (based on X/Y values compared to mid values) to 4 quadrants NW/NE/SW/SE
        for pnt in points:
            x, y = pnt
            if x < x_mid and y > y_mid:
                NW.append(pnt)
            elif x > x_mid and y > y_mid:
                NE.append(pnt)
            elif x < x_mid and y < y_mid:
                SW.append(pnt)
            else:
                SE.append(pnt)

        # draws slicing bounding box to 4 quadrants
        pencolor("red")
        pensize(line)
        speed(1)
        setpos(x_min, y_mid)
        pendown()
        setpos(x_max, y_mid)
        penup()
        setpos(x_mid, y_min)
        pendown()
        setpos(x_mid, y_max)
        penup()

        # recursion of the function with new 4 quadrant lists as attributes
        quadtree_turtle_draw(NW, x_min, x_mid, y_mid, y_max, line, dot_size)
        quadtree_turtle_draw(NE, x_mid, x_max, y_mid, y_max, line, dot_size)
        quadtree_turtle_draw(SW, x_min, x_mid, y_min, y_mid, line, dot_size)
        quadtree_turtle_draw(SE, x_mid, x_max, y_min, y_mid, line, dot_size)


# main quadtree drawing function
def quadtree_turtle(features, resolution, line, dot_size):
    # sets screensize to square with side = resolution + 100
    screensize(resolution+100, resolution+100)

    # multiple new lists are needed
    points = []
    points_x = []
    points_y = []
    points_scaled = []
    points_x_scaled = []
    points_y_scaled = []

    # appends values to lists of coordinates
    for feat in features:
        coordinates = feat["geometry"]["coordinates"]
        points.append(coordinates)
        points_x.append(coordinates[0])
        points_y.append(coordinates[1])

    # calculates mid points
    x_mid = (max(points_x) + min(points_x)) / 2
    y_mid = (max(points_y) + min(points_y)) / 2

    # rescales points to fit in square with side = resolution, mid point coordinates are [0,0]
    # appends rescaled coordinates to new lists
    for pnt in points:
        pointx = (resolution/2)*(pnt[0] - x_mid) / (max(points_x) - x_mid)
        pointy = (resolution/2)*(pnt[1] - y_mid) / (max(points_y) - y_mid)
        coordinates_scaled = (pointx, pointy)
        points_scaled.append(coordinates_scaled)
        points_x_scaled.append(coordinates_scaled[0])
        points_y_scaled.append(coordinates_scaled[1])

    # calculation of bounding box
    x_max = max(points_x_scaled)
    y_max = max(points_y_scaled)
    x_min = min(points_x_scaled)
    y_min = min(points_y_scaled)

    # drawing of bounding box
    pencolor("red")
    pensize(line)
    penup()
    setpos(x_min, y_min)
    pendown()
    setpos(x_min, y_max)
    setpos(x_max, y_max)
    setpos(x_max, y_min)
    setpos(x_min, y_min)
    penup()

    # drawing quadtree
    quadtree_turtle_draw(points_scaled, x_min, x_max, y_min, y_max, line, dot_size)

    exitonclick()