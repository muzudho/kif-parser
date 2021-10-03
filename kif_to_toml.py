import glob
from scripts.convert_kif_to_pivot import convert_kif_to_pivot
import argparse
from remove_all_temporary import remove_all_temporary
from scripts.convert_pivot_to_toml import convert_pivot_to_toml
from scripts.converter_template import ConverterTemplate


def __main(debug=False):
    converter = ConverterTemplate()
    # 1. 出力フォルダーを空っぽにします
    if not debug:
        converter.last_layer_folder_clean = True
        converter.last_layer_folder_clean_echo = False

    # 2. 指定のファイルを 指定のフォルダーへコピーします
    converter.firlst_layer_file_pattern = './input/*.kif'
    converter.layer2_folder = 'temporary/kif'
    converter.layer2_file_pattern = './temporary/kif/*.kif'

    converter.convert_before_loop()

    # KIFファイル一覧
    kif_files = glob.glob(converter.layer2_file_pattern)
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
