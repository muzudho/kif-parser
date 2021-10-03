import shutil
import os
import sys


def copy_test_data_to_input_danger(test_data_file, output_folder):
    # basename
    try:
        basename = os.path.basename(test_data_file)
    except:
        print(
            f"Error: test_data_file={test_data_file} except={sys.exc_info()[0]}")
        raise

    _stem, extention = os.path.splitext(basename)
    if not (extention.lower() in ['.kif', '.kifu', '.json', '.toml']):
        return None

    # output_folderへ移動します
    undone_test_data_file = shutil.copyfile(
        test_data_file, os.path.join(output_folder, basename))
    return undone_test_data_file
