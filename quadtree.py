from turtle import speed, penup, pendown, setpos, seth, forward, dot, pencolor, screensize, exitonclick, setworldcoordinates, colormode, pensize, tracer
from random import randint

# new list "final_features"
final_features = []


# function that returns x and y max/min values
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


def quadtree_clustering(features, x_min, x_max, y_min, y_max):
    print("Points count: ", len(features))

    NW = []  # north-west quadrant
    NE = []  # north-east quadrant
    SW = []  # south-west quadrant
    SE = []  # south-east quadrant

    # if list has less than 50 points, goes to "else" and append points with new "cluster_ID" number to "final_features"
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

        # recursion of the function with new 4 quadrant lists as attributes
        quadtree_clustering(NW, x_min, x_mid, y_mid, y_max)
        quadtree_clustering(NE, x_mid, x_max, y_mid, y_max)
        quadtree_clustering(SW, x_min, x_mid, y_min, y_mid)
        quadtree_clustering(SE, x_mid, x_max, y_min, y_mid)
    else:
        for feat in features:
            final_features.append(feat)
    return final_features


# quadtree main function
def quadtree(features):
    points = []
    for feat in features:
        coordinates = feat["geometry"]["coordinates"]
        points.append(coordinates)

    x_min, x_max, y_min, y_max = quadtree_bbox(points)

    return quadtree_clustering(features, x_min, x_max, y_min, y_max)

def quadtree_turtle_points(xpoints, ypoints, dot_size):
    tracer(len(xpoints)*6)
    colormode(255)
    randcolor = (randint(0, 255), randint(0, 225), randint(0, 255))
    for k in range(len(xpoints)):
        pencolor(randcolor)
        penup()
        setpos(xpoints[k], ypoints[k])
        pendown()
        dot(dot_size)
        penup()


def quadtree_turtle_draw(points, x_min, x_max, y_min, y_max, line, dot_size):
    xpoints = [pointx[0] for pointx in points]
    ypoints = [pointy[1] for pointy in points]

    quadtree_turtle_points(xpoints, ypoints, dot_size)

    NW = []  # north-west quadrant
    NE = []  # north-east quadrant
    SW = []  # south-west quadrant
    SE = []  # south-east quadrant

    x_mid = (x_max + x_min) / 2
    y_mid = (y_max + y_min) / 2
    line = line / 2

    if len(points) > 100:
        # appending points with new cluster ids (based on X/Y values compared to mid values) to 4 quadrants NW/NE/SW/SE
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


def quadtree_turtle(features, resolution, line, dot_size):
    screensize(resolution+100, resolution+100)

    points = []
    points_x = []
    points_y = []
    points_scaled = []
    points_x_scaled = []
    points_y_scaled = []

    for feat in features:
        coordinates = feat["geometry"]["coordinates"]
        points.append(coordinates)
        points_x.append(coordinates[0])
        points_y.append(coordinates[1])

    x_mid = (max(points_x) + min(points_x)) / 2
    y_mid = (max(points_y) + min(points_y)) / 2

    for pnt in points:
        pointx = (resolution/2)*(pnt[0] - x_mid) / (max(points_x) - x_mid)
        pointy = (resolution/2)*(pnt[1] - y_mid) / (max(points_y) - y_mid)
        coordinates_scaled = (pointx, pointy)
        points_scaled.append(coordinates_scaled)
        points_x_scaled.append(coordinates_scaled[0])
        points_y_scaled.append(coordinates_scaled[1])
    x_max = max(points_x_scaled)
    y_max = max(points_y_scaled)
    x_min = min(points_x_scaled)
    y_min = min(points_y_scaled)

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

    quadtree_turtle_draw(points_scaled, x_min, x_max, y_min, y_max, line, dot_size)

    exitonclick()







