__state = None
__text = None


def format_data_json(text):
    global __state, __text

    lines = text.split("\n")
    __state = "<None>"
    __text = ""
    for line in lines:
        if line == "}":
            # 最後の閉じかっこ
            __text += f"\n{line.lstrip()}"
        elif __state == "<Comment>" or __state == "<KvPair>" or __state == "<MovesHeader>" or __state == "<Explain>":
            comment_type(line)
        elif __state == "<Move.Move>":
            move_move_type(line)
        elif __state == "<Move.Time>":
            move_time_type(line)
        elif __state == "<Move.Total>":
            move_total_type(line)
        else:
            if line == '        "type": "comment",':
                __state = "<Comment>"
                __text = __text.rstrip()
                __text += f"{line.lstrip()} "
            elif line == '        "type": "kvPair",':
                __state = "<KvPair>"
                __text = __text.rstrip()
                __text += f"{line.lstrip()} "
            elif line == '        "type": "movesHeader",':
                __state = "<MovesHeader>"
                __text = __text.rstrip()
                __text += f"{line.lstrip()} "
            elif line == '        "type": "explain",':
                __state = "<Explain>"
                __text = __text.rstrip()
                __text += f"{line.lstrip()} "
            elif line == '        "type": "move",':
                # 上の行にくる `    "7": {` といったものの右にくっつき、
                # 下の行にくる moveNum を右にくっつけます
                __text = __text.rstrip()
                __text += f"{line.strip()} "
            elif line.startswith('        "moveNum":'):
                # 上の行にくる type の右にくっつきます
                __text += f"{line.lstrip()}\n"
            elif line == '        "move": {':
                __state = "<Move.Move>"
                __text += f"{line}"
            elif line == '        "time": {':
                __state = "<Move.Time>"
                __text += f"{line}"
            elif line == '        "total": {':
                __state = "<Move.Total>"
                # 上の行にある Time の右にくっつくようにします
                __text += f"{line.lstrip()}"
            else:
                __text += f"{line}\n"
        # print(f"[line] {line}")
    # print(f"[__text] {__text}")
    return __text


def comment_type(line):
    global __state, __text

    if line == "    },":
        __text = __text.rstrip()
        __text += f"{line.lstrip()}\n"
        __state = "<None>"
    else:
        __text += f"{line.lstrip()} "


def move_move_type(line):
    global __state, __text

    if line == "        },":
        __text = __text.rstrip()
        __text += f"{line.lstrip()}\n"
        __state = "<None>"
    else:
        __text += f"{line.lstrip()} "


def move_time_type(line):
    global __state, __text

    if line == "        },":  # 末尾にカンマが付いている
        __text = __text.rstrip()
        # 次にくる Total を右にくっつけます
        __text += f"{line.lstrip()} "
        __state = "<None>"
    else:
        __text += f"{line.lstrip()} "


def move_total_type(line):
    global __state, __text

    if line == "        }":  # 末尾にカンマが付いていない
        __text = __text.rstrip()
        __text += f"{line.lstrip()}\n"
        __state = "<None>"
    else:
        __text += f"{line.lstrip()} "
