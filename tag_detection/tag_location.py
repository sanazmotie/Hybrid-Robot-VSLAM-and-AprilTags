import numpy as np
import msg_to_location as loc


def get_april_tag_location(tag_relative_coordinates, camera_info):
    camera_coordinates = camera_info[0]
    rotation_matrix = camera_info[1]

    tag_coordinates_float = (rotation_matrix @ tag_relative_coordinates) + camera_coordinates
    tag_coordinates_int = np.round(tag_coordinates_float).astype(int)
    # print("inja", rotation_matrix.shape, tag_relative_coordinates[:2], camera_coordinates.shape)

    return tag_coordinates_int

