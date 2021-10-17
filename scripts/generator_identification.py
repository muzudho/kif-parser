import re


class GeneratorIdentification():
    """棋譜を生成したソフトらしさを類推します"""

    def __init__(self):
        # Example: `   1 ７六歩(77)        ( 0:00/00:00:00)` の `( 0:00/00:00:00)` の部分を当てにいきます
        self._shogi_gui_time_stamp = re.compile(
            r"^.*\(\s\d:\d{2}/\d{2}:\d{2}:\d{2}\)$")

        # Result
        self._Y = {
            "shogidokoro": 0,
            "shogigui": 0,
        }

    @property
    def Y(self):
        """Result"""
        return self._Y

    def read_all_text(self, text):
        """テキストを読込ませてください"""

        shogi_gui_time_stamp_flag = False

        lines = text.split('\n')
        for line in lines:
            result = self._shogi_gui_time_stamp.match(line)
            if result:
                shogi_gui_time_stamp_flag = True
            pass

        self._Y["shogidokoro"] = 1
        self._Y["shogigui"] = 0

        if shogi_gui_time_stamp_flag:
            self._Y["shogigui"] += 10
