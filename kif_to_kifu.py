import argparse
import glob
from os import error, system
import os
from remove_all_output import clear_all_records_in_folder
from remove_all_temporary import remove_all_temporary
from scripts.convert_kif_to_kifu import convert_kif_to_kifu
from scripts.convert_kifu_to_kif import convert_kifu_to_kif
from scripts.copy_files_to_folder import copy_files_to_folder
from scripts.move_file_to_folder_by_pattern import move_file_to_folder
from scripts.test_lib import create_sha256_by_file_path


def __main(debug=False):

    # Layer 1. 入力フォルダ―
    layer1_file_pattern = './input/*.kif'

    # Layer 2. 入力フォルダ―のコピーフォルダー
    layer2_folder = 'temporary/kif'
    layer2_file_pattern = './temporary/kif/*.kif'

    # Layer 3. Pivotフォルダ―
    # (なし)

    # 中間Layer.
    object_folder = 'temporary/object'

    # Layer 4. 逆方向のフォルダ―
    layer4_folder = 'reverse-temporary/kif'

    # 最終Layer.
    last_layer_folder = 'output'

    # 1. 最終レイヤーの フォルダー を空っぽにします
    if not debug:
        clear_all_records_in_folder(last_layer_folder, echo=False)

    # 2. レイヤー１フォルダ―にあるファイルを レイヤー２フォルダ―へコピーします
    copy_files_to_folder(layer1_file_pattern, layer2_folder)

    # 3. レイヤー２にあるファイルのリスト
    kif_files = glob.glob(layer2_file_pattern)

    for kif_file in kif_files:

        # レイヤー２にあるファイルの SHA256 生成
        layer2_file_sha256 = create_sha256_by_file_path(kif_file)

        # Shift-JIS から UTF-8 へ変換
        kifu_file = convert_kif_to_kifu(
            kif_file, output_folder=object_folder)
        if kifu_file is None:
            print(f"Error: kif_to_kifu.py parse fail. kif_file=[{kif_file}]")
            continue

        # ここから逆の操作を行います

        # UTF-8 から Shift-JIS へ変換
        reversed_kif_file = convert_kifu_to_kif(
            kifu_file, output_folder=layer4_folder)

        # レイヤー４にあるファイルの SHA256 生成
        layer4_file_sha256 = create_sha256_by_file_path(reversed_kif_file)

        # 一致比較
        if layer2_file_sha256 != layer4_file_sha256:
            # Error
            try:
                basename = os.path.basename(kif_file)
            except:
                print(
                    f"Error: kif_file={kif_file} except={system.exc_info()[0]}")
                raise

            # 不可逆な変換だが、とりあえず通します
            print(
                f"WARNING: Irreversible conversion. basename={basename}")
            # continue

        # 後ろから2. 中間レイヤー フォルダ―の中身を 最終レイヤー フォルダ―へ移動します
        move_file_to_folder(kifu_file, last_layer_folder)

    # 後ろから1. 変換の途中で作ったファイルは削除します
    if not debug:
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
