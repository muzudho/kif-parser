# kif-parser

WIP 作業中です。  

このプロジェクトは、（仕様のあいまいさを積極的に包容していることで賛否がある） `.kif` ファイルの **将棋ソフト開発者の新規参入が難しい現状** を打開するための方法の提案と、その方法を実装している途中の パーサーです。  
`.kif` は、本将棋の棋譜のファイル フォーマットです。  

作戦名は `ローカル.kif仕様書ジェネレーター` です。  

アイデアとしては `.kif` ファイルの内容を解析するのではなく、 `.kif` ファイルの書式の方を解析し、 `ローカル .kif 仕様書` とでもいうようなものを生成（TODO この部分がまだできていません）、  
この仕様書を自動生成するツールと、 `ローカル .kif 仕様書` に従って `.kif` ファイルの解析をするツールの２つを **新規の将棋ソフト開発者** にオープンソース、フリーウェアで配ってしまえば、  
「ソフトAで作った `.kif` ファイルがあなたの作った将棋ソフトで読めません」「あなたのソフトで作った `.kif` ファイルは A というソフトで読めません」という責任を  
この muzudho/kif-parser に丸投げできるという段取りです。  

その **書式の解析** をする方法としては、ソフトA に `.kif` ファイルを出力させます。  
muzudho/kif-parser が その `.kif` の書式を解析します。（TODO この部分がまだできていません）  
ソフトA が出力した書式の `.kif` を ソフトA が読込めないというのは考えづらいことから、 ソフトA が読込める `.kif` を生成できるはずです。  
これで ソフトA は攻略です。 これを出会った全ソフトに対して行えば打開完了です。  

こうなってくれば、 `.kif` (Shift-JIS) を変換した `.kifu` (UTF-8) を使い続けても問題ありません。  
これは時間稼ぎで、何かしらの **プロパティファイル** 、例えば `.json` など 構文が厳密な仕様にスライドするのが適当ですが、  
既存のソフトが 仕様の固まっていない JSON に対応するとも思えません。ひとまず時間稼ぎです。  

muzudho/kif-parser の内部では `.json` を使い始めています。  
移行先（その２）のプロパティファイルには `.toml` を考えています。  

* [.kifファイルの問題点の洗い出し](./docs/research.md)
* [.kifファイルの利用実態の調査](./docs/examples)
* .KIF に変わる棋譜保存フォーマット仕様の提案、および　その変換アルゴリズム。
* [.kifファイルの国際化に向けた翻訳について](./docs/translation.md)

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
    pivot_to_toml.py
    remove_all_output.py
    remove_all_temporary.py
    toml_to_pivot.py
```

## KIF から KIFU へ変換

1. 📂`input` フォルダーに 📄`*.kif` ファイルをたくさん入れてください
2. ターミナルで `python.exe kif_to_kifu.py` コマンドを実行してください
3. 📄`input/*.kif` は UTF-8形式に変換して 📂`output` へ 📄`*.kifu` が出力されます

## KIFU から KIF へ変換

1. 📂`input` フォルダーに 📄`*.kifu` ファイルをたくさん入れてください
2. ターミナルで `python.exe kifu_to_kif.py` コマンドを実行してください
3. 📄`input/*.kifu` は Shift-JIS形式に変換して 📂`output` へ 📄`*.kif` が出力されます

## Documents

📖　[kif-parser の展望](./docs/vision.md)  
📖　[kif-parser 開発者向けドキュメント](./docs/developer.md)  

## Other site documents

📖　[棋譜ファイル KIF 形式](http://kakinoki.o.oo7.jp/kif_format.html) - オリジナルである柿木将棋での仕様  
📖　[分岐棋譜→単一棋譜変換プログラム](http://www.hakusa.net/computer/free/kifuconv.html) - オリジナルにはない「変化」の説明  
📖　[KIF形式を調べようぜ（＾～＾）？](https://crieit.net/drafts/6150ffc21e0de)  
📖　[将棋の符号](https://crieit.net/drafts/615192ae93d14)  
