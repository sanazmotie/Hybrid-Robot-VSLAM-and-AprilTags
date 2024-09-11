import pickle
import numpy as np
import msg_to_location
import matplotlib.pyplot as plt

# Load the dictionary containing tag locations
# with open('/home/nargess/Documents/GitHub/VSLAM/seen_tags.pkl', 'rb') as f:
#     my_dict = pickle.load(f)

# Get the robot path locations
X, Y = msg_to_location.robot_path_locations("/home/nargess/Documents/GitHub/VSLAM/SLAM/test7_khube/map.msg")

# print(my_dict)

# Extract tag locations from the dictionary
# tag_x = [coords[0] for coords in my_dict.values()]
# tag_y = [coords[1] for coords in my_dict.values()]

tag_x = [136, 273]
tag_y = [-104, 52]


# Plot the tag locations in red
plt.scatter(tag_y, tag_x, color='red', label='Tag Locations')

# Plot the robot path with a gradient of blue
# Normalize the values to get a color gradient
norm = plt.Normalize(0, len(X))
colors = plt.cm.Blues(norm(range(len(X))))

for i in range(len(X) - 1):
    plt.plot([3.2 * y for y in Y[i:i+2]], [2.23 * x for x in X[i:i+2]], color=colors[i])

# plt.plot(-104, 136, color='red', linewidth=7.0)
# plt.plot(52, 273, color='red')

# Add labels and a legend
plt.xlabel('Y coordinate')
plt.ylabel('X coordinate')
plt.title('Tag Locations and Robot Path')
plt.legend()

# Display the plot
plt.show()