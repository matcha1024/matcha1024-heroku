# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os
import flask
import pretty_midi
import shutil

app = flask.Flask(__name__)

# フォーム表示
@app.route('/', methods=['GET'])
def index():
	return '''
	<head>
    <meta name="description" content="Minecraftの音ブロック演奏を自動生成します。">
		<style>
		@import url('https://fonts.googleapis.com/css?family=Exo:400,700');


button {
    /* 文字サイズを1.4emに指定 */
    font-size: 1.4em;

    /* 文字の太さをboldに指定 */
    font-weight: bold;

    /* 縦方向に10px、
     * 横方向に30pxの余白を指定 */
    padding: 10px 30px;

    /* 背景色を濃い青色に指定 */
    background-color: #248;

    /* 文字色を白色に指定 */
    color: #fff;

    /* ボーダーをなくす */
    border-style: none;
}

button:hover {
    /* 背景色を明るい青色に指定 */
    background-color: #24d;

    /* 文字色を白色に指定 */
    color: #fff;
}

*{
    margin: 0px;
    padding: 0px;
}

body{
    font-family: 'Exo', sans-serif;
}


.context {
    width: 100%;
    position: absolute;
    top:10vh;
    text-align: center;
}

.context h1{
    text-align: center;
    color: #fff;
    font-size: 50px;
}

.context h2{
    text-align: center;
    font-size: 30px;
}

.context iframe{
    text-align: center;
}

.context a{
	background-color: #248;
    text-align: center;
    font-size: 30px;
    color:#fff
}

.context a:hover{
    background-color: #24d;
    color: #fff;
}

.area{
	pointer-events: none;
    background: #4e54c8;  
    background: -webkit-linear-gradient(to left, #8f94fb, #4e54c8);  
    width: 100%;
    height:250vh;
    
   
}

.circles{
	pointer-events: none;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.circles li{
    position: absolute;
    display: block;
    list-style: none;
    width: 20px;
    height: 20px;
    background: rgba(255, 255, 255, 0.2);
    animation: animate 25s linear infinite;
    bottom: -150px;
    
}

.circles li:nth-child(1){
    left: 25%;
    width: 80px;
    height: 80px;
    animation-delay: 0s;
}


.circles li:nth-child(2){
    left: 10%;
    width: 20px;
    height: 20px;
    animation-delay: 2s;
    animation-duration: 12s;
}

.circles li:nth-child(3){
    left: 70%;
    width: 20px;
    height: 20px;
    animation-delay: 4s;
}

.circles li:nth-child(4){
    left: 40%;
    width: 60px;
    height: 60px;
    animation-delay: 0s;
    animation-duration: 18s;
}

.circles li:nth-child(5){
    left: 65%;
    width: 20px;
    height: 20px;
    animation-delay: 0s;
}

.circles li:nth-child(6){
    left: 75%;
    width: 110px;
    height: 110px;
    animation-delay: 3s;
}

.circles li:nth-child(7){
    left: 35%;
    width: 150px;
    height: 150px;
    animation-delay: 7s;
}

.circles li:nth-child(8){
    left: 50%;
    width: 25px;
    height: 25px;
    animation-delay: 15s;
    animation-duration: 45s;
}

.circles li:nth-child(9){
    left: 20%;
    width: 15px;
    height: 15px;
    animation-delay: 2s;
    animation-duration: 35s;
}

.circles li:nth-child(10){
    left: 85%;
    width: 150px;
    height: 150px;
    animation-delay: 0s;
    animation-duration: 11s;
}

.circles2{
    pointer-events: none;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 250%;
    overflow: hidden;
}

.circles2 li{
    position: absolute;
    display: block;
    list-style: none;
    width: 20px;
    height: 20px;
    background: rgba(255, 255, 255, 0.2);
    animation: animate 25s linear infinite;
    bottom: -150px;
    
}

.circles2 li:nth-child(1){
    left: 25%;
    width: 80px;
    height: 80px;
    animation-delay: 0s;
}


.circles2 li:nth-child(2){
    left: 10%;
    width: 20px;
    height: 20px;
    animation-delay: 2s;
    animation-duration: 12s;
}

.circles2 li:nth-child(3){
    left: 70%;
    width: 20px;
    height: 20px;
    animation-delay: 4s;
}

.circles2 li:nth-child(4){
    left: 40%;
    width: 60px;
    height: 60px;
    animation-delay: 0s;
    animation-duration: 18s;
}

.circles2 li:nth-child(5){
    left: 65%;
    width: 20px;
    height: 20px;
    animation-delay: 0s;
}

.circles2 li:nth-child(6){
    left: 75%;
    width: 110px;
    height: 110px;
    animation-delay: 3s;
}

.circles2 li:nth-child(7){
    left: 35%;
    width: 150px;
    height: 150px;
    animation-delay: 7s;
}

.circles2 li:nth-child(8){
    left: 50%;
    width: 25px;
    height: 25px;
    animation-delay: 15s;
    animation-duration: 45s;
}

.circles2 li:nth-child(9){
    left: 20%;
    width: 15px;
    height: 15px;
    animation-delay: 2s;
    animation-duration: 35s;
}

.circles2 li:nth-child(10){
    left: 85%;
    width: 150px;
    height: 150px;
    animation-delay: 0s;
    animation-duration: 11s;
}

.circles3{
    pointer-events: none;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 175%;
    overflow: hidden;
}

.circles3 li{
    position: absolute;
    display: block;
    list-style: none;
    width: 20px;
    height: 20px;
    background: rgba(255, 255, 255, 0.2);
    animation: animate 25s linear infinite;
    bottom: -150px;
    
}

.circles3 li:nth-child(1){
    left: 25%;
    width: 80px;
    height: 80px;
    animation-delay: 0s;
}


.circles3 li:nth-child(2){
    left: 10%;
    width: 20px;
    height: 20px;
    animation-delay: 2s;
    animation-duration: 12s;
}

.circles3 li:nth-child(3){
    left: 70%;
    width: 20px;
    height: 20px;
    animation-delay: 4s;
}

.circles3 li:nth-child(4){
    left: 40%;
    width: 60px;
    height: 60px;
    animation-delay: 0s;
    animation-duration: 18s;
}

.circles3 li:nth-child(5){
    left: 65%;
    width: 20px;
    height: 20px;
    animation-delay: 0s;
}

.circles3 li:nth-child(6){
    left: 75%;
    width: 110px;
    height: 110px;
    animation-delay: 3s;
}

.circles3 li:nth-child(7){
    left: 35%;
    width: 150px;
    height: 150px;
    animation-delay: 7s;
}

.circles3 li:nth-child(8){
    left: 50%;
    width: 25px;
    height: 25px;
    animation-delay: 15s;
    animation-duration: 45s;
}

.circles3 li:nth-child(9){
    left: 20%;
    width: 15px;
    height: 15px;
    animation-delay: 2s;
    animation-duration: 35s;
}

.circles3 li:nth-child(10){
    left: 85%;
    width: 150px;
    height: 150px;
    animation-delay: 0s;
    animation-duration: 11s;
}


@keyframes animate {

    0%{
        transform: translateY(0) rotate(0deg);
        opacity: 1;
        border-radius: 0;
    }

    100%{
        transform: translateY(-1000px) rotate(720deg);
        opacity: 0;
        border-radius: 50%;
    }

}
</style>
	<title>MC Note Functioner</title>
	</head>
	<body>
	<div class="context">
	<form method="post" action="/upload" enctype="multipart/form-data">
	  <input type="file" name="file">
	  <button>Upload</button>
	</form>
		<h1>使い方</h1>
		<h2>1.midiファイルをアップロードして、ダウンロードされたnote.zipを解凍します。</h2>
		<h2>2.フォルダ:noteをマインクラフトのdatapackフォルダに入れます。</h2>
		<h2>3.マインクラフト内で/function note:startを実行することで演奏が開始します。</h2>
		<h2>4./function note:stopを実行することで演奏が停止します。</h2>
		<h1>アップデート</h1>
		<h2>2021/01/18/0:21：演奏が開始されないバグを修正しました。</h2>
		<h2>2021/01/18/1:26：音程を改善しました。<h2>
		<p>2021/01/18/1:26：note:stopを追加しました。</p>
		<h1>YouTube:</h1>
		<iframe width="560" height="315" src="https://www.youtube.com/embed/vcqT1Di1CDM" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
		<h1>演奏例</h1>
		<h2>最終鬼畜姉妹フランドール・S</h2>
		<iframe width="560" height="315" src="https://www.youtube.com/embed/PYhc8vX1DuA" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
		<h2>unravel</h2>
		<iframe width="560" height="315" src="https://www.youtube.com/embed/adPjYUovu-Q" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
		<h2>夜明けの蛍</h2>
		<iframe width="560" height="315" src="https://www.youtube.com/embed/KmT0csiabkE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        <a href="https://twitter.com/matcha_1024"><br>ご連絡はTwitterDMまで</a>

        </div>
		<div class="area" >
            <ul class="circles">
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
            </ul>
            <ul class="circles2">
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
            </ul>
            <ul class="circles3">
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
            </ul>
    </div >
    </body>
'''

