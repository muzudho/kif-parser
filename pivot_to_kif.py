import glob
from pivot_to_kifu import convert_pivot_to_kifu
from kifu_to_kif import convert_kifu_to_kif
from kif_to_kifu import copy_kif_from_input
import argparse
from remove_all_temporary import remove_all_temporary
from remove_all_output import remove_all_output


def convert_pivot_to_kif(pivotFile, output_folder='temporary/kif'):
    kifuFile, donePivotFile = convert_pivot_to_kifu(pivotFile)
    if kifuFile is None:
        return None, None

    # kifu to kif
    kifFile, _doneKifuFile = convert_kifu_to_kif(
        kifuFile, output_folder=output_folder)
    return kifFile, donePivotFile


def __main(debug=False):
    if not debug:
        # 出力フォルダーを空っぽにします
        remove_all_output()

    copy_kif_from_input()

    # PIVOTファイル一覧
    pivot_files = glob.glob("./temporary/pivot/*.json")
    for pivot_file in pivot_files:
        kif_file, _done_pivot_file = convert_pivot_to_kif(
            pivot_file, output_folder='output')

        if kif_file is None:
            print(f"Parse fail. pivot_file={pivot_file}")

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary()


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    # Description
    parser = argparse.ArgumentParser(
        description='Convert from .json (PIVOT) file to .kif file.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    __main(debug=args.debug)
