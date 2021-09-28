import glob
import shutil
import os
import codecs
import sys

def read_kif_file(path):
    """(1) input フォルダーのKIFファイルを読み取ります
    (2) KIFUファイルを hidden-step1 フォルダーへ生成します
    (3) KIFファイルは input-done フォルダーへ移動します
    """

    success = False

    # シフトJISエンコードのテキストファイルの読み込み
    with codecs.open(path, "r", encoding='shift_jis') as f:

        # basename
        basename = os.path.basename(path)
        # Except old extention
        stem = os.path.splitext(basename)[0]
        # Append new extention
        basename = f"{stem}.kifu"

        destination = os.path.join('hidden-step1', basename)

        with codecs.open(destination, "w", encoding='utf-8') as fOut:

            # UTF-8形式に変換して保存
            for row in f:
                fOut.write(row)

        success = True

    # with句を抜けて、ファイルを閉じたあと

    if success:
        # ファイルの移動
        new_path = shutil.move(path, 'input-done')
        print(new_path)

def main():
    # ファイル一覧
    files = glob.glob("./input/*")
    for file in files:
        read_kif_file(file)

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
