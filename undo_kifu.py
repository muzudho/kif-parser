import glob
import shutil
import os
import sys


def undo_kifu(kifu_file, output_folder='temporary/kifu'):
    # basename
    try:
        basename = os.path.basename(kifu_file)
    except:
        print(f"Error: kifu_file={kifu_file} except={sys.exc_info()[0]}")
        raise

    _stem, extention = os.path.splitext(basename)
    if extention.lower() != '.kifu':
        return None

    # kifuフォルダーへ移動します
    undone_kifu_file = shutil.move(
        kifu_file, os.path.join(output_folder, basename))
    return undone_kifu_file


def main():
    # KIFUファイル一覧
    kifu_files = glob.glob("./temporary/kifu-done/*.kifu")
    for kifu_file in kifu_files:
        _undone_kifu_file = undo_kifu(kifu_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
