import shutil
from scripts.change_place import change_place


def copy_file_to_folder(input_file, output_folder, debug=False):

    copy_file = change_place(output_folder, input_file)

    if input_file == copy_file:
        raise ValueError(f"[FATAL] Copy same. [{input_file}]")

    if debug:
        print(f"[DEBUG] Copy from [{input_file}] to [{copy_file}]")

    shutil.copyfile(input_file, copy_file)