@app.route('/upload', methods=['POST'])
def upload(): 
	if 'file' not in flask.request.files:
		return 'ファイル未指定'
	fs = flask.request.files['file']
	fs.save("./midi_file.mid")

	PITCH = {0:0.67, 1:0.710, 2:0.714, 3:0.718, 4:0.84, 5:0.89, 6:0.5, 7:0.53, 8:0.56, 9:0.59, 10:0.63, 11:0.67, 12:0.71, 13:0.714, 14:0.79, 15:0.84, 16:0.9, 17:0.95, 18:1, 19:1.05, 20:1.13, 21:1.18, 22:1.25, 23:1.33, 24:1.4, 25:1.5, 26:1.57, 27:1.67, 28:1.8, 29:1.9, 30:2, 31:1.05, 32:1.13, 33:1.18, 34:1.25, 35:1.33}

	midi_data = pretty_midi.PrettyMIDI("./midi_file.mid")

	with open("./note/data/note/functions/ontick.mcfunction", "w") as f:
		f.write("scoreboard players add Timer TICK 1\nscoreboard players operation Timer TICK %= Timer 20\nexecute if score Timer TICK matches 0 unless score Timer SECOND matches -1 run scoreboard players add Timer SECOND 1\n")
		for instrument in midi_data.instruments:
			if not instrument.is_drum:
				time = instrument.get_onsets()
				i = 0
				for note in instrument.notes:
					f.write(f"execute at @a run execute if score Timer SECOND matches {int(time[i]*20)} run playsound minecraft:block.note_block.harp master @a ~ ~ ~ 1 {PITCH[int(note.pitch) % 36]}\n")

					i += 1


	shutil.make_archive("note", "zip", root_dir = "./note")

	return send_file("./note.zip", as_attachment = True, \
        attachment_filename = "note.zip")
if __name__ == '__main__':
	app.run()