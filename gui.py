import sys
import tkinter as tk
import tkinter.ttk as ttk

values = ('Shogi-dokoro', 'Shogi GUI')


"""
                 2  2     2  2         4  4
      1          1  2     6  7         7  8
   0  0          0  0     0  0         0  0
  0+--------------------------------------+
   |                                      |
 10|  +----------+           +---------+  |
   |  | Japanese |           | English |  |
 30|  +----------+           +---------+  |
 40|  +----------+           +---------+  |
   |  | Japanese |           | English |  |
 60|  +----------+           +---------+  |
 70|  +----------+           +---------+  |
   |  |          |           |         |  |
160|  |          |  +-----+  |         |  |
   |  |          |  | --> |  |         |  |
190|  |          |  +-----+  |         |  |
210|  |          |  +-----+  |         |  |
   |  |          |  | <-- |  |         |  |
240|  |          |  +-----+  |         |  |
   |  |          |           |         |  |
350|  +----------+           +---------+  |
   |                                      |
360+--------------------------------------+
"""
scale = 2

window = tk.Tk()
window.title(u"Tkinter practice")
# window.geometry("480x360")
window.geometry("960x720")

# 左コンボボックス
left_combobox_value = tk.StringVar()
left_combobox_value.set("Shogi-dokoro")
left_combobox = ttk.Combobox(
    window, height=3, textvariable=left_combobox_value, values=values)
left_combobox.place(x=10*scale, y=10*scale, width=200*scale, height=20*scale)

# 右コンボボックス
right_combobox_value = tk.StringVar()
right_combobox_value.set("Shogi GUI")
right_combobox = ttk.Combobox(
    window, height=3, textvariable=right_combobox_value, values=values)
right_combobox.place(x=270*scale, y=10*scale, width=200*scale, height=20*scale)

# 左テキストボックス
left_text_box = tk.Entry(window)
left_text_box.place(x=10*scale, y=40*scale, width=200*scale, height=20*scale)
left_text_box.insert(tk.END, "demo_in[shogigui]")

# 右テキストボックス
right_text_box = tk.Entry(window)
right_text_box.place(x=270*scale, y=40*scale, width=200*scale, height=20*scale)
right_text_box.insert(tk.END, "demo_out[shogidokoro]")

# 左テキストエリア
left_text_area = tk.Text(window)
left_text_area.place(x=10*scale, y=70*scale, width=200*scale, height=280*scale)

# 右テキストエリア
right_text_area = tk.Text(window)
right_text_area.place(x=270*scale, y=70*scale,
                      width=200*scale, height=280*scale)


def copy_left_to_right():
    """左のテキストボックスの内容を、右のテキストボックスにコピーする機能"""
    global left_text_area, right_text_area
    right_text_area.delete('1.0', 'end')
    text = left_text_area.get("1.0", 'end-1c')
    right_text_area.insert("1.0", text)


def copy_right_to_left():
    """右のテキストボックスの内容を、左のテキストボックスにコピーする機能"""
    global right_text_area, left_text_area
    left_text_area.delete('1.0', 'end')
    text = right_text_area.get("1.0", 'end-1c')
    left_text_area.insert("1.0", text)


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
