import glob
from kifu_to_pivot import convert_kifu_to_pivot
from kif_to_kifu import convert_kif_to_kifu_file


def convert_kif_to_pivot(kifFile):
    kifuFile, doneKifFile = convert_kif_to_kifu_file(kifFile)
    if kifuFile is None:
        return None, None

    if kifuFile:
        pivotFile, _doneKifuFile = convert_kifu_to_pivot(kifuFile)
        # print(f'kifu={kifuFile} pivot={pivotFile}')
        return pivotFile, doneKifFile

    return None, None


def main():
    # KIFファイル一覧
    kifFiles = glob.glob("./kif/*")
    for kifFile in kifFiles:
        _pivotFile, _doneKifFile = convert_kif_to_pivot(kifFile)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
