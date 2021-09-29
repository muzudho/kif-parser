import glob
from pibot_to_kifu import convert_pibot_to_kifu
from kifu_to_kif import convert_kifu_to_kif


def main():
    # KIFファイル一覧
    pibotFiles = glob.glob("./pibot/*")
    for pibotFile in pibotFiles:
        kifuFile, _donePibotFile = convert_pibot_to_kifu(pibotFile)

        # kifu to kif
        _kifFile, _donePath = convert_kifu_to_kif(kifuFile)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
