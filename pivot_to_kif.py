import argparse
import glob
from remove_all_output import clear_all_records_in_folder
from remove_all_temporary import remove_all_temporary
from scripts.convert_pivot_to_kifu import convert_pivot_to_kifu
from scripts.convert_kifu_to_kif import convert_kifu_to_kif
from scripts.copy_file_to_folder import copy_file_to_folder


def __main(debug=False, template_name=""):

    # Layer 1. 入力フォルダ―
    layer1_file_pattern = './input/*.json'

    # Layer 2. 入力フォルダ―のコピーフォルダー
    layer2_folder = 'temporary/pivot'
    layer2_file_pattern = './temporary/pivot/*[[]data[]].json'

    # Layer 3. Pivotフォルダ―
    # (なし)

    # 中間Layer.
    middle_folder = 'temporary/object'

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
    pivot_files = glob.glob(layer2_file_pattern)

    for pivot_file in pivot_files:
        # レイヤー２にあるファイルの SHA256 生成
        # layer2_file_sha256 = create_sha256_by_file_path(pivot_file)

        # 5. Pivot から 目的の棋譜ファイルへ変換
        kifu_file = convert_pivot_to_kifu(
            pivot_file, output_folder='temporary/kifu', template_name=template_name)
        if kifu_file is None:
            print(f"Parse fail. pivot_file={pivot_file}")
            continue

        # UTF-8 から Shift-JIS へ変換
        kif_file = convert_kifu_to_kif(
            kifu_file, output_folder=last_layer_folder)
        if kif_file is None:
            print(f"Parse fail. pivot_file={pivot_file}")
            continue

    # 後ろから1. 変換の途中で作ったファイルは削除します
    if not debug:
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
