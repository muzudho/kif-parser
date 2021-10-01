import glob
import shutil
import os
import codecs


def copy_kif_from_input():
    """inputフォルダーにある `*.kif` ファイルを kifフォルダーへコピーします"""

    input_files = glob.glob("./input/*.kif")
    for input_file in input_files:
        # basename
        basename = os.path.basename(input_file)
        copy_file = os.path.join('kif', basename)
        shutil.copyfile(input_file, copy_file)


def convert_kif_to_kifu(kif_file, output_folder='kifu', done_folder='kif-done'):
    """(1) kif フォルダーの *.kifファイルを読み取ります
    (2) *.kifuファイルを kifu フォルダーへ生成します
    (3) 読み終えた *.kifファイルは kif-done フォルダーへ移動します

    Returns
    -------
    (str, str)
        出力したkifuファイルへのパス, 読み終えたkifファイルへのパス
        KIFファイルでなかったなら空文字列
    """

    outPath = ""

    # シフトJISエンコードのテキストファイルの読み込み
    with codecs.open(kif_file, "r", encoding='shift_jis') as f:

        # basename
        basename = os.path.basename(kif_file)
        stem, extention = os.path.splitext(basename)
        if extention.lower() != '.kif':
            return None, None

        # Append new extention
        outPath = os.path.join(output_folder, f"{stem}.kifu")

        with codecs.open(outPath, "w", encoding='utf-8') as fOut:

            # UTF-8形式に変換して保存
            for row in f:
                fOut.write(row)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    donePath = shutil.move(kif_file, os.path.join(done_folder, basename))
    return outPath, donePath


def main():
    copy_kif_from_input()

    # KIFファイル一覧
    kif_files = glob.glob("./kif/*.kif")
    for kif_file in kif_files:
        _outPath, _donePath = convert_kif_to_kifu(
            kif_file, output_folder='output')


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
