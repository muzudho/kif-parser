# kif-parser

作業中です。

`.kif` は、本将棋の棋譜のファイル フォーマットです  

* [.kifファイルの問題点の洗い出し](./docs/research.md)
* [.kifファイルの利用実態の調査](./docs/examples/README.md)
* .KIF に変わる棋譜保存フォーマット仕様の提案、および　その変換アルゴリズム。

## KIF から KIFU へ変換

1. 📂`input` フォルダーに 📄`*.kif` ファイルをたくさん入れてください
2. ターミナルで `python.exe kif_to_kifu.py` コマンドを実行してください
3. UTF-8形式に変換して 📂`output` へ 📄`*.kifu` が出力されます
4. ゴミファイルが溜まっているので消すために、`python.exe remove_all_temporary.py` コマンドを実行してください

## KIFU から KIF へ変換

1. 📂`input` フォルダーに 📄`*.kifu` ファイルをたくさん入れてください
2. ターミナルで `python.exe kifu_to_kif.py` コマンドを実行してください
3. Shift-JIS形式に変換して 📂`output` へ 📄`*.kif` が出力されます
4. ゴミファイルが溜まっているので消すために、`python.exe remove_all_temporary.py` コマンドを実行してください

## Documents

📖　[kif-parser の展望](./docs/vision.md)  
📖　[kif-parser 開発者向けドキュメント](./docs/developer.md)  

## Other site documents

📖　[棋譜ファイル KIF 形式](http://kakinoki.o.oo7.jp/kif_format.html) - オリジナルである柿木将棋での仕様  
📖　[分岐棋譜→単一棋譜変換プログラム](http://www.hakusa.net/computer/free/kifuconv.html) - オリジナルにはない「変化」の説明  
📖　[KIF形式を調べようぜ（＾～＾）？](https://crieit.net/drafts/6150ffc21e0de)  
📖　[将棋の符号](https://crieit.net/drafts/615192ae93d14)  
