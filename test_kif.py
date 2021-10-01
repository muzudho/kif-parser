import glob
import shutil
import os
from scripts.test_lib import create_sha256
from kif_to_pivot import convert_kif_to_pivot
from pivot_to_kif import convert_pivot_to_kif
from kif_to_kifu import copy_kif_from_input


def test_2_kif_files(kif_file, done_folder='temporary/kif-done_d'):
    # basename
    basename = os.path.basename(kif_file)
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
    pivot_file, _doneKifFile = convert_kif_to_pivot(kif_file)
    if pivot_file is None:
        # Error
        print(f"convert kif to pivot_file fail. kif_file={kif_file}")
        return None

    # pivot -> kif 変換
    kif_file2, _donePivotFile2 = convert_pivot_to_kif(pivot_file)
    if kif_file2 is None:
        # Error
        print(f"convert pivot to kif fail. kif_file2={kif_file2}")
        return None

    kif_binary2 = None

    # 読み取り専用、バイナリ
    with open(kif_file2, 'rb') as f:
        kif_binary2 = f.read()

    # ファイルをバイナリ形式で読み込んで SHA256 生成
    kif_2_Sha256 = create_sha256(kif_binary2)
    # print(f"kif 2 Sha256={kif_2_Sha256}")

    if kif_1_Sha256 != kif_2_Sha256:
        # Error
        print(f"Not match SHA256. basename={basename}")
        return None

    # Ok
    # ファイルの移動
    doneKifFile = shutil.move(kif_file, os.path.join(done_folder, basename))
    return doneKifFile


def main():
    # `input` フォルダーから `temporary/kif_d` フォルダーへ `*.kif` ファイルを移動します
    copy_kif_from_input()

    # KIFファイル一覧
    kif_files = glob.glob("./temporary/kif_d/*.kif")
    for kif_file in kif_files:
        _doneKifFile = test_2_kif_files(kif_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
