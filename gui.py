import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from translate import Translator
from scripts.generator_identification import GeneratorIdentification


def __main():
    global left_generator_combobox_value, right_generator_combobox_value
    global left_stem_text_box_value
    global left_encoding_combobox_value
    global right_encoding_combobox_value
    global left_file_text_box_value, left_file_text_box, right_file_text_box_value, right_file_text_box
    global left_text_area, right_text_area

    generator_name_list = ('Shogi-dokoro', 'Shogi GUI')
    encoding_name_list = ('KIFU (UTF-8)', 'KIF (Shift-JIS)')

    """
    .            1   2  2     2  2         4  4
    ......1      5   1  2     6  7         7  8
    ...0  0      0   0  0     0  0         0  0
    ..0+--------------------------------------+
    ...|                                      |
    .10|  +----------+           +---------+  |
    ...|  | Japanese |           | English |  |
    .25|  +----------+           +---------+  |
    .30|  +----------+                        |
    ...|  | Stem     |                        |
    .45|  +----------+                        |
    .50|  +----------+           +---------+  |
    ...|  | KIFU     |           | KIF     |  |
    .65|  +----------+           +---------+  |
    .70|  +----------+           +---------+  |
    ...|  | File1    |           | File2   |  |
     85|  +----------+           +---------+  |
    .90|         +---+                        |
    ...|         |Btn|                        |
    105|         +---+                        |
    110|  +----------+           +---------+  |
    ...|  |          |           |         |  |
    160|  |          |  +-----+  |         |  |
    ...|  |          |  | --> |  |         |  |
    190|  |          |  +-----+  |         |  |
    210|  |          |  +-----+  |         |  |
    ...|  |          |  | <-- |  |         |  |
    240|  |          |  +-----+  |         |  |
    ...|  |          |           |         |  |
    350|  +----------+           +---------+  |
    ...|                                      |
    360+--------------------------------------+
    """
    scale = 2

    window = tk.Tk()
    window.title(u"Tkinter practice")
    window.geometry("960x720")  # 2倍のスケール

    # 値を前もって用意（再計算が先に働いてしまう前に）
    left_generator_combobox_value = tk.StringVar()
    right_generator_combobox_value = tk.StringVar()
    left_stem_text_box_value = tk.StringVar()
    left_encoding_combobox_value = tk.StringVar()
    right_encoding_combobox_value = tk.StringVar()
    left_file_text_box_value = tk.StringVar()
    right_file_text_box_value = tk.StringVar()

    # 左コンボボックス（ジェネレーター名）
    left_generator_combobox_value.set("Shogi GUI")
    left_generator_combobox = ttk.Combobox(
        window, height=3, textvariable=left_generator_combobox_value, values=generator_name_list)
    left_generator_combobox.place(x=10*scale, y=10*scale,
                                  width=200*scale, height=15*scale)
    left_generator_combobox.bind(
        '<<ComboboxSelected>>', left_generator_combobox_selected)

    # 右コンボボックス（ジェネレーター名）
    right_generator_combobox_value.set("Shogi-dokoro")
    right_generator_combobox = ttk.Combobox(
        window, height=3, textvariable=right_generator_combobox_value, values=generator_name_list)
    right_generator_combobox.place(x=270*scale, y=10*scale,
                                   width=200*scale, height=15*scale)
    right_generator_combobox.bind(
        '<<ComboboxSelected>>', right_generator_combobox_selected)

    # 左テキストボックス1（ファイル名基幹部）
    left_stem_text_box_value.trace("w", on_left_stem_text_box_value_changed)
    left_stem_text_box = tk.Entry(
        window, textvariable=left_stem_text_box_value)
    left_stem_text_box.place(x=10*scale, y=30*scale,
                             width=200*scale, height=15*scale)
    left_stem_text_box.insert(tk.END, "demo")

    # 左コンボボックス（エンコーディング）
    left_encoding_combobox_value.set("KIFU (UTF-8)")
    left_encoding_combobox = ttk.Combobox(
        window, height=3, textvariable=left_encoding_combobox_value, values=encoding_name_list)
    left_encoding_combobox.place(x=10*scale, y=50*scale,
                                 width=200*scale, height=15*scale)
    left_encoding_combobox.bind(
        '<<ComboboxSelected>>', left_encoding_combobox_selected)

    # 右コンボボックス（エンコーディング）
    right_encoding_combobox_value.set("KIFU (UTF-8)")
    right_encoding_combobox = ttk.Combobox(
        window, height=3, textvariable=right_encoding_combobox_value, values=encoding_name_list)
    right_encoding_combobox.place(x=270*scale, y=50*scale,
                                  width=200*scale, height=15*scale)
    right_encoding_combobox.bind(
        '<<ComboboxSelected>>', right_encoding_combobox_selected)

    # 左テキストボックス2（ファイル名）
    left_file_text_box = tk.Entry(
        window, textvariable=left_file_text_box_value)
    left_file_text_box.place(x=10*scale, y=70*scale,
                             width=200*scale, height=15*scale)
    left_file_text_box.configure(state='readonly')

    # 右テキストボックス2（ファイル名）
    right_file_text_box = tk.Entry(
        window, textvariable=right_file_text_box_value)
    right_file_text_box.place(x=270*scale, y=70*scale,
                              width=200*scale, height=15*scale)
    right_file_text_box.configure(state='readonly')

    # [↑フォーマット推測]ボタン
    left_to_right_button = ttk.Button(
        window, text='↑フォーマット推測', command=recognition)
    left_to_right_button.place(x=150*scale, y=90*scale,
                               width=60*scale, height=15*scale)

    # 左テキストエリア
    left_text_area = tk.Text(window)
    left_text_area.place(x=10*scale, y=110*scale,
                         width=200*scale, height=240*scale)

    # 右テキストエリア
    right_text_area = tk.Text(window)
    right_text_area.place(x=270*scale, y=110*scale,
                          width=200*scale, height=240*scale)

    # [-->]ボタン
    left_to_right_button = ttk.Button(
        window, text='-->', command=copy_left_to_right)
    left_to_right_button.place(x=220*scale, y=160*scale,
                               width=40*scale, height=30*scale)
    # [<--]ボタン
    # right_to_left_button = ttk.Button(
    #    window, text='<--', command=copy_right_to_left)
    # right_to_left_button.place(x=220*scale, y=210*scale,
    #                           width=40*scale, height=30*scale)
    # right_to_left_button.configure(state='readonly')  # WIP まだできてない

    window.mainloop()


