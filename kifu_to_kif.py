import glob
import argparse
from remove_all_temporary import remove_all_temporary
from remove_all_output import remove_all_output
from scripts.copy_kifu_from_input import copy_kifu_from_input
from scripts.convert_kifu_to_kif import convert_kifu_to_kif


def __main(debug=False):
    if not debug:
        # 出力フォルダーを空っぽにします
        remove_all_output(echo=False)

    copy_kifu_from_input()

    # KIFUファイル一覧
    kifu_files = glob.glob("./temporary/kifu/*.kifu")
    for kifu_file in kifu_files:
        kif_file, _done_path = convert_kifu_to_kif(
            kifu_file, output_folder='output')

        if kif_file is None:
            print(f"Parse fail. kifu_file={kifu_file}")

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary(echo=False)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    # Description
    parser = argparse.ArgumentParser(
        description='Convert from .kifu file to .kif file.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    __main(debug=args.debug)
