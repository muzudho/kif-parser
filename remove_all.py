import os
import glob


def main():
    # KIFファイル一覧
    kif_files = glob.glob("./kif/*.kif")
    for kif_file in kif_files:
        print(f"Remove: {kif_file}")
        os.remove(kif_file)

    # KIFファイル一覧
    kif_files = glob.glob("./kif-done/*.kif")
    for kif_file in kif_files:
        print(f"Remove: {kif_file}")
        os.remove(kif_file)

    # KIFUファイル一覧
    kifu_files = glob.glob("./kifu/*.kifu")
    for kifu_file in kifu_files:
        print(f"Remove: {kifu_file}")
        os.remove(kifu_file)

    # KIFUファイル一覧
    kifu_files = glob.glob("./kifu-done/*.kifu")
    for kifu_file in kifu_files:
        print(f"Remove: {kifu_file}")
        os.remove(kifu_file)

    # PIBOTファイル一覧
    pivot_files = glob.glob("./pivot/*.json")
    for pivot_file in pivot_files:
        print(f"Remove: {pivot_file}")
        os.remove(pivot_file)

    # PIBOTファイル一覧
    pivot_files = glob.glob("./pivot-done/*.json")
    for pivot_file in pivot_files:
        print(f"Remove: {pivot_file}")
        os.remove(pivot_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
