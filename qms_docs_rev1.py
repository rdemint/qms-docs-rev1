import os
import sys 

class DocRevManager(object):
    def __init__(self):
        self.top_dir = "C:\\Users\\raine\\Documents\\Backup\\Active QMS Documents"
        self.rev_str = " Rev1.docx"
        self.delete_file_types = ("pdf",)
        self.renamed_files = []
        self.errors = []
        self.skipped_files = []
        self.deleted_files = []
        self.count = 0
        self.main()

    def reset_config(self):
        self.count = 0
        self.renamed_files = []
        self.skipped_files = []
        self.deleted_files = []
        self.errors = []

    def new_line(self):
        print("\n")
        print("\n")

    def replace_name(self, name_str):
        if name_str.rsplit(".")[0][-1] == "1":
            self.skipped_files.append(name_str)
            return None 
        else:
            lstr = name_str.split(' Rev')[0]
            return lstr + self.rev_str

    def handle_doc(self, name_str, f_path, process=False):
        file_type = name_str.rsplit(".")[1].lower()
        replaced = False
        
        if file_type in self.delete_file_types:
            self.deleted_files.append(name_str)
            if process==True:
                os.remove(os.path.join(name_str, f_path))
        else:
            result = self.replace_name(name_str)
            if result is not None:
                self.renamed_files.append(result)
                if process==True:
                    try:
                        os.rename(os.path.join(f_path, name_str), os.path.join(f_path, new_name))
                    except FileExistsError:
                        self.skipped_files.append(name_str)
                    except Exception as e:
                        print(e)

    def loop_dirs(self, process=False):
        self.reset_config()
        for sub_dir in os.listdir(self.top_dir):
            sub_dir_path = os.path.join(self.top_dir,sub_dir)
            for file_name in os.listdir(sub_dir_path):
                self.handle_doc(file_name, sub_dir_path)
                self.count+=1

    def set_top_dir(self):
        self.new_line()
        print('Please input the top level directory or press "d" for the default.')
        top_dir = input()
        if top_dir == "d":
            pass
        else:
            self.top_dir = top_dir

    def log_results(self):
        self.new_line()
        total_handled = len(self.renamed_files) + len(self.deleted_files)
        print("{} total file names modified to {}".format(len(self.renamed_files), self.rev_str))
        print("{} files deleted".format(len(self.deleted_files)))
        print("{} files skipped".format(len(self.skipped_files)))
        if len(self.renamed_files) + len(self.deleted_files) + len(self.skipped_files) == self.count:
            print("OK. All files handled.")
        else: 
            print("Some files were not handles or deleted correctly")

    def confirm(self):
        self.new_line()
        total_handled = len(self.renamed_files) + len(self.deleted_files)
        print("{} total files.".format(self.count))
        print("{} total file names to be modified to {}.".format(len(self.renamed_files), self.rev_str))
        print("{} files names will be skipped".format(len(self.skipped_files)))
        self.new_line()
        print("The final file names will be the following:")
        for name in self.renamed_files:
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