def left_generator_combobox_selected(e):
    filename = create_left_file_name()
    left_file_text_box_value.set(filename)


def right_generator_combobox_selected(e):
    filename = create_right_file_name()
    right_file_text_box_value.set(filename)


def on_left_stem_text_box_value_changed(*args):
    left_filename = create_left_file_name()
    left_file_text_box_value.set(left_filename)
    right_filename = create_right_file_name()
    right_file_text_box_value.set(right_filename)


def left_encoding_combobox_selected(e):
    filename = create_left_file_name()
    left_file_text_box_value.set(filename)


def right_encoding_combobox_selected(e):
    filename = create_right_file_name()
    right_file_text_box_value.set(filename)


def create_left_file_name():
    global left_generator_combobox_value
    global left_encoding_combobox_value

    filename = "input/"
    stem = left_stem_text_box_value.get()
    filename += stem

    generator = left_generator_combobox_value.get()
    if generator == "Shogi GUI":
        filename += "[shogigui]"
    else:
        filename += "[shogidokoro]"

    encoding = left_encoding_combobox_value.get()
    if encoding == "KIF (Shift-JIS)":
        filename += ".kif"
    else:
        filename += ".kifu"
    return filename


def create_right_file_name():
    global right_generator_combobox_value, right_encoding_combobox_value
    filename = "output/"
    stem = left_stem_text_box_value.get()  # 左のを使う
    filename += stem
    generator = right_generator_combobox_value.get()
    if generator == "Shogi GUI":
        filename += "[shogigui]"
    else:
        filename += "[shogidokoro]"
    encoding = right_encoding_combobox_value.get()
    if encoding == "KIF (Shift-JIS)":
        filename += ".kif"
    else:
        filename += ".kifu"
    return filename


