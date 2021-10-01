import glob
from pivot_to_kifu import convert_pivot_to_kifu
from kifu_to_kif import convert_kifu_to_kif
from kif_to_kifu import copy_kif_from_input


def convert_pivot_to_kif(pivotFile, output_folder='temporary/kif_d'):
    kifuFile, donePivotFile = convert_pivot_to_kifu(pivotFile)
    if kifuFile is None:
        return None, None

    # kifu to kif
    kifFile, _doneKifuFile = convert_kifu_to_kif(
        kifuFile, output_folder=output_folder)
    return kifFile, donePivotFile


def main():
    copy_kif_from_input()

    # PIVOTファイル一覧
    pivot_files = glob.glob("./temporary/pivot_d/*.json")
    for pivot_file in pivot_files:
        _kifFile, _donePivotFile = convert_pivot_to_kif(
            pivot_file, output_folder='output')


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
