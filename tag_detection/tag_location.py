import msg_to_location as loc
import math


def get_april_tag_location(tag_relative_coordinates, camera_info):
    camera_coordinates = camera_info[0][:2]
    rotation_matrix = camera_info[1]

    tag_coordinates = rotation_matrix @ (tag_relative_coordinates[:2] + camera_coordinates[:2])
    # print("inja", rotation_matrix.shape, tag_relative_coordinates.shape, camera_coordinates.shape)

    return tag_coordinates

