# kif-parser

WIP 作業中です。  

将棋ソフト間で受け渡しされる棋譜ファイル形式（`.kif`, `.kifu`）の仕様のゆらぎを解決するためのプログラムです。  
ShogiGUI で作成した `.kifu` ファイルを、 将棋所のフォーマットに変換したり、その逆ができます。  
このアプリケーションは 翻訳 に似ています  

現在対応を進めているのは２ソフトです

* [将棋所](http://shogidokoro.starfree.jp/)
* [ShogiGUI](http://shogigui.siganus.com/)

## Attention（注意）

初めに注意。  
棋譜ファイルはバックアップを残しておいてください。  
このアプリケーションでは、棋譜ファイルのコピーを利用してください。  

## Set up（設定）

```shell
python.exe is_ready.py
# または
is_ready.py
```

👆 [Python3](https://www.python.org/)をインストールして、`is_ready.py` スクリプトを実行してください

```shell
readyok
```

👆 問題なければ `readyok` と表示されます

## Smoke test（最初の動作確認）

このアプリケーションの最上位ディレクトリーに  

* 📄`20211002_223506_KifuwarabeW31B22vsKifuwarabeW31B22[shogigui].kif`
* 📄`20211002_223506_KifuwarabeW31B22vsKifuwarabeW31B22[shogigui].kifu`

という KIFファイルと、 KIFUファイル を置いてあります。  
これは ShogiGUI で出力したファイルですが、これを 将棋所 のフォーマットに変換する例を示します  

同じく最上位ディレクトリーに 📂`input` フォルダーがありますので、ここに 📄`20211002_223506_KifuwarabeW31B22vsKifuwarabeW31B22[shogigui].kif` のコピーを置いてください。  
このアプリケーションで棋譜ファイルを使う（翻訳する）場合、必ずバックアップを取っておいて コピーの方を使ってください  

以下のコマンドを打鍵してください  

```shell
python.exe translate.py -s kif -d kifu -t shogidokoro
                        ------ ------- --------------
                        1      2       3
```

1. `-s kif` - 変換前は kif 形式です。他に `kifu` を指定できます
2. `-d kifu` - 変換後は kifu 形式です。他に `kif` を指定できます
3. `-t shogidokoro` - 変換後は 将棋所のフォーマットにします。他に `shogigui` を指定できます

そのあと、同じく最上位ディレクトリーの 📂`output` フォルダーの中を確認してください。以下のファイルが生成されています  

* `20211002_223506_KifuwarabeW31B22vsKifuwarabeW31B22[shogidokoro].kifu`

ファイルを１つ１つ指定することはできず、フォルダーの中にあるファイルがすべて翻訳の対象になります  

## Danger（危険）

危険な操作を先に覚えてしまいましょう  

### 翻訳の過程で作られる一時ファイルを全部残す

```shell
python.exe translate.py -s kif -d kifu -t shogidokoro --debug
                                                      -------
                                                      1
```

1. `--debug` - 翻訳の途中で大量の一時ファイルを作りますが、それを消さずに残します

以下のフォルダーの中を確認してみてください

* 📂`temporary/to-pivot/kif`
* 📂`temporary/to-pivot/kifu`
* 📂`temporary/to-pivot/object`
* 📂`temporary/to-pivot/reverse-kifu`
* 📂`temporary/to-pivot/reverse-kif`
* 📂`temporary/output-pivot`
* 📂`temporary/from-pivot/pivot`
* 📂`temporary/from-pivot/reverse-pivot`

### inputフォルダーの中のファイル消す

📂`input` フォルダーの中の棋譜ファイルを削除するコマンドは以下の通りです  

```shell
python.exe debug.py --rmin
                    ------
                    1
```

* `--rmin` - remove input の略語。inputフォルダーの中の `.kif`, `.kifu`, `.json`, `.toml` ファイルを削除します

他に 📂`output`フォルダーの中を消す `--rmout`、  
📂`temporary`フォルダーの中を消す `--rmtmp` オプションもあります

フォルダーのクリアーは、翻訳のあとに行われます

## Documents

未整理  

* 📖　[.kifファイルの問題点の洗い出し](./docs/research.md)
* 📖　[.kifファイルの利用実態の調査](./docs/examples)
* .KIF に変わる棋譜保存フォーマット仕様の提案、および　その変換アルゴリズム。
* 📖　[.kifファイルの国際化に向けた翻訳について](./docs/translation.md)
* 📖　[kif-parser の展望](./docs/vision.md)  
* 📖　[kif-parser 開発者向けドキュメント](./docs/developer.md)  

## Other site documents

📖　[棋譜ファイル KIF 形式](http://kakinoki.o.oo7.jp/kif_format.html) - オリジナルである柿木将棋での仕様  
📖　[分岐棋譜→単一棋譜変換プログラム](http://www.hakusa.net/computer/free/kifuconv.html) - 白砂 青松によるオリジナルにはない「変化」の説明。2004年  
📖　[KIF形式を調べようぜ（＾～＾）？](https://crieit.net/drafts/6150ffc21e0de)  
📖　[将棋の符号](https://crieit.net/drafts/615192ae93d14)  
📖　[Kif](https://lishogi.org/explanation/kif) - lishogiによる KIFフォーマットの説明  
