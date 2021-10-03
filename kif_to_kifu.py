import argparse
from remove_all_output import remove_all_output
from remove_all_temporary import remove_all_temporary
from scripts.convert_kif_to_kifu import convert_kif_to_kifu
from scripts.converter_template import ConverterTemplate
from scripts.copy_files_to_folder import copy_files_to_folder


def __main(debug=False):
    converter = ConverterTemplate()
    # 1. 出力フォルダーを空っぽにします
    if not debug:
        converter.last_layer_folder_clean = True
        converter.last_layer_folder_clean_echo = False

    # 2. 指定のファイルを 指定のフォルダーへコピーします
    converter.firlst_layer_file_pattern = './input/*.kif'
    converter.layer2_folder = 'temporary/kif'

    # 3-1. 処理対処となる各ファイル
    converter.layer2_file_pattern = './temporary/kif/*.kif'

    # 1. 最終フォルダーを空っぽにします
    if converter._last_layer_folder_clean:
        remove_all_output(echo=False)

    # inputフォルダーにある ? ファイルを layer2_folder へコピーします
    copy_files_to_folder(
        converter.firlst_layer_file_pattern, converter.layer2_folder)

    kif_files = converter.list_layer2_files()

    for kif_file in kif_files:
        # 5. Shift-JIS から UTF-8 へ変換
        out_path, _done_path = convert_kif_to_kifu(
            kif_file, output_folder='output')
        if out_path is None:
            print(f"Parse fail. kif_file={kif_file}")

        # 6. Pivot へ変換 (不要)

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary(echo=False)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":

    # Description
    parser = argparse.ArgumentParser(
        description='Convert from .kif file to .kifu file.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    __main(debug=args.debug)
