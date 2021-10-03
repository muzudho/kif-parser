import glob
from scripts.convert_pivot_to_kif import convert_pivot_to_kif
from pivot_to_kifu import copy_pivot_from_input
import argparse
from remove_all_temporary import remove_all_temporary
from remove_all_output import remove_all_output


def __main(debug=False):
    # 1. 出力フォルダーを空っぽにします
    if not debug:
        remove_all_output(echo=False)

    # 2. `input` フォルダーから `temporary/pivot` フォルダーへ `*.kif` ファイルを移動します
    copy_pivot_from_input()

    # PIVOTファイル一覧
    pivot_files = glob.glob("./temporary/pivot/*.json")
    for pivot_file in pivot_files:
        kif_file, _done_pivot_file = convert_pivot_to_kif(
            pivot_file, output_folder='output')

        if kif_file is None:
            print(f"Parse fail. pivot_file={pivot_file}")

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary(echo=False)


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
