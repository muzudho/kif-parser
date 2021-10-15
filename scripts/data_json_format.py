def format_data_json(text):
    lines = text.split("\n")
    text = ""
    state = "<None>"
    for line in lines:
        if state == "<Comment>" or state == "<KvPair>" or state == "<MovesHeader>" or state == "<Explain>":
            if line == "    },":
                text = text.rstrip()
                text += f"{line.lstrip()}\n"
                state = "<None>"
            else:
                text += f"{line.lstrip()} "
        elif state == "<Move>":
            if line == "        },":
                text = text.rstrip()
                text += f"{line.lstrip()}\n"
                state = "<None>"
            else:
                text += f"{line.lstrip()} "
        elif state == "<Time>":
            if line == "        },":  # 末尾にカンマが付いている
                text = text.rstrip()
                # 次にくる Total を右にくっつけます
                text += f"{line.lstrip()} "
                state = "<None>"
            else:
                text += f"{line.lstrip()} "
        elif state == "<Total>":
            if line == "        }":  # 末尾にカンマが付いていない
                text = text.rstrip()
                text += f"{line.lstrip()}\n"
                state = "<None>"
            else:
                text += f"{line.lstrip()} "
        else:
            if line == '        "type": "comment",':
                state = "<Comment>"
                text = text.rstrip()
                text += f"{line.lstrip()} "
            elif line == '        "type": "kvPair",':
                state = "<KvPair>"
                text = text.rstrip()
                text += f"{line.lstrip()} "
            elif line == '        "type": "movesHeader",':
                state = "<MovesHeader>"
                text = text.rstrip()
                text += f"{line.lstrip()} "
            elif line == '        "type": "explain",':
                state = "<Explain>"
                text = text.rstrip()
                text += f"{line.lstrip()} "
            elif line == '        "type": "move",':
                # 上の行にくる `    "7": {` といったものの右にくっつき、
                # 下の行にくる moveNum を右にくっつけます
                text = text.rstrip()
                text += f"{line.strip()} "
            elif line.startswith('        "moveNum":'):
                # 上の行にくる type の右にくっつきます
                text += f"{line.lstrip()}\n"
            elif line == '        "move": {':
                state = "<Move>"
                text += f"{line}"
            elif line == '        "time": {':
                state = "<Time>"
                text += f"{line}"
            elif line == '        "total": {':
                state = "<Total>"
                # 上の行にある Time の右にくっつくようにします
                text += f"{line.lstrip()}"
            else:
                text += f"{line}\n"
        # print(f"[line] {line}")
    # print(f"[text] {text}")
    return text
