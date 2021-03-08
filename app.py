# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, send_file, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os
import flask
import pretty_midi
import shutil
import mc_note_functionner
import delay

app = flask.Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/mc-note-functionner', methods=['GET'])
def index2():
    return render_template("index2.html")

@app.route('/matcha-shaders', methods=['GET'])
def shaders():
    return render_template("shaders.html")

@app.route('/matcha-shaders/download', methods=['GET'])
def shaders_download():
    return send_file("./matcha-shaders-v1.0.zip", as_attachment = True, \
        attachment_filename = "matcha-shaders-v1.0.zip")

@app.route('/upload', methods=['POST'])
def upload(): 
    if 'file' not in flask.request.files:
        return 'ファイル未指定'
    fs = flask.request.files['file']
    fs.save("./midi_file.mid")
    mc_note_functionner.create_function()
    return send_file("./note.zip", as_attachment = True, \
        attachment_filename = "note.zip")

@app.route("/hr-delay", methods=['GET'])
def hr_pass_get():
	return '''
	<form action="/hr-delay" method="POST" enctype="multipart/form-data">
	<div> <input type="password" id="pass" name="pass" placeholder="PASSWORD"> </div>
	<div> <input type="submit" value="認証"> </div>
	</form>
	'''

@app.route("/hr-delay", methods=['POST'])
def hr_pass_post():
	pw = request.form['pass']
	if(pw == "OkudairaIsGod"):
		DELAY = delay.ret_delay()
		return DELAY
	else:
		return '''
		<p>パスワードが違います。</p>
		<form action="/hr-delay" method="POST" enctype="multipart/form-data">
	<div> <input type="password" id="pass" name="pass" placeholder="PASSWORD"> </div>
	<div> <input type="submit" value="認証"> </div>
	</form>
		'''



@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html")

if __name__ == '__main__':
    app.run()
