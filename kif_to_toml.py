import glob
from kif_to_kifu import copy_kif_from_input
from kif_to_pivot import convert_kif_to_pivot
from pivot_to_toml import convert_pivot_to_toml


def main():
    copy_kif_from_input()

    # KIFファイル一覧
    kif_files = glob.glob("./temporary/kif/*.kif")
    for kif_file in kif_files:
        pivot_file, _doneKifFile = convert_kif_to_pivot(
            kif_file, output_folder='output')
        if pivot_file is None:
            continue

        _tomlFile, _done_pivot_file = convert_pivot_to_toml(
            pivot_file, 'output')


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
