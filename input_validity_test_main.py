from check_init_pose_validity import InputFiles
import os

def test_validity():
    print("in testing inputs")
    # navigate to code queue folder
    input_files = InputFiles("Vaish_Flocking")
    print("Files Loaded Correctly:", input_files.files_loaded_correctly, "Valid initial positions given", input_files.init_poses_valid)
    print(input_files.files_loaded_correctly and input_files.init_poses_valid)
    assert input_files.files_loaded_correctly == True and input_files.init_poses_valid == True
    # return input_files.files_loaded_correctly and input_files.init_poses_valid
    # for each folder in code queue?
        # load in folder
        # check validity

test_validity()

# if __name__ == "__main__":
#     asyncio.run(main())