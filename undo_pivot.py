import glob
import shutil
import os


def undo_pivot(pivot_file, output_folder='temporary/pivot_d'):
    # basename
    basename = os.path.basename(pivot_file)
    _stem, extention = os.path.splitext(basename)
    if extention.lower() != '.json':
        return None

    # pivotフォルダーへ移動します
    undone_pivot_file = shutil.move(
        pivot_file, os.path.join(output_folder, basename))
    return undone_pivot_file


def main():
    # PIVOTファイル一覧
    pivot_files = glob.glob("./temporary/pivot-done_d/*.json")
    for pivot_file in pivot_files:
        _undone_pivot_file = undo_pivot(pivot_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
