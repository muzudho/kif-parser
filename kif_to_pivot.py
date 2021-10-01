import glob
from kifu_to_pivot import convert_kifu_to_pivot
from kif_to_kifu import convert_kif_to_kifu
from kif_to_kifu import copy_kif_from_input


def convert_kif_to_pivot(kif_file, output_folder='temporary/pivot'):
    kifu_file, doneKifFile = convert_kif_to_kifu(kif_file)
    if kifu_file is None:
        return None, None

    pivot_file, _doneKifuFile = convert_kifu_to_pivot(
        kifu_file, output_folder=output_folder)
    if pivot_file is None:
        return None, None

    # print(f'kifu_file={kifu_file} pivot_file={pivot_file}')
    return pivot_file, doneKifFile


def main():
    copy_kif_from_input()

    # KIFファイル一覧
    kif_files = glob.glob("./temporary/kif/*.kif")
    for kif_file in kif_files:
        _pivotFile, _doneKifFile = convert_kif_to_pivot(
            kif_file, output_folder='output')


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
