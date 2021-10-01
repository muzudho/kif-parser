import glob
import shutil
import os


def undo_kifu(kifu_file, output_folder='temporary/kifu_d'):
    # basename
    basename = os.path.basename(kifu_file)
    _stem, extention = os.path.splitext(basename)
    if extention.lower() != '.kifu':
        return None

    # kifuフォルダーへ移動します
    undone_kifu_file = shutil.move(
        kifu_file, os.path.join(output_folder, basename))
    return undone_kifu_file


def main():
    # KIFUファイル一覧
    kifu_files = glob.glob("./kifu-done/*.kifu")
    for kifu_file in kifu_files:
        _undone_kifu_file = undo_kifu(kifu_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
