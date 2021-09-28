import glob
import shutil
import os
import codecs

def convert_kifu_to_kif_file(path):
    """(1) kifu フォルダーの *.kifuファイルを読み取ります
    (2) *.kifファイルを kif フォルダーへ生成します
    (3) 読み終えた *.kifuファイルは kifu-done フォルダーへ移動します

    Returns
    -------
    str
        新しいパス。
        KIFUファイルでなかったなら空文字列
    """

    outPath = ""

    # シフトJISエンコードのテキストファイルの読み込み
    with codecs.open(path, "r", encoding='utf-8') as f:

        # basename
        basename = os.path.basename(path)
        stem, extention = os.path.splitext(basename)
        if extention.lower() != '.kifu':
            return ""

        # Append new extention
        basename = f"{stem}.kif"

        outPath = os.path.join('kif', basename)

        with codecs.open(outPath, "w", encoding='shift_jis') as fOut:

            # UTF-8形式に変換して保存
            for row in f:
                fOut.write(row)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    donePath = shutil.move(path, 'kifu-done')
    return outPath, donePath

def main():
    # KIFファイル一覧
    files = glob.glob("./kifu/*")
    for file in files:
        _outPath, _donePath = convert_kifu_to_kif_file(file)

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
