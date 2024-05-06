import shutil
import os

shutil.copyfile(os.getcwd()+"/Vaish_Flocking/init_poses.csv", "init_poses.csv")
print("Copied")