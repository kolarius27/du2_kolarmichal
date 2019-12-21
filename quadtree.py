from turtle import speed, penup, pendown, setpos, seth, forward, dot, pencolor, screensize, exitonclick, setworldcoordinates

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



def quadtree_turtle(points):
    points_x = [pointx[0] for pointx in points]
    points_y = [pointy[1] for pointy in points]
    point_x_min = min(points_x)
    point_x_max = max(points_x)
    point_y_min = min(points_y)
    point_y_max = max(points_y)
    print(point_x_min, point_y_min, point_x_max, point_y_max)
    setworldcoordinates(point_x_min, point_y_min, point_x_max, point_y_max)
    for k in range(len(points)):
        penup()
        setpos(points_x[k], points_y[k])
        pendown()
        dot(10, "blue")
        penup()
    exitonclick()







