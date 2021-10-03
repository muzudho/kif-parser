import shutil
import os
import codecs
import sys


def convert_kif_to_kifu(kif_file, output_folder='temporary/kifu'):
    """(1) kif_file(*.kif)ファイルを読み取ります
    (2) *.kifuファイルを output_folder へ生成します

    Returns
    -------
    (str, str)
        出力したkifuファイルへのパス, 読み終えたkifファイルへのパス
        KIFファイルでなかったなら空文字列
    """

    out_path = ""

    # シフトJISエンコードのテキストファイルの読み込み
    with codecs.open(kif_file, "r", encoding='shift_jis') as f:

        # basename
        try:
            basename = os.path.basename(kif_file)
        except:
            print(f"Error: kif_file={kif_file} except={sys.exc_info()[0]}")
            raise

        stem, extention = os.path.splitext(basename)
        if extention.lower() != '.kif':
            return None, None

        # Append new extention
        out_path = os.path.join(output_folder, f"{stem}.kifu")

        with codecs.open(out_path, "w", encoding='utf-8') as fOut:

            # UTF-8形式に変換して保存
            for row in f:
                fOut.write(row)

    return out_path
