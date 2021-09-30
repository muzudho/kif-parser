import glob
import shutil
import os
import codecs


def convert_kifu_to_kif(kifuFile):
    """(1) kifu フォルダーの *.kifuファイルを読み取ります
    (2) *.kifファイルを kif フォルダーへ生成します
    (3) 読み終えた *.kifuファイルは kifu-done フォルダーへ移動します

    Returns
    -------
    str
        新しいパス。
        KIFUファイルでなかったなら空文字列
    """

    kifFile = ""

    # シフトJISエンコードのテキストファイルの読み込み
    with codecs.open(kifuFile, "r", encoding='utf-8') as f:

        # basename
        basename = os.path.basename(kifuFile)
        stem, extention = os.path.splitext(basename)
        if extention.lower() != '.kifu':
            return ""

        # New file
        kifFile = os.path.join('kif', f"{stem}.kif")

        with codecs.open(kifFile, "w", encoding='shift_jis') as fOut:

            # UTF-8形式に変換して保存
            for row in f:
                fOut.write(row)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    doneKifuFile = shutil.move(kifuFile, os.path.join('kifu-done', basename))
    return kifFile, doneKifuFile


def main():
    # KIFUファイル一覧
    kifu_files = glob.glob("./kifu/*.kifu")
    for kifu_file in kifu_files:
        _kifFile, _donePath = convert_kifu_to_kif(kifu_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
