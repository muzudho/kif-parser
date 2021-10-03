import argparse
import glob
from remove_all_output import clear_all_records_in_folder
from remove_all_temporary import remove_all_temporary
from scripts.convert_kifu_to_kif import convert_kifu_to_kif
from scripts.copy_files_to_folder import copy_files_to_folder


def __main(debug=False):

    # Layer 1. 入力フォルダ―
    layer1_file_pattern = './input/*.kifu'

    # Layer 2. 入力フォルダ―のコピーフォルダー
    layer2_folder = 'temporary/kifu'
    layer2_file_pattern = './temporary/kifu/*.kifu'

    # Layer 3. Pivotフォルダ―
    # (なし)

    # 最終Layer.
    last_layer_folder = 'output'

    # 1. 最終レイヤーの フォルダー を空っぽにします
    if not debug:
        clear_all_records_in_folder(last_layer_folder, echo=False)

    # 2. レイヤー１フォルダ―にあるファイルを レイヤー２フォルダ―へコピーします
    copy_files_to_folder(layer1_file_pattern, layer2_folder)

    # 3. レイヤー２にあるファイルのリスト
    kifu_files = glob.glob(layer2_file_pattern)

    for kifu_file in kifu_files:

        # レイヤー２にあるファイルの SHA256 生成
        # layer2_file_sha256 = create_sha256_by_file_path(kif_file)

        # Shift-JIS から UTF-8 へ変換
        kif_file = convert_kifu_to_kif(
            kifu_file, output_folder=last_layer_folder)
        if kif_file is None:
            print(f"Parse fail. kifu_file={kifu_file}")
            continue

    # 後ろから1. 変換の途中で作ったファイルは削除します
    if not debug:
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
