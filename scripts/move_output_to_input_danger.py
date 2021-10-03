import shutil
import os
import sys


def move_output_to_input_danger(output_file, output_folder):
    # basename
    try:
        basename = os.path.basename(output_file)
    except:
        print(f"Error: output_file={output_file} except={sys.exc_info()[0]}")
        raise

    _stem, extention = os.path.splitext(basename)
    if not (extention.lower() in ['.kif', '.kifu', '.json', '.toml']):
        return None

    # output_folderへ移動します
    undone_input_file = shutil.move(
        output_file, os.path.join(output_folder, basename))
    return undone_input_file
