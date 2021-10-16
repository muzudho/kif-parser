import os
import glob


def remove_all_temporary(echo=True, no_remove_output_pivot=False):
    pattern_list = (
        "temporary/from-pivot/kif/*.kif",
        "temporary/from-pivot/kifu/*.kifu",
        "temporary/from-pivot/pivot/*.json",
        "temporary/from-pivot/toml/*.toml",
        "temporary/from-pivot/object/*.kif",
        "temporary/from-pivot/object/*.kifu",
        "temporary/from-pivot/object/*.json",
        "temporary/from-pivot/object/*.toml",
        "temporary/from-pivot/reverse-kif/*.kif",
        "temporary/from-pivot/reverse-kifu/*.kifu",
        "temporary/from-pivot/reverse-pivot/*.json",
        "temporary/from-pivot/reverse-toml/*.toml",

        "temporary/no-pivot/kif/*.kif",
        "temporary/no-pivot/kifu/*.kifu",
        "temporary/no-pivot/pivot/*.json",
        "temporary/no-pivot/toml/*.toml",
        "temporary/no-pivot/object/*.kif",
        "temporary/no-pivot/object/*.kifu",
        "temporary/no-pivot/object/*.json",
        "temporary/no-pivot/object/*.toml",
        "temporary/no-pivot/reverse-kif/*.kif",
        "temporary/no-pivot/reverse-kifu/*.kifu",
        "temporary/no-pivot/reverse-pivot/*.json",
        "temporary/no-pivot/reverse-toml/*.toml",

        "temporary/to-pivot/kif/*.kif",
        "temporary/to-pivot/kifu/*.kifu",
        "temporary/to-pivot/pivot/*.json",
        "temporary/to-pivot/toml/*.toml",
        "temporary/to-pivot/object/*.kif",
        "temporary/to-pivot/object/*.kifu",
        "temporary/to-pivot/object/*.json",
        "temporary/to-pivot/object/*.toml",
        "temporary/to-pivot/reverse-kif/*.kif",
        "temporary/to-pivot/reverse-kifu/*.kifu",
        "temporary/to-pivot/reverse-pivot/*.json",
        "temporary/to-pivot/reverse-toml/*.toml",
    )

    pattern_list2 = (
        "temporary/output-pivot/*.json",
    )

    for pattern in pattern_list:
        file_list = glob.glob(pattern)
        for file in file_list:
            if echo:
                print(f"Remove: {file}")
            os.remove(file)

    if not no_remove_output_pivot:
        for pattern in pattern_list2:
            file_list = glob.glob(pattern)
            for file in file_list:
                if echo:
                    print(f"Remove: {file}")
                os.remove(file)
