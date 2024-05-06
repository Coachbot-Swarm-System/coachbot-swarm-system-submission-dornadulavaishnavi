import shutil
import os

# shutil.copyfile("/Vaish_Flocking/init_poses.csv", "init_poses.csv")
with open('Vaish_Flocking/init_pose.csv', 'r') as f:
    init_pose_file = f.read()
# print("initial file loaded")
print("Copied")