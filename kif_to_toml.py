import glob
from remove_all_output import clear_all_records_in_folder
from scripts.convert_kifu_to_pivot import convert_kifu_to_pivot
import argparse
from remove_all_temporary import remove_all_temporary
from scripts.convert_pivot_to_toml import convert_pivot_to_toml
from scripts.convert_kif_to_kifu import convert_kif_to_kifu
from scripts.copy_files_to_folder import copy_files_to_folder
from scripts.move_file_to_folder import move_file_to_folder


def __main(debug=False):

    # Layer 1. 入力フォルダ―
    layer1_file_pattern = './input/*.kif'

    # Layer 2. 入力フォルダ―のコピーフォルダー
    layer2_folder = 'temporary/kif'
    layer2_file_pattern = './temporary/kif/*.kif'

    # Layer 3. Pivotフォルダ―
    layer3_folder = 'temporary/pivot'

    # 中間Layer.
    object_folder = 'temporary/object'

    # Layer 4. 逆Pivotフォルダ―
    layer4_folder = 'temporary/reverse-pivot'

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
        # layer2_file_sha256 = create_sha256_by_file_path(kif_file)

        # Shift-JIS から UTF-8 へ変更
        kifu_file = convert_kif_to_kifu(kif_file, output_folder='temporary/kifu')
        if kifu_file is None:
            continue

        # 4. Pivot へ変換
        pivot_file = convert_kifu_to_pivot(
            kifu_file, output_folder=layer3_folder)
        if pivot_file is None:
            print(f"kif_to_toml.py Parse fail. kif_file=[{kif_file}]")
            continue

        # 5. TOML へ変換
        toml_file = convert_pivot_to_toml(pivot_file, object_folder)

        # TODO ここから逆の操作を行います

        # convert_toml_to_pivot(toml_file, layer4_folder)

        # 後ろから2. 中間レイヤー フォルダ―の中身を 最終レイヤー フォルダ―へ移動します
        move_file_to_folder(toml_file, last_layer_folder)

    # 後ろから1. 変換の途中で作ったファイルは削除します
    if not debug:
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
