import glob
import shutil
import os
from scripts.test_lib import create_sha256
from kifu_to_pivot import convert_kifu_to_pivot
from pivot_to_kifu import convert_pivot_to_kifu
from kifu_to_kif import copy_kifu_from_input


def test_2_kifu_files(kifuFile):
    # basename
    basename = os.path.basename(kifuFile)
    _stem, extention = os.path.splitext(basename)
    if extention.lower() != '.kifu':
        return ""

    kifuBinary = None

    # 読み取り専用、バイナリ
    with open(kifuFile, 'rb') as f:
        kifuBinary = f.read()

    # print(binaryData)

    # ファイルをバイナリ形式で読み込んで SHA256 生成
    kifu_1_Sha256 = create_sha256(kifuBinary)

    # kifu -> pivot 変換
    pivotFile, _doneKifuFile = convert_kifu_to_pivot(kifuFile)

    # pivot -> kifu 変換
    kifuFile2, _donePivotFile2 = convert_pivot_to_kifu(pivotFile)

    kifuBinary2 = None

    # 読み取り専用、バイナリ
    with open(kifuFile2, 'rb') as f:
        kifuBinary2 = f.read()

    # ファイルをバイナリ形式で読み込んで SHA256 生成
    kifu_2_Sha256 = create_sha256(kifuBinary2)

    if kifu_1_Sha256 != kifu_2_Sha256:
        # Error
        print(f"Not match SHA256. basename={basename}")
        return None

    # Ok
    # ファイルの移動
    doneKifuFile = shutil.move(kifuFile, os.path.join('kifu-done', basename))
    return doneKifuFile


def main():
    copy_kifu_from_input()

    # KIFUファイル一覧
    kifu_files = glob.glob("./kifu/*.kifu")
    for kifu_file in kifu_files:
        _doneKifuFile = test_2_kifu_files(kifu_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
