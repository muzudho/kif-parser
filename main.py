import glob
import shutil
import os
import codecs
import sys
import re

__handicap = re.compile(r"^手合割：(.+)$")

def read_kif_file(path):
    """(1) input フォルダーのKIFファイルを読み取ります
    (2) KIFUファイルを hidden-step1 フォルダーへ生成します
    (3) KIFファイルは input-done フォルダーへ移動します

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
        # Except old extention
        stem, extention = os.path.splitext(basename)
        if extention.lower() != '.kif':
            return ""

        # Append new extention
        basename = f"{stem}.kifu"

        newPath = os.path.join('hidden-step1', basename)

        with codecs.open(newPath, "w", encoding='utf-8') as fOut:

            # UTF-8形式に変換して保存
            for row in f:
                fOut.write(row)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    new_path = shutil.move(path, 'input-kif-done')
    print(new_path)

    return newPath

def main():
    # KIFファイル一覧
    files = glob.glob("./input-kif/*")
    for file in files:
        _newPath = read_kif_file(file)

    # KIFUファイル一覧
    files = glob.glob("./hidden-step1/*")
    for file in files:

        # とりあえず KIFU を読んでみます
        with open(file, encoding='utf-8') as f:
            s = f.read()
            text = s.rstrip()

            lines = text.split('\n')
            for line in lines:

                result = __handicap.match(line)
                if result:
                    handicap = result.group(1)
                    if handicap == '平手':
                        print("★平手 WIP")
                        pass
                    elif handicap == '香落ち':
                        pass
                    elif handicap == '右香落ち':
                        pass
                    elif handicap == '角落ち':
                        pass
                    elif handicap == '飛車落ち':
                        pass
                    elif handicap == '飛香落ち':
                        pass
                    elif handicap == '二枚落ち':
                        pass
                    elif handicap == '三枚落ち':
                        pass
                    elif handicap == '四枚落ち':
                        pass
                    elif handicap == '五枚落ち':
                        pass
                    elif handicap == '左五枚落ち':
                        pass
                    elif handicap == '六枚落ち':
                        pass
                    elif handicap == '左七枚落ち':
                        pass
                    elif handicap == '右七枚落ち':
                        pass
                    elif handicap == '八枚落ち':
                        pass
                    elif handicap == '十枚落ち':
                        pass
                    elif handicap == 'その他':
                        pass

                    continue

                print(f"> [{line}]")

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
