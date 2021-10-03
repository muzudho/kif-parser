import argparse
from remove_all_temporary import remove_all_temporary
from scripts.converter_template import ConverterTemplate
from scripts.convert_pivot_to_kifu import convert_pivot_to_kifu
from scripts.convert_kifu_to_kif import convert_kifu_to_kif


def __main(debug=False):
    converter = ConverterTemplate()
    # 1. 出力フォルダーを空っぽにします
    if not debug:
        converter.last_layer_folder_clean = True
        converter.last_layer_folder_clean_echo = False

    # 2. 指定のファイルを 指定のフォルダーへコピーします
    converter.firlst_layer_file_pattern = './input/*.json'
    converter.layer2_folder = 'temporary/pivot'

    # 3-1. 処理対処となる各ファイル
    converter.layer2_file_pattern = './temporary/pivot/*.json'

    # 4. PIVOTファイル一覧
    converter.convert_before_loop()
    pivot_files = converter.list_layer2_files()

    for pivot_file in pivot_files:
        # 5. Shift-JIS から UTF-8 へ変換 (不要)

        # 6. Pivot へ変換 (不要)

        # Pivot to kifu
        kifu_file, _done_pivot_file = convert_pivot_to_kifu(pivot_file)
        if kifu_file is None:
            print(f"Parse fail. pivot_file={pivot_file}")
            continue

        # kifu to kif
        kif_file, _done_kifu_file = convert_kifu_to_kif(
            kifu_file, output_folder='output')

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
