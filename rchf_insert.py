import os
import argparse

# --------------------------------------------------------------------------------
# Classes 
# --------------------------------------------------------------------------------

class ConsolePrinter:
    def __init__(self, app_args):
        self.app_args = app_args
    
    def print(self, msg, override_quiet = False):
        if self.app_args.quiet == False or override_quiet == True:
            print(msg)

    def input(self, msg):
        return input(msg)
    
    def prompt_yes_no(self, msg, append_yn_to_msg):
        final_msg = msg + ' [Y/N] ' if append_yn_to_msg else msg
        result = None
        while result == None:
            response = input(final_msg).lower()
            if response == 'y':
                result = True 
            elif response == 'n':
                result = False 
        return result
    
    def pause_until_enter(self):
        msg = "Press \'Enter\' to continue..."
        input(msg)

# --------------------------------------------------------------------------------
# Utility functions 
# --------------------------------------------------------------------------------

def get_files_in_dir(dir_path_str, only_names = False):
    result = []
    dir = os.fsencode(dir_path_str)
    for file in os.listdir(dir):
        if only_names:
            result.append(file)     
        else:
            result.append(os.path.join(dir, file))     
    return result

def get_all_invalid_paths(paths):
    result = []
    for path in paths:
       if os.path.exists(path) == False:
           result.append(path)
    return result

# Input:
# - 'fn' -- string of file to append to
# - 'text' -- text to append
# - 'prefix'/'postfix' -- where to append. Both can be set to True at once
def append_fn_text(fn, text, prefix, postfix):
    no_ext, ext = os.path.splitext(os.fsencode(fn))
    result = text if prefix else ''
    result += os.fsdecode(no_ext)
    if postfix:
        result += text
    result += os.fsdecode(ext)
    return result

# --------------------------------------------------------------------------------
# Main  
# --------------------------------------------------------------------------------

def run_main_app(app_args, printer):
    to_insert = str(app_args.inserted_string)
        
    if app_args.preview > 0:
        max_preview_items = min(int(app_args.preview), len(app_args.target_paths))
        printer.print(f'Preview of first {max_preview_items} incoming changes:', True)
        for i in range(0, max_preview_items):
            file = app_args.target_paths[i]
            new_fn = append_fn_text(file, to_insert, app_args.start, app_args.end)
            printer.print('\t\'' + file + '\'  ->  \'' + new_fn, True)
        printer.print('\t ...', True)
        if printer.prompt_yes_no('Proceed?', True) == False:
            return

    for file in app_args.target_paths:
        new_fn = append_fn_text(file, to_insert, app_args.start, app_args.end)
        old_path = os.fsencode(file)
        new_path = os.fsencode(new_fn)
        os.rename(old_path, new_path)


# TODO: Features:
# - input_parser.add_argument("-tas", "--treat_as_dirs", action="store_true")
# - input_parser.add_argument("-rof", "--rename_only_files", action="store_true")
if __name__ == '__main__':
    input_parser = argparse.ArgumentParser()
    input_parser.add_argument("target_paths", type=str, nargs='+')
    input_parser.add_argument("-i", "--inserted_string", action='store', required=True)
    input_parser.add_argument("-s", "--start", action="store_true")
    input_parser.add_argument("-e", "--end", action="store_true")
    input_parser.add_argument("-q", "--quiet", action="store_true")
    input_parser.add_argument("-p", "--preview", action="store", type=int, default=0, required=False)
    input_parser.add_argument("-poe", "--pause_on_exit", action="store_true")
    args = input_parser.parse_args()

    if args.start == False and args.end == False:
        print('Specify at least one of:  \'--start\', \'--end\'')
        raise SystemExit(1)

    invalid_paths = get_all_invalid_paths(args.target_paths)
    if len(invalid_paths) > 0:
        print('[Error] following paths are invalid:')
        for p in invalid_paths:
            print('\t' + p)
        raise SystemExit(2)

    printer = ConsolePrinter(args)
    run_main_app(args, printer)
    
    printer.print('Done.')
    if args.pause_on_exit == True:
        printer.pause_until_enter()