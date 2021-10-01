import glob
import shutil
import os


def undo_kif(kif_file, output_folder='temporary/kif_d'):
    # basename
    basename = os.path.basename(kif_file)
    _stem, extention = os.path.splitext(basename)
    if extention.lower() != '.kif':
        return None

    # kifフォルダーへ移動します
    undone_kif_file = shutil.move(
        kif_file, os.path.join(output_folder, basename))
    return undone_kif_file


def main():
    # KIFファイル一覧
    kif_files = glob.glob("./kif-done/*.kif")
    for kif_file in kif_files:
        _undone_kif_file = undo_kif(kif_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
