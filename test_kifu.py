import glob
import shutil
import os
from scripts.test_lib import create_sha256, create_sha256_by_file_path
from kifu_to_pivot import convert_kifu_to_pivot
from pivot_to_kifu import convert_pivot_to_kifu
from kifu_to_kif import copy_kifu_from_input
import argparse
from remove_all_temporary import remove_all_temporary
from remove_all_output import remove_all_output
import sys


def test_2_kifu_files(kifu_file, reverse_output_folder='reverse-temporary/kifu', done_folder='temporary/kifu-done'):
    # basename
    try:
        basename = os.path.basename(kifu_file)
    except:
        print(
            f"Error: test_kifu.py kifu_file={kifu_file} except={sys.exc_info()[0]}")
        raise

    # 拡張子 check は必ず入れます
    _stem, extention = os.path.splitext(basename)
    if extention.lower() != '.kifu':
        return None

    # ファイルをバイナリ形式で読み込んで SHA256 生成
    kifu_1_Sha256 = create_sha256_by_file_path(kifu_file)

    # kifu -> pivot 変換
    pivot_file, _done_kifu_file = convert_kifu_to_pivot(kifu_file)

    # pivot -> kifu 変換
    reverse_kifu_file, _done_pivot_file_2nd = convert_pivot_to_kifu(
        pivot_file, output_folder=reverse_output_folder)

    kifuBinary2 = None

    # 読み取り専用、バイナリ
    with open(reverse_kifu_file, 'rb') as f:
        kifuBinary2 = f.read()

    # ファイルをバイナリ形式で読み込んで SHA256 生成
    kifu_2_Sha256 = create_sha256(kifuBinary2)

    if kifu_1_Sha256 != kifu_2_Sha256:
        # Error
        print(f"Not match SHA256. basename={basename}")
        return None

    # Ok
    # ファイルの移動
    done_kifu_file = shutil.move(reverse_kifu_file, os.path.join(
        done_folder, basename))
    return done_kifu_file


def __main(debug=False):
    # 1. 出力フォルダーを空っぽにします
    if not debug:
        remove_all_output(echo=False)

    copy_kifu_from_input()

    # 2 各 kif ファイルについて
    kifu_files = glob.glob('./temporary/kifu/*.kifu')
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
