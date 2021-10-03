import os
import codecs
import sys


def convert_kifu_to_kif(kifu_file, output_folder):
    """(1) kifu_file(*.kifu)ファイルを読み取ります
    (2) *.kifファイルを kif フォルダーへ生成します
    (3) 読み終えた *.kifuファイルは done_folder フォルダーへ移動します

    Returns
    -------
    str
        新しいパス。
        KIFUファイルでなかったなら空文字列
    """

    kif_file = ""

    # シフトJISエンコードのテキストファイルの読み込み
    with codecs.open(kifu_file, "r", encoding='utf-8') as f:

        # basename
        try:
            basename = os.path.basename(kifu_file)
        except:
            print(f"Error: kifu_file={kifu_file} except={sys.exc_info()[0]}")
            raise

        stem, extention = os.path.splitext(basename)
        if extention.lower() != '.kifu':
            return ""

        # New file
        kif_file = os.path.join(output_folder, f"{stem}.kif")

        with codecs.open(kif_file, "w", encoding='shift_jis') as fOut:

            # UTF-8形式に変換して保存
            for row in f:
                fOut.write(row)

    return kif_file
