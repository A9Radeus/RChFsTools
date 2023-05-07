import os
import argparse

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

def get_files_in_dir(dir_path_str, only_names = False):
    result = []
    dir = os.fsencode(dir_path_str)
    for file in os.listdir(dir):
        if only_names:
            result.append(file)     
        else:
            result.append(os.path.join(dir, file))     
    return result

# Takes in os.path ('file'), but returns string
def append_fn_text(file, text, prefix, postfix):
    no_ext, ext = os.path.splitext(file)
    result = text if prefix else ''
    result += os.fsdecode(no_ext)
    if postfix:
        result += text
    result += os.fsdecode(ext)
    return result

def run_main_app(app_args):
    input_path_str = str(app_args.dir_path)
    input_path = os.fsencode(input_path_str)
    to_insert = str(app_args.str_to_insert)
    files_in_dir = get_files_in_dir(input_path_str, True)

    if len(files_in_dir) == 0:
        printer.print('No files in given directory.')
        return

    if app_args.preview > 0:
        max_preview_items = min(int(app_args.preview), len(files_in_dir))
        printer.print(f'Preview of first {max_preview_items} incoming changes:', True)
        for i in range(0, max_preview_items):
            file = files_in_dir[i]
            new_fn = append_fn_text(file, to_insert, app_args.start, app_args.end)
            printer.print('\t\'' + os.fsdecode(file) + '\'  ->  \'' + new_fn, True)
        printer.print('\t ...', True)
        if printer.prompt_yes_no('Proceed?', True) == False:
            return

    for file in files_in_dir:
        new_fn = append_fn_text(file, to_insert, app_args.start, app_args.end)
        old_path = os.path.join(input_path, file)
        new_path = os.path.join(input_path, os.fsencode(new_fn))
        os.rename(old_path, new_path)

if __name__ == '__main__':
    input_parser = argparse.ArgumentParser()
    input_parser.add_argument("dir_path")
    input_parser.add_argument("str_to_insert")
    input_parser.add_argument("-s", "--start", action="store_true")
    input_parser.add_argument("-e", "--end", action="store_true")
    input_parser.add_argument("-q", "--quiet", action="store_true")
    input_parser.add_argument("-p", "--preview", action="store", type=int, default=0, required=False)
    input_parser.add_argument("-poe", "--pause_on_exit", action="store_true")
    args = input_parser.parse_args()

    if args.start == False and args.end == False:
        print('Specify at least one of:  \'--start\', \'--end\'')
        raise SystemExit(1)

    printer = ConsolePrinter(args)
    
    run_main_app(args)
    
    printer.print('Done.')
    if args.pause_on_exit == True:
        printer.pause_until_enter()