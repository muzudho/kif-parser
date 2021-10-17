import os
import inspect
import codecs
import sys


def convert_kifu_to_kif(input_file, output_folder, debug=False):
    """(1) input_file(*.kifu)ファイルを読み取ります
    (2) *.kifファイルを kif フォルダーへ生成します
    (3) 読み終えた *.kifuファイルは done_folder フォルダーへ移動します

    Returns
    -------
    str
        新しいパス。
        KIFUファイルでなかったなら空文字列
    """

    # BOM付きUTF-8か、BOM無しUTF-8かを見分けます
    if is_utf8_file_with_bom(input_file):
        encoding = 'utf-8-sig'
    else:
        encoding = 'utf-8'

    # シフトJISエンコードのテキストファイルの読み込み
    with codecs.open(input_file, "r", encoding=encoding) as f_in:

        # basename
        try:
            basename = os.path.basename(input_file)
        except:
            print(
                f"Basename fail. input_file={input_file} except={sys.exc_info()[0]}")
            raise

        stem, extention = os.path.splitext(basename)
        if extention.lower() != '.kifu':
            return ""

        # New file
        out_path = os.path.join(output_folder, f"{stem}.kif")

        if debug:
            print(
                f"[DEBUG] {os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}: Write from [{input_file}](UTF-8) to [{out_path}](Shift-JIS)")

        try:
            # TODO UTF-8 から Shift-JIS へ変換できない文字（波線）などが現れた時、エラーにならないように何とかしたい
            with codecs.open(out_path, "w", encoding='shift_jis') as f_out:

                # UTF-8 --> Shift-JIS 変換して保存
                for row in f_in:
                    f_out.write(row)
        except:
            raise ValueError(
                f"Write fail. Write from [{input_file}](UTF-8) to [{out_path}](Shift-JIS)")

    return out_path


def is_utf8_file_with_bom(filename):
    """utf-8 ファイルが BOM ありかどうかを判定します
    📖 [Python Tips： Python で UTF-8 の BOM ありなしを見分けたい](https://www.lifewithpython.com/2017/10/python-detect-bom-in-utf8-file.html)
    """
    line_first = open(filename, encoding='utf-8').readline()
    return (line_first[0] == '\ufeff')
