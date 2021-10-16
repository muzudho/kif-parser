import re

__state = None
__subState = None
__text = None
__row_number = None

__row_number_pattern = re.compile(r'^    "(\d+)": \{$')
# Example: `        "num": "270",`
__move_number_pattern = re.compile(r'^        "num": "(\d+)",$')
# Example: `            0,`
# Example: `            0`
__time_number_pattern = re.compile(r'^            (\d+)(,?)$')


def format_data_json(text):
    global __row_number, __state, __subState, __text

    lines = text.split("\n")
    __state = "<None>"
    __subState = "<None>"
    __text = ""

    for line in lines:

        # [Debug]
        # __text += f"{__state} {__subState}"

        result = __row_number_pattern.match(line)
        if result:
            # 行番号
            # =====
            __row_number = int(result.group(1))
            digits = number_digits(__row_number)
            padding = "".ljust(5-digits)
            __text += f'    {padding}"{__row_number}": {{\n'
        elif line == "}":
            # 最後の閉じかっこ
            __text += f"\n{line.lstrip()}"
        elif __state == "<Comment>" or __state == "<KvPair>" or __state == "<MovesHeader>" or __state == "<Explain>":
            comment_type(line)
        elif __state == "<Move>":
            if __subState == "<Move.Move>":
                move_move_type(line)
            elif __subState == "<Move.Time>":
                move_time_type(line)
            elif __subState == "<Move.Total>":
                move_total_type(line)
            elif line.startswith('        "num":'):
                result = __move_number_pattern.match(line)
                if result:
                    num = int(result.group(1))
                    padding = number_digits(num)
                    # 上の行にくる type の右にくっつきます
                    __text = __text.rstrip()
                    # 書き直します
                    spaces = "".ljust(3-padding)
                    __text += f'"num":{spaces}"{num}",'
            elif line == '        "m": {':
                __text = __text.rstrip()
                __text += f"{line.lstrip()}"
                __subState = "<Move.Move>"
            elif line == '        "time": [':
                __text = __text.rstrip()
                __text += f"{line.lstrip()}"
                __subState = "<Move.Time>"
            elif line == '        "total": [':
                # 上の行にある Time の右にくっつくようにします
                __text += f"{line.lstrip()}"
                __subState = "<Move.Total>"
            elif line == '    },':
                # おわり
                __text = __text.rstrip()
                __text += f"{line.lstrip()}\n"
                __state = "<None>"
                __subState = "<None>"
            else:
                raise ValueError(f"[ERROR] [{line}]\n")
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
                # 下の行にくる num を右にくっつけます
                __text = __text.rstrip()
                __text += f"{line.strip()} "
                __state = "<Move>"
            else:
                __text += f"{line}\n"
        # print(f"[line] {line}")
    # print(f"[__text] {__text}")
    return __text


def comment_type(line):
    global __state, __subState, __text

    if line == "    },":
        __text = __text.rstrip()
        __text += f"{line.lstrip()}\n"
        __state = "<None>"
    else:
        __text += f"{line.lstrip()} "


def move_move_type(line):
    global __state, __subState, __text

    if line == "        },":
        __text = __text.rstrip()
        __text += f"{line.lstrip()}\n"
        __subState = "<None>"
    else:
        __text += f"{line.lstrip()} "


def move_time_type(line):
    global __state, __subState, __text

    if line == "        ],":  # 末尾にカンマが付いている
        __text = __text.rstrip()
        # 次にくる Total を右にくっつけます
        __text += f"{line.lstrip()} "
        __subState = "<None>"
    else:
        result = __time_number_pattern.match(line)
        if result:
            number = int(result.group(1))
            comma = result.group(2)
            digits = number_digits(number)
            padding = "".ljust(2-digits)
            __text += f"{padding}{number}{comma}"
        # __text += f"{line.lstrip()} "


def move_total_type(line):
    global __state, __subState, __text

    if line == "        ]":  # 末尾にカンマが付いていない
        __text = __text.rstrip()
        __text += f"{line.lstrip()}\n"
        __subState = "<None>"
    else:
        result = __time_number_pattern.match(line)
        if result:
            number = int(result.group(1))
            comma = result.group(2)
            digits = number_digits(number)
            padding = "".ljust(2-digits)
            __text += f"{padding}{number}{comma}"
        # __text += f"{line.lstrip()} "


def number_digits(number: int):
    """数の桁数を返します"""

    # 行番号が1桁のとき7
    if number is None:
        digits = 0
    elif number < 10:
        digits = 1
    elif number < 100:
        digits = 2
    elif number < 1000:
        digits = 3
    elif number < 10000:
        digits = 4
    else:
        digits = 5

    return digits
