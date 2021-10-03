import glob
from scripts.convert_kif_to_pivot import convert_kif_to_pivot
import argparse
from remove_all_temporary import remove_all_temporary
from scripts.converter_template import ConverterTemplate


def __main(debug=False):
    converter = ConverterTemplate()
    # 1. 出力フォルダーを空っぽにします
    if not debug:
        converter.output_folder_clean = True
        converter.output_folder_clean_echo = False

    # 2. 指定のファイルを 指定のフォルダーへコピーします
    converter.input_file_pattern = './input/*.kif'
    converter.layer2_folder = 'temporary/kif'

    converter.convert_before_loop()

    # KIFファイル一覧
    kif_files = glob.glob("./temporary/kif/*.kif")
    for kif_file in kif_files:
        pivot_File, _done_kif_file = convert_kif_to_pivot(
            kif_file, output_folder='output')
        if pivot_File is None:
            print(f"Parse fail. kif_file={kif_file}")

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary(echo=False)


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

    __main(debug=args.debug)
