import glob
import shutil
import os
from scripts.test_lib import create_sha256
from kifu_to_pivot import convert_kifu_to_pivot
from pivot_to_kifu import convert_pivot_to_kifu
from kifu_to_kif import copy_kifu_from_input


def test_2_kifu_files(kifu_file, output_folder_2nd='temporary/kifu-2nd', done_folder='temporary/kifu-done'):
    # basename
    basename = os.path.basename(kifu_file)
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


def main():
    copy_kifu_from_input()

    # KIFUファイル一覧
    kifu_files = glob.glob("./temporary/kifu/*.kifu")
    for kifu_file in kifu_files:
        _done_kifu_file = test_2_kifu_files(kifu_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
