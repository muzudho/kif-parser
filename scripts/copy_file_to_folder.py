import shutil
import os
import inspect
from scripts.change_place import change_place


def copy_file_to_folder(input_file, output_folder, debug=False):

    copy_file = change_place(output_folder, input_file)

    if input_file == copy_file:
        raise ValueError(f"[FATAL] Copy same. [{input_file}]")

    if debug:
        print(f"[DEBUG] {os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}: Copy from [{input_file}] to [{copy_file}]")

    shutil.copyfile(input_file, copy_file)
