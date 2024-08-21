import msg_to_location as loc
import math


def get_april_tag_location(tag, X_camera, Y_camera):
    x_tag = tag[1]
    y_tag = tag[2]
    d_tag = tag[3]


    # cc = math.sqrt(x_tag**2 + y_tag**2) #center of the apriltag to center of the frame
    # dx = math.sqrt(d_tag**2 - cc**2)
    X_tag = X_camera + d_tag
    Y_tag = Y_camera + x_tag

    return round(X_tag), round(Y_tag)



