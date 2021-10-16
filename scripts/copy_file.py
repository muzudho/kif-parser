import shutil


def copy_file(input_file, copy_file, debug=False):

    if input_file == copy_file:
        raise ValueError(f"[FATAL] Copy same. [{input_file}]")

    if debug:
        print(f"[DEBUG] Copy from [{input_file}] to [{copy_file}]")

    shutil.copyfile(input_file, copy_file)
