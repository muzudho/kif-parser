import glob
import re
import os

__handicap = re.compile(r"^手合割：(.+)$")

def main():
    # KIFUファイル一覧
    files = glob.glob("./kifu/*")
    for file in files:

        # basename
        basename = os.path.basename(file)
        _stem, extention = os.path.splitext(basename)
        if extention.lower() != '.kifu':
            return

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
