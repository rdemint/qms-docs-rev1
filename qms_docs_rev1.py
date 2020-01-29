def replace_name(name_str):
    lstr = name_str.split(' Rev')[0]
    return lstr + ' Rev1.docx'

def handle_doc(name_str, f_path):
    file_type = name_str.rsplit(".")[1].lower()
    if file_type == "pdf":
#         os.remove(name_str+'\\'+f_path)
        return False, name_str
    else:
        return True, replace_name(name_str)

def loop_dirs(top_dir):
    replaced_names = []
    paths = []
    deleted_files = []
    count = 0
    for sub_dir in os.listdir(top_dir):
        sub_dir_path = top_dir+sub_dir
        for file_name in os.listdir(sub_dir_path):
            replaced, result = handle_doc(file_name, sub_dir_path)
            count += 1
            if replaced == True:
                paths.append(sub_dir_path + "\\" + result)
                replaced_names.append(result)
            else:
                deleted_files.append(result)
    return replaced_names, paths, deleted_files, count

def get_input():
    print('Please input the top level directory.  Files must be placed in subdirectories of this location.')
    top_dir = input()
    #assert that the top_dir is valid

def log_results(replaced_names, full_paths, deleted_names, count):
    print("{} total replaced file names".format(replaced_names.count))
    print("{} pdf files deleted".format(deleted_names))
    print("{} total files expected".format(count))

def main():
    top_dir = get_input()
    replaced_names, paths, deleted_files, count = loop_dirs(top_dir)
    log_results(replaced_names, paths, deleted_files)


if __name__=="__main__":
    main()
    