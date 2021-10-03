import glob
import argparse
from remove_all_temporary import remove_all_temporary
from scripts.convert_kifu_to_kif import convert_kifu_to_kif
from scripts.converter_template import ConverterTemplate


def __main(debug=False):
    converter = ConverterTemplate()
    # 1. 出力フォルダーを空っぽにします
    if not debug:
        converter.last_layer_folder_clean = True
        converter.last_layer_folder_clean_echo = False

    # 2. 指定のファイルを 指定のフォルダーへコピーします
    converter.firlst_layer_file_pattern = './input/*.kifu'
    converter.layer2_folder = 'temporary/kifu'

    converter.convert_before_loop()

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
