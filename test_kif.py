import glob
import shutil
import os
import sys
from scripts.test_lib import create_sha256
from kif_to_pivot import convert_kif_to_pivot
from pivot_to_kif import convert_pivot_to_kif
from kif_to_kifu import copy_kif_from_input
import argparse
from remove_all_temporary import remove_all_temporary
from remove_all_output import remove_all_output


def test_2_kif_files(kif_file, reverse_output_folder='reverse-temporary/kif', done_folder='temporary/kif-done'):
    # basename
    try:
        basename = os.path.basename(kif_file)
    except:
        print(f"Error: kif_file={kif_file} except={sys.exc_info()[0]}")
        raise

    _stem, extention = os.path.splitext(basename)
    if extention.lower() != '.kif':
        return ""

    kif_binary = None

    # 読み取り専用、バイナリ
    with open(kif_file, 'rb') as f:
        kif_binary = f.read()

    # print(binaryData)

    # ファイルをバイナリ形式で読み込んで SHA256 生成
    kif_1_Sha256 = create_sha256(kif_binary)
    # print(f"kif 1 Sha256={kif_1_Sha256}")

    # kif -> pivot 変換
    pivot_file, _done_kif_file = convert_kif_to_pivot(kif_file)
    if pivot_file is None:
        # Error
        print(f"convert kif to pivot_file fail. kif_file={kif_file}")
        return None

    # pivot -> kif 変換
    reverse_kif_file, _reverse_done_pivot_file = convert_pivot_to_kif(
        pivot_file, output_folder=reverse_output_folder)
    if reverse_kif_file is None:
        # Error
        print(
            f"convert pivot to kif fail. reverse_kif_file={reverse_kif_file}")
        return None

    kif_binary_2nd = None

    # 読み取り専用、バイナリ
    with open(reverse_kif_file, 'rb') as f:
        kif_binary_2nd = f.read()

    # ファイルをバイナリ形式で読み込んで SHA256 生成
    kif_2_Sha256 = create_sha256(kif_binary_2nd)
    # print(f"kif 2 Sha256={kif_2_Sha256}")

    if kif_1_Sha256 != kif_2_Sha256:
        # Error
        print(f"Not match SHA256. basename={basename}")
        return None

    # Ok
    # ファイルの移動
    done_kif_file = shutil.move(
        reverse_kif_file, os.path.join(done_folder, basename))
    return done_kif_file


def __main(debug=False):
    if not debug:
        # 出力フォルダーを空っぽにします
        remove_all_output(echo=False)

    # `input` フォルダーから `temporary/kif` フォルダーへ `*.kif` ファイルを移動します
    copy_kif_from_input()

    # KIFファイル一覧
    kif_files = glob.glob("./temporary/kif/*.kif")
    for kif_file in kif_files:
        _done_kif_file = test_2_kif_files(kif_file)

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
