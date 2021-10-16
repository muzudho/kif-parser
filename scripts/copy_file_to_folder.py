import glob
import shutil
import os
import sys


def copy_file_to_folder(input_file, output_folder):

    # basename
    try:
        basename = os.path.basename(input_file)
    except:
        print(
            f"[ERROR] copy_file_to_folder.py copy_file_to_folder: input_file={input_file} except={sys.exc_info()[0]}")
        raise

    copy_file = os.path.join(output_folder, basename)

    if input_file == copy_file:
        raise ValueError(f"[FATAL] Copy same. [{input_file}]")

    shutil.copyfile(input_file, copy_file)
