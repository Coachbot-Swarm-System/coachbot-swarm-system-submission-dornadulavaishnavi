import math
import numpy as np 
import py_compile

x_lim_pos = 1.0
x_lim_neg = -1.2
y_lim_pos = 2.35
y_lim_neg = -1.4
min_start_dist = 0.25 # 0.3535
max_robots = 50

class InputFiles:
    def __init__(self, path):
        self.path = path
        self.init_pose_file = 0
        self.usr_code_file = 0
        self.valid_init_pose_file_load = self.load_init_pose_file()
        self.valid_usr_code_file_load = self.load_usr_code_file()
        self.files_loaded_correctly = False
        self.folder_name = ""
        self.email = self.load_email()
        if self.valid_init_pose_file_load and self.valid_usr_code_file_load:
            self.init_pose_dict = {}
            self.init_poses_valid = self.check_input_file_validity()
            self.files_loaded_correctly = True
            self.num_robots_requested = len(self.init_pose_dict)

    def load_init_pose_file(self):
        try:
            with open(self.path+'/init_pose.csv', 'r') as f:
                self.init_pose_file = f.read()
            print("initial file loaded")
            return True
        except:
            print("Could not find/open init_pose.csv file")
            return False

    def load_usr_code_file(self):
        # check if usr_code.py compiles using py_compile (https://stackoverflow.com/questions/48547566/check-if-a-python-script-compiles-using-another-python-script)
        try:
            py_compile.compile(self.path+"/usr_code.py", doraise=True)
            print("usr_code.py successfully compiled")
        except:
            print("invalid usr_code.py file, the code was either unable to compile or could not find a file named usr_code.py")
            ret_str = "invalid usr_code.py file, the code was either unable to compile or could not find a file named usr_code.py"
            return_file = open(self.path+"/input_pose_errors.csv", "w")
            return_file.write(ret_str)
            return_file.close()
            return False
        with open(self.path+'/usr_code.py', 'r') as f:
            self.usr_code_file = f.read()
        return True

    def load_email(self):
        emails = []
        local_path = self.path
        try:
            emails_file = open(local_path+"/email.txt", 'r')
        except:
            print("User did not share an email")
            return ["vaishnavidornadula2026@u.northwestern.edu"]
        lines = emails_file.readlines()
        for line in lines:
            line = line.replace("\n","")
            emails.append(line)
            # print(line)
        emails_file.close()
        print("Sending Emails to: " + str(emails))
        return emails
    # -------------------------MAIN FUNCTION -------------------------------
    def check_validity(self, dict_init_pose):
        invalid_flag = True
        to_iterate = dict(dict_init_pose)
        if len(to_iterate) > max_robots:
            print("Requesting too many robots, please limit your script to using " + str(max_robots) + " robots")
            ret_str = "Requesting too many robots, please limit your script to using " + str(max_robots) + " robots"
            return_file = open(self.path+"/input_pose_errors.csv", "w")
            return_file.write(ret_str)
            return_file.close()
            return False
        
        for key in dict_init_pose:
            ret_str = ""
            if self.check_format_validity(dict_init_pose[key]) == False:
                # ret_str = "Format of line is invalid, make sure there are 4 values and all are numerical values (int robot id and float orientation)"
                # print(key,ret_str)
                to_iterate.pop(key)
                # corresponding line in file should have that string
            else:
                to_iterate[key]=[float(to_iterate[key][0]), float(to_iterate[key][1]), float(to_iterate[key][2]), float(to_iterate[key][3])]
                # move output file to write to correct line
        print(to_iterate)
        print("\n")
        
        full_string = ""
        for key in dict_init_pose:
            ret_str = ""
            if key in to_iterate: 
                if self.check_ID_validity(to_iterate[key]) == False:
                    ret_str = "ID is invalid "
                    invalid_flag = False
                if self.check_xy_validity(to_iterate[key]) == False:
                    ret_str += "The x and/or y position is out of bounds "
                    invalid_flag = False
                to_iterate[key][3] = self.modulus_theta(to_iterate[key])
                conflicting_pos = self.check_startdist_validity(key, to_iterate)
                if bool(conflicting_pos) == True:
                    ret_str += "too close to " 
                    for i in range(len(conflicting_pos)):
                        ret_str += str(conflicting_pos[i])
                        ret_str += " "
                    invalid_flag = False
                if ret_str == "":
                    ret_str = str(to_iterate[key])
            else:
                ret_str = "Format of line is invalid, make sure there are 4 values and all are numerical values"
                #skip to next line of file
            full_string += ret_str + "\n"
        # write return string to file
        return_file = open(self.path+"/input_pose_errors.csv", "w")
        return_file.write(full_string)
        return_file.close()
        print(full_string)
        # return true or false indicating if the given input file is valid or not
        return invalid_flag

    # 1. check validity of input format (4 items)
    def check_format_validity(self, line):
        if len(line) != 4:
            return False
        for i in range(len(line)):
            try:
                float(line[i])
            except:
                return False
        return True

    # 2. check ID validity
    def check_ID_validity(self, line):
        # print(line[0])
        if line[0] > 99 or line[0] < 0:
            return False
        if line[0].is_integer() == False:
            return False
        return True

    # 3. check that x and y are within the bounds
    def check_xy_validity(self, line):
        if line[1] < x_lim_neg or line[1] > x_lim_pos:
            return False
        if line[2] < y_lim_neg or line[2] > y_lim_pos:
            return False
        return True

    # 4. modulus the theta by 2*pi
    def modulus_theta(self, line):
        return (line[3] % (2*math.pi))

    # 5. check that the distance between it to the others is greater than 3.535 (2.5**2)
    def check_startdist_validity(self, check_key, dict_pos):
        too_close = []
        check_x = dict_pos[check_key][1]
        check_y = dict_pos[check_key][2]
        for key in dict_pos:
            if key != check_key:
                if (math.sqrt((check_x-dict_pos[key][1])**2 + (check_y-dict_pos[key][2])**2)) < min_start_dist:
                    too_close.append(key)
        # print(too_close)
        return too_close


    def check_input_file_validity(self):
        # print(data)
        new_line_split = self.init_pose_file.split('\n')
        # print("Split by new line: " + str(new_line_split))
        # new_line_split.pop()

        input_pose_dict = {}
        for line in new_line_split:
            if line == '':
                pass
                # print("Empty Line")
            else:
                split_line = line.split(',')
                # print("line: " + str(split_line))
                input_pose_dict[split_line[0]] = []
                for item in range(len(split_line)):
                    input_pose_dict[split_line[0]].append(float(split_line[item])) # = [split_line[1],split_line[2],split_line[3]]

        # print("Starting Input String: " + str(input_pose_dict))

        # return(check_validity(input_pose_dict))
        if self.check_validity(input_pose_dict):
            self.init_pose_dict = input_pose_dict
            return True
        else:
            return False

    # if __name__=="__main__":
    #     main()