from turtle import speed, penup, pendown, setpos, seth, forward, dot, pencolor, screensize, exitonclick, setworldcoordinates

final_features = []


def quadtree_mids(features):
    points = []
    for feat in features:
        coordinates = feat["geometry"]["coordinates"]
        points.append(coordinates)
    points_x = [pointx[0] for pointx in points]
    points_y = [pointy[1] for pointy in points]
    x_min = min(points_x)
    x_max = max(points_x)
    y_min = min(points_y)
    y_max = max(points_y)
    x_mid = (x_max + x_min) / 2
    y_mid = (y_max + y_min) / 2
    return x_mid, y_mid


def quadtree(features):
    print("Count of points: ", len(features))

    NW = []
    NE = []
    SW = []
    SE = []

    if len(features) > 10:
        x_mid, y_mid = quadtree_mids(features)
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







