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
        dot(10, randcolor)
        penup()


def quadtree_turtle_draw(points):
    xpoints = [pointx[0] for pointx in points]
    ypoints = [pointy[1] for pointy in points]

    quadtree_turtle_points(xpoints, ypoints)

    x_min = min(xpoints)
    x_max = max(xpoints)
    y_min = min(ypoints)
    y_max = max(ypoints)

    pencolor("red")
    penup()
    setpos(x_min, y_min)
    pendown()
    setpos(x_min, y_max)
    setpos(x_max, y_max)
    setpos(x_max, y_min)
    penup()

    NW = []  # north-west quadrant
    NE = []  # north-east quadrant
    SW = []  # south-west quadrant
    SE = []  # south-east quadrant

    if len(points) > 50:
        x_mid = (x_min + x_max) / 2
        y_mid = (y_min + y_max) / 2
        # appending points with new cluster ids (based on X/Y values compared to mid values) to 4 quadrants NW/NE/SW/SE
        for pnt in points:
            x, y = points
            if x < x_mid and y > y_mid:
                NW.append(pnt)
            elif x > x_mid and y > y_mid:
                NE.append(pnt)
            elif x < x_mid and y < y_mid:
                SW.append(pnt)
            else:
                SE.append(pnt)

    # recursion of the function with new 4 quadrant lists as attributes
    quadtree_turtle_draw(NW)
    quadtree_turtle_draw(NE)
    quadtree_turtle_draw(SW)
    quadtree_turtle_draw(SE)


def quadtree_turtle(features):
    points = []
    for feat in features:
        coordinates = feat["geometry"]["coordinates"]
        points.append(coordinates)

    x_mid, y_mid = quadtree_mids(features)

    points_x = [pointx[0] - x_mid for pointx in points]
    points_y = [pointy[1] - y_mid for pointy in points]
    x_min = min(points_x)
    x_max = max(points_x)
    y_min = min(points_y)
    y_max = max(points_y)

    #setworldcoordinates(x_min, y_min, x_max, y_max)

    quadtree_turtle_draw(points)

    exitonclick()







