# Examples - .kifファイルの利用実態の調査

`.kif` ファイル（Shift-JIS）は文字化けして不便なので、 `.kifu` ファイル（UTF-8）に変換して説明します  

## [shogidokoro-wcsc31]20210503_191257 AI_AN_shogi_ver1 vs Kifuwarabe.kifu

第31回世界コンピュータ将棋選手権（WCSC31）に出場したした きふわらべ が用いたGUIである 将棋所 から出力した棋譜です。  

## [wcsc31]WCSC31_L8_ANS_KFW_1.csa

ちなみに WCSC31 の [インターネット中継サイト](http://live4.computer-shogi.org/wcsc31/) からダウンロードできる棋譜は  
`.csa` 形式です。  
CSA形式は コンピューター将棋ソフト同士が通信対局を行うためのフォーマットであり、  
指し手のコメントが書き込めないことが 棋譜ファイルとしての普及に向いていません。  

## [floodgate]wdoor+floodgate-300-10F+Titanda_L+SILENT_MAJORITY_sf170225_6950XEE+20170302210003.csa

[floodgate](http://wdoor.c.u-tokyo.ac.jp/shogi/) では 拡張CSA形式の `.csa` フォーマットの棋譜ファイルをダウンロードできます。  
これは CSA形式に 評価値、読み筋、コメントを追加できるようにしたものです。  
[電王トーナメント](https://denou.jp/tournament2017/) や、 [電竜戦](https://denryu-sen.jp/) でも使われています。  

## [shogigui]20211002_223506_KifuwarabeW31B22vsKifuwarabeW31B22.kif

ShogiGUI で WCSC31の きふわらべ を自己対局させた `.kif` ファイルを `.kifu` へ変換したものです。  
