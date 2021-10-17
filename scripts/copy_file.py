import shutil
import os
import inspect


def copy_file(input_file, copy_file, debug=False):

    if input_file == copy_file:
        raise ValueError(f"[FATAL] Copy same. [{input_file}]")

    if debug:
        print(f"[DEBUG] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] Copy from [{input_file}] to [{copy_file}]")

    shutil.copyfile(input_file, copy_file)
