import glob
from kifu_to_pivot import convert_kifu_to_pivot
from kif_to_kifu import convert_kif_to_kifu


def convert_kif_to_pivot(kifFile):
    kifuFile, doneKifFile = convert_kif_to_kifu(kifFile)
    if kifuFile is None:
        return None, None

    if kifuFile:
        pivotFile, _doneKifuFile = convert_kifu_to_pivot(kifuFile)
        # print(f'kifu={kifuFile} pivot={pivotFile}')
        return pivotFile, doneKifFile

    return None, None


def main():
    # KIFファイル一覧
    kif_files = glob.glob("./kif/*.kif")
    for kif_file in kif_files:
        _pivotFile, _doneKifFile = convert_kif_to_pivot(kif_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
