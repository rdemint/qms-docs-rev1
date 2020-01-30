import os
import sys 

class DocRevManager(object):
    def __init__(self):
        self.top_dir = "C:\\Users\\raine\\Documents\\Backup\\Active QMS Documents"
        self.rev_str = " Rev1"
        self.delete_file_types = ("pdf",)
        self.target_files = []
        self.renamed_files = []
        self.errors = []
        self.skipped_files = []
        self.deleted_files = []
        self.count = 0
        self.main()

    def reset_config(self):
        self.target_files = []
        self.count = 0
        self.renamed_files = []
        self.skipped_files = []
        self.deleted_files = []
        self.errors = []

    def new_line(self):
        print("\n")

    def replace_name(self, name_str, file_type):
        if name_str.rsplit(".")[0][-1] == "1":
            self.skipped_files.append(name_str)
            return None 
        else:
            lstr = name_str.split(' Rev')[0]
            return lstr + self.rev_str + "." + file_type

    def handle_doc(self, name_str, f_path, process=False):
        file_type = name_str.rsplit(".")[1].lower()        
        if file_type in self.delete_file_types:
            self.deleted_files.append(name_str)
            if process==True:
                os.remove(os.path.join(f_path, name_str))
        else:
            result = self.replace_name(name_str, file_type)
            if result is not None:
                self.target_files.append(result)
                if process==True:
                    try:
                        os.rename(os.path.join(f_path, name_str), os.path.join(f_path, result))
                        self.renamed_files.append(result)
                    except FileExistsError:
                        self.skipped_files.append(name_str)
                    except Exception as e:
                        self.errors.append(e)

    def loop_dirs(self, process=False):
        self.reset_config()
        for sub_dir in os.listdir(self.top_dir):
            sub_dir_path = os.path.join(self.top_dir,sub_dir)
            for file_name in os.listdir(sub_dir_path):
                self.handle_doc(file_name, sub_dir_path, process=process)
                self.count+=1

    def set_top_dir(self):
        self.new_line()
        print('Please input the top level directory or press "d" for the default.')
        print('The current default is: {}'.format(self.top_dir))
        top_dir = input()
        if top_dir == "d":
            pass
        else:
            self.top_dir = top_dir

    def log_results(self):
        self.new_line()
        total_handled = len(self.renamed_files) + len(self.deleted_files)
        print("RESULTS:")
        print("{} total file names modified to {}".format(len(self.renamed_files), self.rev_str))
        print("{} files deleted".format(len(self.deleted_files)))
        print("{} files skipped".format(len(self.skipped_files)))
        if len(self.renamed_files) + len(self.deleted_files) + len(self.skipped_files) == self.count:
            print("OK. All files handled.")
        else: 
            print("Some files were not handles or deleted correctly")
        if len(self.errors) != 0:
            print("The following errors occured")
            for e in self.errors:
                print(e)

    def confirm(self):
        self.new_line()
        total_handled = len(self.renamed_files) + len(self.deleted_files)
        print("{} total files.".format(self.count))
        print("{} files names will be skipped".format(len(self.skipped_files)))
        for skipped_file in self.skipped_files:
            print(skipped_file)
        self.new_line()
        print("{} total file names to be modified to {}:".format(len(self.target_files), self.rev_str))
        for name in self.target_files:
            print(name)
        self.new_line()
        print("{} files will be deleted".format(len(self.deleted_files)))
        for deleted in self.deleted_files:
            print(deleted)
        self.new_line()
        answer = input("Please type confirm to make changes.  Other input will exit the program.\n")
        if answer.lower() == "confirm":
            return True
        else:
            return False

    def main(self):
        self.set_top_dir()
        self.loop_dirs()
        if self.confirm():
            self.loop_dirs(process=True)
            self.log_results()
        else:
            sys.exit()

if __name__=="__main__":
    DocRevManager()    