import glob
import shutil
import os
from scripts.test_lib import create_sha256
from kifu_to_pivot import convert_kifu_to_pivot
from pivot_to_kifu import convert_pivot_to_kifu
from kifu_to_kif import copy_kifu_from_input
import argparse
from remove_all_temporary import remove_all_temporary
from remove_all_output import remove_all_output
import sys


def test_2_kifu_files(kifu_file, output_folder_2nd='temporary/kifu-2nd', done_folder='temporary/kifu-done'):
    # basename
    try:
        basename = os.path.basename(kifu_file)
    except:
        print(f"Error: kifu_file={kifu_file} except={sys.exc_info()[0]}")
        raise

    _stem, extention = os.path.splitext(basename)
    if extention.lower() != '.kifu':
        return ""

    kifu_binary = None

    # 読み取り専用、バイナリ
    with open(kifu_file, 'rb') as f:
        kifu_binary = f.read()

    # print(binaryData)

    # ファイルをバイナリ形式で読み込んで SHA256 生成
    kifu_1_Sha256 = create_sha256(kifu_binary)

    # kifu -> pivot 変換
    pivot_file, _done_kifu_file = convert_kifu_to_pivot(kifu_file)

    # pivot -> kifu 変換
    kifu_file_2nd, _done_pivot_file_2nd = convert_pivot_to_kifu(
        pivot_file, output_folder=output_folder_2nd)

    kifuBinary2 = None

    # 読み取り専用、バイナリ
    with open(kifu_file_2nd, 'rb') as f:
        kifuBinary2 = f.read()

    # ファイルをバイナリ形式で読み込んで SHA256 生成
    kifu_2_Sha256 = create_sha256(kifuBinary2)

    if kifu_1_Sha256 != kifu_2_Sha256:
        # Error
        print(f"Not match SHA256. basename={basename}")
        return None

    # Ok
    # ファイルの移動
    done_kifu_file = shutil.move(kifu_file_2nd, os.path.join(
        done_folder, basename))
    return done_kifu_file


def __main(debug=False):
    if not debug:
        # 出力フォルダーを空っぽにします
        remove_all_output(echo=False)

    copy_kifu_from_input()

    # KIFUファイル一覧
    kifu_files = glob.glob("./temporary/kifu/*.kifu")
    for kifu_file in kifu_files:
        _done_kifu_file = test_2_kifu_files(kifu_file)

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary(echo=False)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    # Description
    parser = argparse.ArgumentParser(
        description='Test .kif Convert.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    __main(debug=args.debug)
