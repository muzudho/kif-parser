import glob
import shutil
import os
import codecs
import sys

def read_kif_file(path):
    """(1) input フォルダーのKIFファイルを読み取ります
    (2) KIFUファイルを hidden-step1 フォルダーへ生成します
    (3) KIFファイルは input-done フォルダーへ移動します

    Returns
    -------
    str
        新しいパス
    """

    newPath = ""

    # シフトJISエンコードのテキストファイルの読み込み
    with codecs.open(path, "r", encoding='shift_jis') as f:

        # basename
        basename = os.path.basename(path)
        # Except old extention
        stem = os.path.splitext(basename)[0]
        # Append new extention
        basename = f"{stem}.kifu"

        newPath = os.path.join('hidden-step1', basename)

        with codecs.open(newPath, "w", encoding='utf-8') as fOut:

            # UTF-8形式に変換して保存
            for row in f:
                fOut.write(row)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    new_path = shutil.move(path, 'input-done')
    print(new_path)

    return newPath

def main():
    # KIFファイル一覧
    files = glob.glob("./input/*")
    for file in files:
        _newPath = read_kif_file(file)

    # KIFUファイル一覧
    files = glob.glob("./hidden-step1/*")
    for file in files:

        # とりあえず KIFU を読んでみます
        with open(file, encoding='utf-8') as f:
            s = f.read()
            print(s.rstrip())  # このファイルはシフトJISでエンコードされています

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
