# TODO: Main features:
# ===========================================================================================================
# [x] Allow both prefixes, suffxies
#       [x] Prefixes
#       [x] Suffixes
# [x] Use library for handling CLI flags, etc
# [ ] Option (prolly a flag) that gives user a preview of N first files and how they would change if application
#     runs with given arguments
# [x] Option (prolly a flag): silent mode -- no "Done" at the end, etc
# ===========================================================================================================

import os
import argparse

class ConsolePrinter:
    def __init__(self, app_args):
        self.app_args = app_args
    
    def cprint(self, msg):
        if self.app_args.quiet == False:
            print(msg)

def get_files_in_dir(dir_path_str, only_names = False):
    result = []
    dir = os.fsencode(dir_path_str)
    for file in os.listdir(dir):
        if only_names:
            result.append(file)     
        else:
            result.append(os.path.join(dir, file))     
    return result

def run_main_app(app_args):
    input_path_str = str(app_args.dir_path)
    input_path = os.fsencode(input_path_str)
    to_insert = str(app_args.str_to_insert)

    files_in_dir = get_files_in_dir(input_path_str, True)

    if len(files_in_dir) == 0:
        printer.cprint('No files in given directory.')
        return

    for file in files_in_dir:
        no_ext, ext = os.path.splitext(file)
        
        str_file = ''

        if app_args.start:
            str_file += to_insert
        
        str_file += os.fsdecode(no_ext)

        if app_args.end:
            str_file += to_insert
        
        str_file += os.fsdecode(ext)
            
        old_path = os.path.join(input_path, file)
        new_path = os.path.join(input_path, os.fsencode(str_file))
        os.rename(old_path, new_path)


if __name__ == '__main__':
    input_parser = argparse.ArgumentParser()
    input_parser.add_argument("dir_path")
    input_parser.add_argument("str_to_insert")
    input_parser.add_argument("-s", "--start", action="store_true")
    input_parser.add_argument("-e", "--end", action="store_true")
    input_parser.add_argument("-q", "--quiet", action="store_true")
    args = input_parser.parse_args()

    if args.start == False and args.end == False:
        print('Specify at least one of:  \'--start\', \'--end\'')
        raise SystemExit(1)

    printer = ConsolePrinter(args)

    run_main_app(args)
    
    printer.cprint('Done.')