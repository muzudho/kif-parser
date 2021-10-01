import glob
from kifu_to_pivot import convert_kifu_to_pivot
from kif_to_kifu import convert_kif_to_kifu
from kif_to_kifu import copy_kif_from_input
import argparse
from remove_all_temporary import remove_all_temporary


def convert_kif_to_pivot(kif_file, output_folder='temporary/pivot'):
    kifu_file, doneKifFile = convert_kif_to_kifu(kif_file)
    if kifu_file is None:
        return None, None

    pivot_file, _doneKifuFile = convert_kifu_to_pivot(
        kifu_file, output_folder=output_folder)
    if pivot_file is None:
        return None, None

    # print(f'kifu_file={kifu_file} pivot_file={pivot_file}')
    return pivot_file, doneKifFile


def main(debug=False):
    copy_kif_from_input()

    # KIFファイル一覧
    kif_files = glob.glob("./temporary/kif/*.kif")
    for kif_file in kif_files:
        pivot_File, _done_kif_file = convert_kif_to_pivot(
            kif_file, output_folder='output')
        if pivot_File is None:
            print(f"Parse fail. kif_file={kif_file}")

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary()


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    # Description
    parser = argparse.ArgumentParser(
        description='Convert from .kif file to .json (PIVOT) file.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    main(debug=args.debug)
