import glob
from kif_to_kifu import copy_kif_from_input
from kif_to_pivot import convert_kif_to_pivot
from pivot_to_toml import convert_pivot_to_toml
import argparse
from remove_all_temporary import remove_all_temporary
from remove_all_output import remove_all_output


def __main(debug=False):
    if not debug:
        # 出力フォルダーを空っぽにします
        remove_all_output(echo=False)

    copy_kif_from_input()

    # KIFファイル一覧
    kif_files = glob.glob("./temporary/kif/*.kif")
    for kif_file in kif_files:
        pivot_file, _doneKifFile = convert_kif_to_pivot(
            kif_file, output_folder='output')
        if pivot_file is None:
            print(f"kif_to_toml.py Parse fail. kif_file=[{kif_file}]")
            continue

        _tomlFile, _done_pivot_file = convert_pivot_to_toml(
            pivot_file, 'output')

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary(echo=False)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    # Description
    parser = argparse.ArgumentParser(
        description='Convert from .kif file to .toml file.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    __main(debug=args.debug)
