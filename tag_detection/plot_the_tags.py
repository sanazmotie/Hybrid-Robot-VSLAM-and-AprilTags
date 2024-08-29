import pickle
import numpy as np
import msg_to_location
import matplotlib.pyplot as plt

# Load the dictionary containing tag locations
with open('/home/nargess/Documents/GitHub/VSLAM/seen_tags.pkl', 'rb') as f:
    my_dict = pickle.load(f)

# Get the robot path locations
X, Y = msg_to_location.robot_path_locations()

print(X, Y)

# Extract tag locations from the dictionary
tag_x = [coords[0] for coords in my_dict.values()]
tag_y = [coords[1] for coords in my_dict.values()]

# Plot the tag locations in red
plt.scatter(tag_x, tag_y, color='red', label='Tag Locations')

# Plot the robot path with a gradient of blue
# Normalize the values to get a color gradient
norm = plt.Normalize(0, len(X))
colors = plt.cm.Blues(norm(range(len(X))))

for i in range(len(X) - 1):
    plt.plot(X[i:i+2], Y[i:i+2], color=colors[i])

# Add labels and a legend
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.title('Tag Locations and Robot Path')
plt.legend()

# Display the plot
plt.show()