def recognition():
    """TODO フォーマット認識ボタン"""
    global left_generator_combobox_value
    global left_text_area
    global left_file_text_box_value
    global right_file_text_box_value
    left_textbox_content = left_text_area.get("1.0", 'end-1c')
    generator_identification = GeneratorIdentification()
    generator_identification.read_all_text(left_textbox_content)
    print(
        f'[DEBUG] shogidokoro={generator_identification._Y["shogidokoro"]} shogigui={generator_identification._Y["shogigui"]}')

    best_key = "shogidokoro"
    best_value = -1
    for key, value in generator_identification._Y.items():
        if best_value < value:
            best_key = key
            best_value = value

    print(
        f'[DEBUG] best_key={best_key} best_value={best_value}')

    # 再計算は自動でしてくれないみたいだ
    if best_key == "shogigui":
        left_generator_combobox_value.set("Shogi GUI")
    else:
        left_generator_combobox_value.set("Shogi-dokoro")

    # 再計算
    left_filename = create_left_file_name()
    left_file_text_box_value.set(left_filename)
    right_filename = create_right_file_name()
    right_file_text_box_value.set(right_filename)


def copy_left_to_right():
    """左のテキストボックスの内容を、右のテキストボックスにコピーする機能"""
    global left_generator_combobox_value
    global right_generator_combobox_value
    global left_encoding_combobox_value, right_encoding_combobox_value
    global left_file_text_box_value
    global left_text_area
    global right_file_text_box_value
    global right_text_area
    # 左のテキストボックスの内容を
    left_textbox_content = left_text_area.get("1.0", 'end-1c')
    # print(f"left_textbox_content=[{left_textbox_content}]")
    # 📂`input` へ保存します
    input_filename = left_file_text_box_value.get()
    print(f"input_filename=[{input_filename}]")

    try:
        basename = os.path.basename(input_filename)
    except:
        print(
            f"Basename fail. input_filename={input_filename} except={sys.exc_info()[0]}")
        raise

    stem, extention = os.path.splitext(basename)
    if extention == ".kif":
        # UTF-8 --> Shift-JIS 変換して保存
        # TODO UTF-8 から Shift-JIS へ変換できない文字（波線）などが現れた時、エラーにならないように何とかしたい
        left_text_encoding = 'shift_jis'
    else:
        # TODO BOM付きにも対応したい
        left_text_encoding = 'utf-8'

    with open(input_filename, "w", encoding=left_text_encoding) as f_out:
        # TODO 改行コードがUnixになったりする（＾～＾）
        f_out.write(left_textbox_content)

    # TODO 翻訳ツール作成
    left_generator = left_generator_combobox_value.get()
    if left_generator == "Shogi GUI":
        source_template = "shogigui"
    else:
        source_template = "shogidokoro"
    right_generator = right_generator_combobox_value.get()
    if right_generator == "Shogi GUI":
        destination_template = "shogigui"
    else:
        destination_template = "shogidokoro"
    left_encoding = left_encoding_combobox_value.get()
    if left_encoding == "KIF (Shift-JIS)":
        source = "kif"
    else:
        source = "kifu"
    right_encoding = right_encoding_combobox_value.get()
    if right_encoding == "KIF (Shift-JIS)":
        destination = "kif"
    else:
        destination = "kifu"

    print(
        f"[TRACE] source=[{source}] destination=[{destination}] source_template=[{source_template}] destination_template=[{destination_template}]")
    translator = Translator(source=source, destination=destination,
                            source_template=source_template, destination_template=destination_template, debug=True)

    # TODO ファイル単位で翻訳します
    translator.translate_file(input_filename)

    # TODO 📂`output` に出来ているファイルを読み込み
    output_filename = right_file_text_box_value.get()
    try:
        basename = os.path.basename(output_filename)
    except:
        print(
            f"Basename fail. output_filename={output_filename} except={sys.exc_info()[0]}")
        raise

    stem, extention = os.path.splitext(basename)
    if extention == ".kif":
        # UTF-8 --> Shift-JIS 変換して保存
        # TODO UTF-8 から Shift-JIS へ変換できない文字（波線）などが現れた時、エラーにならないように何とかしたい
        encoding = 'shift_jis'
    else:
        # TODO BOM付きにも対応したい
        encoding = 'utf-8'

    with open(input_filename, "r", encoding=encoding) as f_in:
        text = ""
        for row in f_in:
            text += row
        right_text_area.delete('1.0', 'end')
        right_text_area.insert("1.0", text)


def copy_right_to_left():
    """WIP 右のテキストボックスの内容を、左のテキストボックスにコピーする機能"""
    pass
    # global right_text_area, left_text_area
    # left_text_area.delete('1.0', 'end')
    # text = right_text_area.get("1.0", 'end-1c')
    # left_text_area.insert("1.0", text)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    __main()
