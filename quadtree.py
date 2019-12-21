from turtle import speed, penup, pendown, setpos, seth, forward, dot, pencolor, screensize, exitonclick, setworldcoordinates
from random import randint

# new list "final_features"
final_features = []

# function that returns x and y mid values
def quadtree_mids(features):
    #new list of coordinates
    points = []
    for feat in features:
        coordinates = feat["geometry"]["coordinates"]
        points.append(coordinates)
    # getting lists of x and y coordinates
    points_x = [pointx[0] for pointx in points]
    points_y = [pointy[1] for pointy in points]
    # calculation of mids
    x_min = min(points_x)
    x_max = max(points_x)
    y_min = min(points_y)
    y_max = max(points_y)
    x_mid = (x_max + x_min) / 2
    y_mid = (y_max + y_min) / 2
    return x_mid, y_mid


# quadtree main function
def quadtree(features):
    print("Points count: ", len(features))

    # setting up 4 new lists
    NW = []  # north-west quadrant
    NE = []  # north-east quadrant
    SW = []  # south-west quadrant
    SE = []  # south-east quadrant

    # if list has less than 50 points, goes to "else" and append points with new "cluster_ID" number to "final_features"
    if len(features) > 50:
        x_mid, y_mid = quadtree_mids(features)
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
        quadtree(NW)
        quadtree(NE)
        quadtree(SW)
        quadtree(SE)
    else:
        for feat in features:
            final_features.append(feat)
    print(final_features)
    return final_features


def quadtree_turtle_points(xpoints, ypoints):
    randcolor = (randint(0, 255), randint(0, 225), randint(0, 255))
    for k in range(len(xpoints)):
        penup()
        setpos(xpoints[k], ypoints[k])
        pendown()
        dot(10, "blue")
        penup()

#def quad_turtle_square(xmin, xmax, ymin, ymax):


def quadtree_turtle_draw(points, x_min, x_max, y_min, y_max):
    xpoints = [pointx[0] for pointx in points]
    ypoints = [pointy[1] for pointy in points]

    quadtree_turtle_points(xpoints, ypoints)

    pencolor("red")
    penup()
    setpos(x_min, y_min)
    pendown()
    setpos(x_min, y_max)
    setpos(x_max, y_max)
    setpos(x_max, y_min)
    setpos(x_min, y_min)
    penup()

    NW = []  # north-west quadrant
    NE = []  # north-east quadrant
    SW = []  # south-west quadrant
    SE = []  # south-east quadrant

    if len(points) > 50:
        x_mid = (x_max + x_min) / 2
        y_mid = (y_max + y_min) / 2
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
        setpos(x_mid, y_min)
        pendown()
        setpos(x_mid, y_max)
        penup()
        setpos(y_mid, x_min)
        pendown()
        setpos(y_mid, x_max)
        penup()

    # recursion of the function with new 4 quadrant lists as attributes
    quadtree_turtle_draw(NW, x_min, x_mid, y_mid, y_max)
    quadtree_turtle_draw(NE, x_mid, x_max, y_mid, y_max)
    quadtree_turtle_draw(SW, x_min, x_mid, y_min, y_mid)
    quadtree_turtle_draw(SE, x_mid, x_max, y_min, y_mid)


def quadtree_turtle(features, resolution):
    screensize(resolution+100, resolution+100)
    speed(10)
    points = []
    points_x = []
    points_y = []
    points_scaled = []
    points_x_scaled = []
    points_y_scaled = []
    x_mid, y_mid = quadtree_mids(features)
    for feat in features:
        coordinates = feat["geometry"]["coordinates"]
        points.append(coordinates)
        points_x.append(coordinates[0])
        points_y.append(coordinates[1])
    x_max = max(points_x) - x_mid
    y_max = max(points_y) - y_mid
    for pnt in points:
        pointx = (resolution/2)*(pnt[0] - x_mid) / x_max
        pointy = (resolution/2)*(pnt[1] - y_mid) / y_max
        coordinates_scaled = (pointx, pointy)
        points_scaled.append(coordinates_scaled)
        points_x_scaled.append(coordinates_scaled[0])
        points_y_scaled.append(coordinates_scaled[1])
    x_max = max(points_x_scaled)
    y_max = max(points_y_scaled)
    x_min = min(points_x_scaled)
    y_min = min(points_y_scaled)

    quadtree_turtle_draw(points_scaled, x_max, y_max, x_min, y_min)

    exitonclick()







