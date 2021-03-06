# Research - .kifファイルの問題点の洗い出し

## .kif について、こんな人は困っていない

将棋を観る人、将棋を指す人、将棋を検討する人は困っていません  

│  
│ `.kif` ファイルを Shogi GUI にドラッグ＆ドロップしたり、  
│ [名前を付けて保存] するだけです  
│  

主に作るものが思考エンジンの人、ベテランのGUI開発者 は困っていません  

│  
│ 自分でなんとかできてしまうので困っていません。  
│ 自動対局するなら `将棋所` と `USI` プロトコル、  
│ サーバーと直接通信するなら `CSA` プロトコルを使います。  
│ 棋譜ファイルを保存するときは `.kif` を使いますが、  
│ 柿木将棋のホームページの [棋譜コンバータシリーズ (DOS/Windows)](http://kakinoki.o.oo7.jp/) には  
│ `CSAtoK.exe` が、  
│ ak110さんのGit hubには、棋譜変換ツール [Blunder.Converter](https://github.com/ak110/Blunder.Converter) が置いてあります  
│  

## .kif について、こんな人は困っている

これから新しく将棋の GUI や、関連ソフトを作ろうとしている **新規のGUI開発者** の人  

│  
│ 例えば SHOGI-EXTEND さんの [KIF 形式](https://www.shogi-extend.com/adapter/description) を見てください。  
│ 他のソフトで作った `.kif` 拡張子のファイルが読めない、または  
│ その逆に 自分のソフトで作った `.kif` 拡張子のファイルが他のソフトで読めない、  
│ といった不具合連絡を受けても サポートをお断りする作業が増えるばかりかもしれません  
│  

## .kif は何ではない

GUIの設定（文字の大きさや、表示しているウィンドウのサイズ等）を保存するファイルではありません。  
GUIの設定は ソフトが別に設定ファイルを持っています。  

検討用の矢印のようなものは保存しません。  

中将棋など、変則将棋には対応していません。  

## .kif は何である

日本将棋連盟が これが将棋と認める範疇の将棋の棋譜を記録します。  
駒落ち将棋、詰将棋にも対応します。  
アマチュア、プロの両方に対応します。  

対局情報を持つことができ、その対局情報や 指し手に対してコメントを付けることができます。  
特に **指し手へのコメント** は 将棋の勉強や 記者の記事などのエンターテイメントに使われ、重要です。  
（プログラム用語でいうコメントとは別に、解説の意味でのコメントがあり、後者を指します）  

しおり（頭出しするラベルのようなもの）を 指し手に付けることができます。  

オリジナルの仕様にはない拡張として、  
変化手順（ジャンプ先ラベルのようなもの、また そこから続く棋譜）を 本譜の後ろに付けることができます。  


## .kif ファイル

![20210929shogi7-kif.png](../docs/img/20210929shogi7-kif-50per.png)  
👆 `.kif` ファイル  

* 😌 国産の既存のGUIで普及していると思います。  
  「あのソフトで動かない！」という形で普及を目にすることになるでしょう。  
  このサポートの負荷が一番大きな問題だと考えます。  
  そもそも これが .kif か？ というファイルが出回っているようです
* 🙃 柿木将棋が .kif 形式のオリジナルですが、  
  柿木将棋が対応していない「変化手順」の仕様が普及しています  
* 😁 文字エンコーディングが Shift-JIS です。  
  国際化に向いていなさそうですが、海外の人は  
  後述の `.kifu` ファイルを使うので、これは それほど大きな問題ではありません
* 😁 漢字を使います。  
  ただし、 `.kif` ファイルをテキストエディターで直接編集している利用者はほぼおらず、  
  ShogiGUIなどのソフトへ入力し、ソフトで編集、出力するだけと聞きます。  
  今は優先順位としては小さな問題です

`.kif` ファイルの仕様

* [棋譜ファイル KIF 形式](http://kakinoki.o.oo7.jp/kif_format.html) - オリジナル
* [KIF 形式](https://www.shogi-extend.com/adapter/description) - 変則的な書式の説明

`.kif` 形式を使っているソフトの例:  

* [柿木将棋](http://kakinoki.o.oo7.jp/) - .kif 形式のオリジナル。 しかし「変化」手順は仕様にありません
* [将棋所](http://shogidokoro.starfree.jp/)
* [Shogi GUI](http://shogigui.siganus.com/)
* [将棋ウォーズ](https://shogiwars.heroz.jp/?locale=ja)

`.kif` 形式のファイルを配布しているサイトの例:  

* [floodgate](http://wdoor.c.u-tokyo.ac.jp/shogi/floodgate.html)
* [世界コンピュータ将棋選手権](http://www2.computer-shogi.org/)
* [将棋電王トーナメント](https://denou.jp/tournament2017/)
* [世界将棋AI 電竜戦](https://denryu-sen.jp/)

## .kifu ファイル

![20210929shogi8-kifu.png](../docs/img/20210929shogi8-kifu-50per.png)  
👆 `.kifu` ファイル  

* 😙 `.kif` を UTF-8 に変換したファイルです。  
  海外で 将棋ソフトが普及しておらず、  
  肝心の 柿木将棋 は現在 Busy で乗換が進んでいません
* 😌 そもそも `.kif` の仕様が まばらであることが  
  解決していません
* 😁 漢字を使います

`.kifu` 形式のファイルを配布しているサイトの例:  

* [lishogi.org](https://lishogi.org/)  
