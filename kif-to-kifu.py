import glob
import shutil
import os
import codecs

def convert_kif_file(path):
    """(1) kif フォルダーの *.kifファイルを読み取ります
    (2) *.kifuファイルを kifu フォルダーへ生成します
    (3) 読み終えた *.kifファイルは kif-done フォルダーへ移動します

    Returns
    -------
    str
        新しいパス。
        KIFファイルでなかったなら空文字列
    """

    newPath = ""

    # シフトJISエンコードのテキストファイルの読み込み
    with codecs.open(path, "r", encoding='shift_jis') as f:

        # basename
        basename = os.path.basename(path)
        stem, extention = os.path.splitext(basename)
        if extention.lower() != '.kif':
            return ""

        # Append new extention
        basename = f"{stem}.kifu"

        newPath = os.path.join('kifu', basename)

        with codecs.open(newPath, "w", encoding='utf-8') as fOut:

            # UTF-8形式に変換して保存
            for row in f:
                fOut.write(row)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    newPath = shutil.move(path, 'kif-done')

    return newPath

def main():
    # KIFファイル一覧
    files = glob.glob("./kif/*")
    for file in files:
        _newPath = convert_kif_file(file)

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
