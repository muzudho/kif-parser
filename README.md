# kif-parser

WIP 作業中です。  

* 📖　[.kifファイルの問題点の洗い出し](./docs/research.md)
* 📖　[.kifファイルの利用実態の調査](./docs/examples)
* .KIF に変わる棋譜保存フォーマット仕様の提案、および　その変換アルゴリズム。
* 📖　[.kifファイルの国際化に向けた翻訳について](./docs/translation.md)
* 📖　[kif-parser の展望](./docs/vision.md)  
* 📖　[kif-parser 開発者向けドキュメント](./docs/developer.md)  

## Set up - このスクリプトの使い方

初めに注意。  
棋譜ファイルは別にバックアップを残しておいてください。  
このアプリケーションでは、棋譜ファイルのコピーを利用してください。  
`*_danger.py` は 📂`input` フォルダーの内容を破壊します。誤ってダブルクリックすることのないようにしましょう。  

**Python 3** を使いこなすスキルがあるものとします。  
リリース時に必要なフォルダー階層は以下の通りです  

```plain
/kif-parser
    /input
        # ここに *.kif, *.kifu, *.toml, *.json のいずれかを置きます
    /output
        # ここに変換後のファイルが出力されます。スクリプト実行時にここに置いてある棋譜ファイルは削除されます
    /scripts
        # このなかに ファイルを変換するプログラムが大量に入っています
    /temporary # このフォルダーの下で棋譜ファイルのコピー、編集、削除が行われます
        /kif
        /kifu
        /pivot
        /toml
        /object # 中間ファイル
        /reverse-kif # 可逆変換テスト
        /reverse-kifu
        /reverse-pivot
        /reverse-toml

    kif_to_kifu.py    # `*_to_*.py` は、用途により使わないものもあるかも知れません
    kif_to_pivot.py
    kif_to_toml.py
    kifu_to_kif.py
    kifu_to_pivot.py
    LICENSE
    pivot_to_kif.py
    pivot_to_kifu.py
    pivot_to_toml.py # WIP 作業中
    remove_all_output.py
    remove_all_temporary.py
    toml_to_pivot.py
```

## KIF から KIFU へ変換（またその逆）

1. 📂`input` フォルダーに 📄`*.kif` ファイルをたくさん入れてください
2. ターミナルで `python.exe kif_to_kifu.py` コマンドを実行してください
3. 📄`input/*.kif` は UTF-8形式に変換して 📂`output` へ 📄`*.kifu` が出力されます

同様に、逆の操作として `python.exe kifu_to_kif.py` というコマンドがあります  


## KIF から PIVOT へ変換

1. 📂`input` フォルダーに `*.kif` ファイルをたくさん入れてください
2. ターミナルで `python.exe kif_to_pivot.py` コマンドを実行してください
3. JSON形式に変換して 📂`output` へ 📄`*.json` （PIVOT）が出力されます

同様に、逆の操作として `python.exe kifu_to_pivot.py` というコマンドがあります

## PIVOT から KIF へ変換

1. 📂`input` フォルダーに `*.json` 形式のPIVOTファイルをたくさん入れてください
2. ターミナルで `python.exe pivot_to_kif.py` コマンドを実行してください
3. KIF形式に変換して 📂`output` へ 📄`*.kif` が出力されます

同様に、逆の操作として `python.exe pivot_to_kifu.py` というコマンドがあります

## Other site documents

📖　[棋譜ファイル KIF 形式](http://kakinoki.o.oo7.jp/kif_format.html) - オリジナルである柿木将棋での仕様  
📖　[分岐棋譜→単一棋譜変換プログラム](http://www.hakusa.net/computer/free/kifuconv.html) - オリジナルにはない「変化」の説明  
📖　[KIF形式を調べようぜ（＾～＾）？](https://crieit.net/drafts/6150ffc21e0de)  
📖　[将棋の符号](https://crieit.net/drafts/615192ae93d14)  
