import argparse
import glob
from remove_all_output import remove_all_output
from remove_all_temporary import remove_all_temporary
from scripts.convert_pivot_to_kifu import convert_pivot_to_kifu
from scripts.convert_kifu_to_kif import convert_kifu_to_kif
from scripts.copy_files_to_folder import copy_files_to_folder


def __main(debug=False):
    # 1. 出力フォルダーを空っぽにします
    if not debug:
        converter_last_layer_folder_clean = True
        converter_last_layer_folder_clean_echo = False

    # 2. 指定のファイルを 指定のフォルダーへコピーします
    converter_firlst_layer_file_pattern = './input/*.json'
    converter_layer2_folder = 'temporary/pivot'

    # 3-1. 処理対処となる各ファイル
    converter_layer2_file_pattern = './temporary/pivot/*.json'

    # 1. 最終フォルダーを空っぽにします
    if converter_last_layer_folder_clean:
        remove_all_output(converter_last_layer_folder_clean_echo)

    # inputフォルダーにある ? ファイルを layer2_folder へコピーします
    copy_files_to_folder(
        converter_firlst_layer_file_pattern, converter_layer2_folder)

    pivot_files = glob.glob(converter_layer2_file_pattern)

    for pivot_file in pivot_files:
        # 5. Shift-JIS から UTF-8 へ変換 (不要)

        # 6. Pivot へ変換 (不要)

        # Pivot to kifu
        kifu_file, _done_pivot_file = convert_pivot_to_kifu(
            pivot_file, output_folder='temporary/kifu', done_folder='temporary/pivot-done')
        if kifu_file is None:
            print(f"Parse fail. pivot_file={pivot_file}")
            continue

        # kifu to kif
        kif_file, _done_kifu_file = convert_kifu_to_kif(
            kifu_file, output_folder='output', done_folder='temporary/kifu-done')

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
