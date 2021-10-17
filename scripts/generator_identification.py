import re


class GeneratorIdentification():
    """棋譜を生成したソフトらしさを類推します"""

    def __init__(self):
        # Example: `   1 ７六歩(77)        ( 0:00/00:00:00)` の `( 0:00/00:00:00)` の部分を当てにいきます
        self._shogi_gui_time_stamp = re.compile(
            r"^.*\(\s\d:\d{2}/\d{2}:\d{2}:\d{2}\)$")

        # Result
        self._shogidokoro = 0
        self._shogigui = 0

    @property
    def shogidokoro(self):
        return self._shogidokoro

    @property
    def shogigui(self):
        return self._shogigui

    def read_all_text(self, text):
        """テキストを読込ませてください"""

        shogi_gui_time_stamp_flag = False

        lines = text.split('\n')
        for line in lines:
            result = self._shogi_gui_time_stamp.match(line)
            if result:
                shogi_gui_time_stamp_flag = True
            pass

        self._shogidokoro = 1
        self._shogigui = 0

        if shogi_gui_time_stamp_flag:
            self._shogigui += 10
