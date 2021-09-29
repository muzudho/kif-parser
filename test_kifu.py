import glob
import shutil
import os
from scripts.test_lib import create_sha256
from kifu_to_pibot import convert_kifu_to_pibot
from pibot_to_kifu import convert_pibot_to_kifu


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

    # kifu -> pibot 変換
    pibotFile, _doneKifuFile = convert_kifu_to_pibot(kifuFile)

    # pibot -> kifu 変換
    kifuFile2, _donePibotFile2 = convert_pibot_to_kifu(pibotFile)

    kifuBinary2 = None

    # 読み取り専用、バイナリ
    with open(kifuFile2, 'rb') as f:
        kifuBinary2 = f.read()

    # ファイルをバイナリ形式で読み込んで SHA256 生成
    kifu_2_Sha256 = create_sha256(kifuBinary2)

    if kifu_1_Sha256 != kifu_2_Sha256:
        # Error
        print("Not match")
        return None

    # Ok
    # ファイルの移動
    doneKifuFile = shutil.move(kifuFile, os.path.join('kifu-done', basename))
    return doneKifuFile


def main():
    # KIFUファイル一覧
    kifuFiles = glob.glob("./kifu/*")
    for kifuFile in kifuFiles:

        _doneKifuFile = test_2_kifu_files(kifuFile)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
