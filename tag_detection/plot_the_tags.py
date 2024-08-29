import pickle

with open('/home/nargess/Documents/GitHub/VSLAM/seen_tags.pkl', 'rb') as f:
    my_dict = pickle.load(f)

print(my_dict)