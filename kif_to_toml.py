import glob
from remove_all_output import clear_last_layer_folder
from scripts.convert_kifu_to_pivot import convert_kifu_to_pivot
import argparse
from remove_all_temporary import remove_all_temporary
from scripts.convert_pivot_to_toml import convert_pivot_to_toml
from scripts.convert_kif_to_kifu import convert_kif_to_kifu
from scripts.copy_files_to_folder import copy_files_to_folder


def __main(debug=False):

    # 2. 指定のファイルを 指定のフォルダーへコピーします
    converter_firlst_layer_file_pattern = './input/*.kif'
    converter_layer2_folder = 'temporary/kif'

    # 3-1. 処理対処となる各ファイル
    converter_layer2_file_pattern = './temporary/kif/*.kif'

    # 1. 出力フォルダーを空っぽにします
    if not debug:
        clear_last_layer_folder(echo=False)

    # inputフォルダーにある ? ファイルを layer2_folder へコピーします
    copy_files_to_folder(
        converter_firlst_layer_file_pattern, converter_layer2_folder)

    kif_files = glob.glob(converter_layer2_file_pattern)

    for kif_file in kif_files:
        # 5. Shift-JIS から UTF-8 へ変更
        kifu_file, _done_kif_file = convert_kif_to_kifu(kif_file)
        if kifu_file is None:
            return None, None

        # 6. Pivot へ変換
        pivot_file = convert_kifu_to_pivot(
            kifu_file, output_folder='output')
        if pivot_file is None:
            print(f"kif_to_toml.py Parse fail. kif_file=[{kif_file}]")
            continue

        _tomlFile, _done_pivot_file = convert_pivot_to_toml(
            pivot_file, 'output', done_folder='temporary/pivot-done')

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
