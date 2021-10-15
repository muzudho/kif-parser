import os
import sys
import tomli


def convert_toml_to_pivot(toml_file, output_folder):
    """.tomlファイルを読込んで、JSON (PIVOT) ファイルを出力します"""

    data = {}

    # basename
    try:
        basename = os.path.basename(toml_file)
    except:
        print(f"Error: toml_file={toml_file} except={sys.exc_info()[0]}")
        raise

    stem, extention = os.path.splitext(basename)
    if extention.lower() != '.toml':
        return

    # insert new extention
    out_path = os.path.join(output_folder, f"{stem}.json")

    # とりあえず KIFU を読んでみます
    row_number = 1
    with open(toml_file, encoding='utf-8') as f:

        s = f.read()
        text = s.rstrip()

        try:
            # tomliは、コメントの読込をサポートしないとのこと
            toml_dict = tomli.loads(text)

            # 日付のところが `datetime.time(0, 0)` と出力される
            print(f"toml_dict={toml_dict}")

        except tomli.TOMLDecodeError:
            # 構文エラーなど
            print(f"Yep, definitely not valid. toml_file={toml_file}")
            raise

        return None
