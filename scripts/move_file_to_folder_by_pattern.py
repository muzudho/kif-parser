import glob
import shutil
import os
import sys


def move_file_to_folder(source_file, destination_folder):
    """指定のファイルを、指定のフォルダーへ移動します"""

    # basename
    try:
        basename = os.path.basename(source_file)
    except:
        print(
            f"Error: source_file={source_file} except={sys.exc_info()[0]}")
        raise

    # `.` や `*` や `/` がここを通ってきてないか、最終チェックしておきます
    _stem, extention = os.path.splitext(basename)
    if not (extention.lower() in ['.kif', '.kifu', '.json', '.toml']):
        print(
            f"Error: record file move fail. move_file_to_folder_by_pattern_list.py source_file=[{source_file}] source_file_pattern=[{source_file_pattern}]")
        return

    destination_file = os.path.join(destination_folder, basename)
    shutil.move(source_file, destination_file)


def move_file_to_folder_by_pattern(source_file_pattern, destination_folder):
    """指定のファイルを、指定のフォルダーへ移動します"""

    # 出力ファイル一覧
    source_file_list = glob.glob(source_file_pattern)
    for source_file in source_file_list:

        # basename
        try:
            basename = os.path.basename(source_file)
        except:
            print(
                f"Error: source_file={source_file} except={sys.exc_info()[0]}")
            raise

        # `.` や `*` や `/` がここを通ってきてないか、最終チェックしておきます
        _stem, extention = os.path.splitext(basename)
        if not (extention.lower() in ['.kif', '.kifu', '.json', '.toml']):
            print(
                f"Error: record file move fail. move_file_to_folder_by_pattern_list.py source_file=[{source_file}] source_file_pattern=[{source_file_pattern}]")
            continue

        destination_file = os.path.join(destination_folder, basename)
        shutil.move(source_file, destination_file)
