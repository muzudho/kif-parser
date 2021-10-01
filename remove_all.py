import os
import glob


def main():
    # KIFファイル一覧
    kif_files = glob.glob("./temporary/kif/*.kif")
    for kif_file in kif_files:
        print(f"Remove: {kif_file}")
        os.remove(kif_file)

    # KIFファイル一覧
    kif_files = glob.glob("./temporary/kif-done/*.kif")
    for kif_file in kif_files:
        print(f"Remove: {kif_file}")
        os.remove(kif_file)

    # KIFUファイル一覧
    kifu_files = glob.glob("./temporary/kifu/*.kifu")
    for kifu_file in kifu_files:
        print(f"Remove: {kifu_file}")
        os.remove(kifu_file)

    # KIFUファイル一覧
    kifu_files = glob.glob("./temporary/kifu-done/*.kifu")
    for kifu_file in kifu_files:
        print(f"Remove: {kifu_file}")
        os.remove(kifu_file)

    # PIVOTファイル一覧
    pivot_files = glob.glob("./temporary/pivot/*.json")
    for pivot_file in pivot_files:
        print(f"Remove: {pivot_file}")
        os.remove(pivot_file)

    # PIVOTファイル一覧
    pivot_files = glob.glob("./temporary/pivot-done/*.json")
    for pivot_file in pivot_files:
        print(f"Remove: {pivot_file}")
        os.remove(pivot_file)

    # TOMLファイル一覧
    toml_files = glob.glob("./temporary/toml_d/*.toml")
    for toml_file in toml_files:
        print(f"Remove: {toml_file}")
        os.remove(toml_file)

    # PIVOTファイル一覧
    toml_files = glob.glob("./temporary/toml-done/*.toml")
    for toml_file in toml_files:
        print(f"Remove: {toml_file}")
        os.remove(toml_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
