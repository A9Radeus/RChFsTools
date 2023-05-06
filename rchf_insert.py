# TODO: Main features:
# ===========================================================================================================
# [x] Allow both prefixes, suffxies
#       [x] Prefixes
#       [x] Suffixes
# [ ] Use library for handling CLI flags, etc
# [ ] Option (prolly a flag) that gives user a preview of N first files and how they would change if application
#     runs with given arguments
# [ ] Option (prolly a flag): silent mode -- no "Done" at the end, etc
# ===========================================================================================================

import os
import sys

def get_files_in_dir_ext(dir_path_str, allowed_exts):
    result = []
    dir = os.fsencode(dir_path_str)
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        for ext in allowed_exts:
            if filename.endswith(ext):
                result.append(os.path.join(dir, file))
                break
    return result

# TODO: This could be more pythonic
# TODO: Add global/relative path option as well
def get_files_in_dir(dir_path_str, only_names = False):
    result = []
    dir = os.fsencode(dir_path_str)
    for file in os.listdir(dir):
        if only_names:
            result.append(file)     
        else:
            result.append(os.path.join(dir, file))     
    return result

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Wrong number of arguments. Correct syntax: [prog_name] [path_to_target_dir] [text_to_insert] [flags]')
        exit(-1)

    input_path_str = str(sys.argv[1])
    input_path = os.fsencode(input_path_str)

    files_in_dir = get_files_in_dir(input_path_str, True)
    str_paths = [os.fsdecode(p) for p in files_in_dir]

    to_insert = str(sys.argv[2])

    input_insert_prefix = False
    input_insert_postfix = False

    for i in range(3, len(sys.argv)):
        if str(sys.argv[i]) == '-s' or str(sys.argv[i]) == '--start':
            input_insert_prefix = True
        if str(sys.argv[i]) == '-e' or str(sys.argv[i]) == '--end':
            input_insert_postfix = True

    if len(files_in_dir) == 0:
        print('No files in given directory.')
        exit(-2)

    for file in files_in_dir:
        no_ext, ext = os.path.splitext(file)
        
        str_file = ''

        if input_insert_prefix:
            str_file += to_insert
        
        str_file += os.fsdecode(no_ext)

        if input_insert_postfix:
            str_file += to_insert
        
        str_file += os.fsdecode(ext)
            
        old_path = os.path.join(input_path, file)
        new_path = os.path.join(input_path, os.fsencode(str_file))
        os.rename(old_path, new_path)

    print('Done.')