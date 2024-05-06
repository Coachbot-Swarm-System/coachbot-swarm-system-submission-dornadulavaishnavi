import shutil
import os

init_file = open('init_pose.csv', 'w')
# shutil.copyfile("/Vaish_Flocking/init_pose.csv", "init_poses.csv")
with open('Vaish_Flocking/init_pose.csv', 'r') as f:
    init_pose_file = f.read()
    init_file.write(init_pose_file)
# print("initial file loaded")
init_file.close()
print("Copied")