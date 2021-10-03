import os
import glob


def remove_all_temporary(echo=True):
    pattern_list = (
        "./temporary/kif/*.kif",
        "./temporary/kifu/*.kifu",
        "./temporary/pivot/*.json",
        "./temporary/toml/*.toml",
        "./temporary/object/*.kif",
        "./temporary/object/*.kifu",
        "./temporary/object/*.json",
        "./temporary/object/*.toml",
        "./temporary/reverse-kif/*.kif",
        "./temporary/reverse-kifu/*.kifu",
        "./temporary/reverse-pivot/*.json",
        "./temporary/reverse-toml/*.toml",
    )

    for pattern in pattern_list:
        file_list = glob.glob(pattern)
        for file in file_list:
            if echo:
                print(f"Remove: {file}")
            os.remove(file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    remove_all_temporary()
