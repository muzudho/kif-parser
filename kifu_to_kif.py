import argparse
import glob
import os
from remove_all_output import clear_all_records_in_folder
from remove_all_temporary import remove_all_temporary
from scripts.convert_kifu_to_kif import convert_kifu_to_kif
from scripts.convert_kif_to_kifu import convert_kif_to_kifu
from scripts.copy_file_to_folder import copy_file_to_folder
from scripts.move_file_to_folder import move_file_to_folder
from scripts.test_lib import create_sha256_by_file_path


def __main(debug=False):

    # Layer 1. 入力フォルダ―
    layer1_file_pattern = './input/*.kifu'

    # Layer 2. 入力フォルダ―のコピーフォルダー
    layer2_folder = 'temporary/kifu'
    layer2_file_pattern = './temporary/kifu/*.kifu'

    # Layer 3. Pivotフォルダ―
    # (なし)

    # 中間Layer.
    object_folder = 'temporary/object'

    # Layer 4. 入力フォルダ―のコピーフォルダー
    layer4_folder = 'temporary/reverse-kifu'

    # 最終Layer.
    last_layer_folder = 'output'

    # 1. 最終レイヤーの フォルダー を空っぽにします
    if not debug:
        clear_all_records_in_folder(last_layer_folder, echo=False)

    # 2. レイヤー１フォルダ―にあるファイルを レイヤー２フォルダ―へコピーします
    input_files = glob.glob(layer1_file_pattern)
    for input_file in input_files:
        copy_file_to_folder(input_file, layer2_folder)

    # 3. レイヤー２にあるファイルのリスト
    kifu_files = glob.glob(layer2_file_pattern)

    for kifu_file in kifu_files:

        # レイヤー２にあるファイルの SHA256 生成
        layer2_file_sha256 = create_sha256_by_file_path(kifu_file)

        # Shift-JIS から UTF-8 へ変換
        kif_file = convert_kifu_to_kif(
            kifu_file, output_folder=object_folder)
        if kif_file is None:
            print(f"Parse fail. kifu_file={kifu_file}")
            continue

        # ここから逆の操作を行います

        reversed_kifu_file = convert_kif_to_kifu(
            kif_file, output_folder=layer4_folder)
        if reversed_kifu_file is None:
            print(f"Error: Parse fail. kifu_file={kifu_file}")
            continue

        # レイヤー４にあるファイルの SHA256 生成
        layer4_file_sha256 = create_sha256_by_file_path(reversed_kifu_file)

        # 一致比較
        if layer2_file_sha256 != layer4_file_sha256:
            # Error
            try:
                basename = os.path.basename(kif_file)
            except:
                print(
                    f"Error: kifu_file={kifu_file} except={os.system.exc_info()[0]}")
                raise

            # 不可逆な変換だが、とりあえず通します
            print(
                f"WARNING: Irreversible conversion. basename={basename}")
            # continue

        # 後ろから2. 中間レイヤー フォルダ―の中身を 最終レイヤー フォルダ―へ移動します
        move_file_to_folder(kif_file, last_layer_folder)

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
