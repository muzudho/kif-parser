import os

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    readyok = True

    directory_list = (
        "temporary/from-pivot/kif",
        "temporary/from-pivot/kifu",
        "temporary/from-pivot/pivot",
        "temporary/from-pivot/toml",
        "temporary/from-pivot/object",
        "temporary/from-pivot/object",
        "temporary/from-pivot/object",
        "temporary/from-pivot/object",
        "temporary/from-pivot/reverse-kif",
        "temporary/from-pivot/reverse-kifu",
        "temporary/from-pivot/reverse-pivot",
        "temporary/from-pivot/reverse-toml",

        "temporary/no-pivot/kif",
        "temporary/no-pivot/kifu",
        "temporary/no-pivot/pivot",
        "temporary/no-pivot/toml",
        "temporary/no-pivot/object",
        "temporary/no-pivot/object",
        "temporary/no-pivot/object",
        "temporary/no-pivot/object",
        "temporary/no-pivot/reverse-kif",
        "temporary/no-pivot/reverse-kifu",
        "temporary/no-pivot/reverse-pivot",
        "temporary/no-pivot/reverse-toml",

        "temporary/output-pivot",

        "temporary/to-pivot/kif",
        "temporary/to-pivot/kifu",
        "temporary/to-pivot/pivot",
        "temporary/to-pivot/toml",
        "temporary/to-pivot/object",
        "temporary/to-pivot/object",
        "temporary/to-pivot/object",
        "temporary/to-pivot/object",
        "temporary/to-pivot/reverse-kif",
        "temporary/to-pivot/reverse-kifu",
        "temporary/to-pivot/reverse-pivot",
        "temporary/to-pivot/reverse-toml",
    )

    for directory in directory_list:
        if not os.path.isdir(directory):
            print(f"Not found directory: {directory}")
            readyok = False

    if readyok:
        print("readyok")
