import glob
from kifu_to_pivot import convert_kifu_to_pivot
from kif_to_kifu import convert_kif_to_kifu
from kif_to_kifu import copy_kif_from_input


def convert_kif_to_pivot(kifFile, output_folder='pivot'):
    kifuFile, doneKifFile = convert_kif_to_kifu(kifFile)
    if kifuFile is None:
        return None, None

    pivotFile, _doneKifuFile = convert_kifu_to_pivot(
        kifuFile, output_folder=output_folder)
    # print(f'kifu={kifuFile} pivot={pivotFile}')
    return pivotFile, doneKifFile


def main():
    copy_kif_from_input()

    # KIFファイル一覧
    kif_files = glob.glob("./kif/*.kif")
    for kif_file in kif_files:
        _pivotFile, _doneKifFile = convert_kif_to_pivot(
            kif_file, output_folder='output')


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
