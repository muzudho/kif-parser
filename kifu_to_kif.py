import argparse
import glob
from remove_all_output import clear_last_layer_folder
from remove_all_temporary import remove_all_temporary
from scripts.convert_kifu_to_kif import convert_kifu_to_kif
from scripts.copy_files_to_folder import copy_files_to_folder


def __main(debug=False):

    # 2. 指定のファイルを 指定のフォルダーへコピーします
    converter_firlst_layer_file_pattern = './input/*.kifu'
    converter_layer2_folder = 'temporary/kifu'

    # 3-1. 処理対処となる各ファイル
    converter_layer2_file_pattern = './temporary/kifu/*.kifu'

    # 1. 出力フォルダーを空っぽにします
    if not debug:
        clear_last_layer_folder(echo=False)

    # inputフォルダーにある ? ファイルを layer2_folder へコピーします
    copy_files_to_folder(
        converter_firlst_layer_file_pattern, converter_layer2_folder)

    kifu_files = glob.glob(converter_layer2_file_pattern)

    for kifu_file in kifu_files:
        # 6. Pivot へ変換 (不要)

        # 5. Shift-JIS から UTF-8 へ変換
        kif_file, _done_path = convert_kifu_to_kif(
            kifu_file, output_folder='output', done_folder='temporary/kifu-done')
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
