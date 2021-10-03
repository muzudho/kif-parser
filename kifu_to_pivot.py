import argparse
from remove_all_temporary import remove_all_temporary
from scripts.convert_kifu_to_pivot import convert_kifu_to_pivot
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

    # 3-1. 処理対処となる各ファイル
    converter.layer2_file_pattern = './temporary/kifu/*.kifu'

    # 4. KIFUファイル一覧
    converter.convert_before_loop()
    kifu_files = converter.list_layer2_files()

    for kifu_file in kifu_files:
        # 5. Shift-JIS から UTF-8 へ変換 (不要)

        # 6. Pivot へ変換
        output_pivot = convert_kifu_to_pivot(
            kifu_file, output_folder='output')
        if output_pivot is None:
            print(f"Parse fail. kifu_file={kifu_file}")

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary(echo=False)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    # Description
    parser = argparse.ArgumentParser(
        description='Convert from .kifu file to .json (PIVOT) file.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    __main(debug=args.debug)
