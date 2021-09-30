import glob
from pivot_to_kifu import convert_pivot_to_kifu
from kifu_to_kif import convert_kifu_to_kif


def convert_pivot_to_kif(pivotFile):
    kifuFile, donePibotFile = convert_pivot_to_kifu(pivotFile)
    if kifuFile is None:
        return None, None

    # kifu to kif
    kifFile, _doneKifuFile = convert_kifu_to_kif(kifuFile)
    return kifFile, donePibotFile


def main():
    # PIBOTファイル一覧
    pivot_files = glob.glob("./pivot/*.json")
    for pivot_file in pivot_files:
        _kifFile, _donePibotFile = convert_pivot_to_kif(pivot_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
