import glob
import shutil
import os
import sys


def move_file_to_folder(src_file, dst_folder):
    """指定のファイルを、指定のフォルダーへ移動します"""

    # basename
    try:
        basename = os.path.basename(src_file)
    except:
        print(
            f"[ERROR] move_file_to_folder.py move_file_to_folder: src_file={src_file} except={sys.exc_info()[0]}")
        raise

    # `.` や `*` や `/` がここを通ってきてないか、最終チェックしておきます
    _stem, extention = os.path.splitext(basename)
    if not (extention.lower() in ['.kif', '.kifu', '.json', '.toml']):
        print(
            f"[ERROR] move_file_to_folder.py move_file_to_folder: record file move fail. move_file_to_folder_by_pattern_list.py src_file=[{src_file}]")
        return

    dst_file = os.path.join(dst_folder, basename)
    shutil.move(src_file, dst_file)
