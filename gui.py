import os
import sys
import tkinter as tk
import tkinter.ttk as ttk


def __main():
    global left_generator_combobox_value, right_generator_combobox_value
    global left_encoding_combobox_value, right_encoding_combobox_value
    global left_file_text_box_value, left_file_text_box, right_file_text_box_value, right_file_text_box
    global left_text_area, right_text_area

    generator_name_list = ('Shogi-dokoro', 'Shogi GUI')
    encoding_name_list = ('KIFU (UTF-8)', 'KIF (Shift-JIS)')

    """
    .                2  2     2  2         4  4
    ......1          1  2     6  7         7  8
    ...0  0          0  0     0  0         0  0
    ..0+--------------------------------------+
    ...|                                      |
    .10|  +----------+           +---------+  |
    ...|  | Japanese |           | English |  |
    .30|  +----------+           +---------+  |
    .40|  +----------+           +---------+  |
    ...|  | KIFU     |           | KIF     |  |
    .60|  +----------+           +---------+  |
    .70|  +----------+           +---------+  |
    ...|  | File1    |           | File2   |  |
    .90|  +----------+           +---------+  |
    100|  +----------+           +---------+  |
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
    # window.geometry("480x360")
    window.geometry("960x720")

    # 左コンボボックス（ジェネレーター名）
    left_generator_combobox_value = tk.StringVar()
    left_generator_combobox_value.set("Shogi GUI")
    left_generator_combobox = ttk.Combobox(
        window, height=3, textvariable=left_generator_combobox_value, values=generator_name_list)
    left_generator_combobox.place(x=10*scale, y=10*scale,
                                  width=200*scale, height=20*scale)
    left_generator_combobox.bind(
        '<<ComboboxSelected>>', left_generator_combobox_selected)

    # 右コンボボックス（ジェネレーター名）
    right_generator_combobox_value = tk.StringVar()
    right_generator_combobox_value.set("Shogi-dokoro")
    right_generator_combobox = ttk.Combobox(
        window, height=3, textvariable=right_generator_combobox_value, values=generator_name_list)
    right_generator_combobox.place(x=270*scale, y=10*scale,
                                   width=200*scale, height=20*scale)
    right_generator_combobox.bind(
        '<<ComboboxSelected>>', right_generator_combobox_selected)

    # 左コンボボックス（エンコーディング）
    left_encoding_combobox_value = tk.StringVar()
    left_encoding_combobox_value.set("KIFU (UTF-8)")
    left_encoding_combobox = ttk.Combobox(
        window, height=3, textvariable=left_encoding_combobox_value, values=encoding_name_list)
    left_encoding_combobox.place(x=10*scale, y=40*scale,
                                 width=200*scale, height=20*scale)
    left_encoding_combobox.bind(
        '<<ComboboxSelected>>', left_encoding_combobox_selected)

    # 右コンボボックス（エンコーディング）
    right_encoding_combobox_value = tk.StringVar()
    right_encoding_combobox_value.set("KIFU (UTF-8)")
    right_encoding_combobox = ttk.Combobox(
        window, height=3, textvariable=right_encoding_combobox_value, values=encoding_name_list)
    right_encoding_combobox.place(x=270*scale, y=40*scale,
                                  width=200*scale, height=20*scale)
    right_encoding_combobox.bind(
        '<<ComboboxSelected>>', right_encoding_combobox_selected)

    # 左テキストボックス2（ファイル名）
    left_file_text_box_value = tk.StringVar()
    left_file_text_box = tk.Entry(
        window, textvariable=left_file_text_box_value)
    left_file_text_box.place(x=10*scale, y=70*scale,
                             width=200*scale, height=20*scale)
    left_file_text_box.insert(tk.END, "demo-left[shogigui].kifu")

    # 右テキストボックス2（ファイル名）
    right_file_text_box_value = tk.StringVar()
    right_file_text_box = tk.Entry(
        window, textvariable=right_file_text_box_value)
    right_file_text_box.place(x=270*scale, y=70*scale,
                              width=200*scale, height=20*scale)
    right_file_text_box.insert(tk.END, "demo-right[shogidokoro].kifu")

    # 左テキストエリア
    left_text_area = tk.Text(window)
    left_text_area.place(x=10*scale, y=100*scale,
                         width=200*scale, height=250*scale)

    # 右テキストエリア
    right_text_area = tk.Text(window)
    right_text_area.place(x=270*scale, y=100*scale,
                          width=200*scale, height=250*scale)

    # [-->]ボタン
    left_to_right_button = ttk.Button(
        window, text='-->', command=copy_left_to_right)
    left_to_right_button.place(x=220*scale, y=160*scale,
                               width=40*scale, height=30*scale)
    # [<--]ボタン
    right_to_left_button = ttk.Button(
        window, text='<--', command=copy_right_to_left)
    right_to_left_button.place(x=220*scale, y=210*scale,
                               width=40*scale, height=30*scale)

    window.mainloop()


def left_generator_combobox_selected(e):
    filename = create_left_file_name()
    left_file_text_box_value.set(filename)


def right_generator_combobox_selected(e):
    filename = create_right_file_name()
    right_file_text_box_value.set(filename)


def left_encoding_combobox_selected(e):
    filename = create_left_file_name()
    left_file_text_box_value.set(filename)


def right_encoding_combobox_selected(e):
    filename = create_right_file_name()
    right_file_text_box_value.set(filename)


def create_left_file_name():
    global left_generator_combobox_value, left_encoding_combobox_value
    filename = "demo-left"
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
    filename = "demo-right"
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


def copy_left_to_right():
    """左のテキストボックスの内容を、右のテキストボックスにコピーする機能"""
    global left_file_text_box_value, left_text_area, right_text_area
    # TODO 左のテキストボックスの内容を
    content = left_text_area.get("1.0", 'end-1c')
    print(f"content=[{content}]")
    # TODO 📂`input` へ保存します
    left_filename = left_file_text_box_value.get()
    print(f"left_filename=[{left_filename}]")

    try:
        basename = os.path.basename(left_filename)
    except:
        print(
            f"Basename fail. left_filename={left_filename} except={sys.exc_info()[0]}")
        raise

    # TODO ファイル単位で翻訳します
    # TODO 📂`output` に出来ているファイルを読み込み、右のテキストボックスへ出力します
    right_text_area.delete('1.0', 'end')
    text = left_text_area.get("1.0", 'end-1c')
    right_text_area.insert("1.0", text)


def copy_right_to_left():
    """右のテキストボックスの内容を、左のテキストボックスにコピーする機能"""
    global right_text_area, left_text_area
    left_text_area.delete('1.0', 'end')
    text = right_text_area.get("1.0", 'end-1c')
    left_text_area.insert("1.0", text)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    __main()
