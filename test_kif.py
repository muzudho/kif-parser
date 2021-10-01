import glob
import shutil
import os
from scripts.test_lib import create_sha256
from kif_to_pivot import convert_kif_to_pivot
from pivot_to_kif import convert_pivot_to_kif


def test_2_kif_files(kifFile):
    # basename
    basename = os.path.basename(kifFile)
    _stem, extention = os.path.splitext(basename)
    if extention.lower() != '.kif':
        return ""

    kifBinary = None

    # 読み取り専用、バイナリ
    with open(kifFile, 'rb') as f:
        kifBinary = f.read()

    # print(binaryData)

    # ファイルをバイナリ形式で読み込んで SHA256 生成
    kif_1_Sha256 = create_sha256(kifBinary)
    # print(f"kif 1 Sha256={kif_1_Sha256}")

    # kif -> pivot 変換
    pivotFile, _doneKifFile = convert_kif_to_pivot(kifFile)

    # pivot -> kif 変換
    kifFile2, _donePivotFile2 = convert_pivot_to_kif(pivotFile)

    kifBinary2 = None

    # 読み取り専用、バイナリ
    with open(kifFile2, 'rb') as f:
        kifBinary2 = f.read()

    # ファイルをバイナリ形式で読み込んで SHA256 生成
    kif_2_Sha256 = create_sha256(kifBinary2)
    # print(f"kif 2 Sha256={kif_2_Sha256}")

    if kif_1_Sha256 != kif_2_Sha256:
        # Error
        print(f"Not match SHA256. basename={basename}")
        return None

    # Ok
    # ファイルの移動
    doneKifFile = shutil.move(kifFile, os.path.join('kif-done', basename))
    return doneKifFile


def main():
    # KIFファイル一覧
    kif_files = glob.glob("./kif/*.kif")
    for kif_file in kif_files:
        _doneKifFile = test_2_kif_files(kif_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
