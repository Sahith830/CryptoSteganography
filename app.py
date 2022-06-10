from audioSteganography import decodeAudio, encodeAudio
from numpy import asarray
from PIL import Image
import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template,send_file
from werkzeug.utils import secure_filename
import sqlite3
from imageSteganography import encrypt,decrypt
from textSteganography import decodeText, encodeText
from videoSteganography import decode_string,encodeVideo
from commonUtils import STEGANOGRAPHIC_AUDIO_FILE, STEGANOGRAPHIC_IMAGE_BMP_FILE, STEGANOGRAPHIC_IMAGE_FILE, STEGANOGRAPHIC_TEXT_FILE, STEGANOGRAPHIC_VIDEO_FILE, UPLOAD_FOLDER,ALLOWED_EXTENSIONS, USER_AUDIO_FILE, USER_IMAGE_FILE, USER_TEXT_FILE, USER_VIDEO_FILE

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route("/signup")
def signup():
    username = request.args.post('user','')
    name = request.args.post('name','')
    email = request.args.post('email','')
    number = request.args.post('mobile','')
    password = request.args.post('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signin.html")

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        mail1 = request.form['user']
        password1 = request.form['password']
        con = sqlite3.connect('signup.db')
        cur = con.cursor()
        cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
        data = cur.fetchone()
        if data == None:
            return render_template("signin.html")    
        elif mail1 == 'admin' and password1 == 'admin':
            return redirect(url_for("index"))
        elif mail1 == str(data[0]) and password1 == str(data[1]):
            return redirect(url_for("index"))
        else:
            return render_template("signup.html")
    return render_template('signin.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return 'No file part'
        # file = request.files['file']
       
        # if file.filename == '':
        #     return render_template('index.html', error='No image uploaded!')
        # if file and allowed_file(file.filename):
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'],'download.jpg'))
        #     if request.form['go']=='encrypt':
        #         return redirect(url_for('image'))
        #     return redirect(url_for('decode1'))
        # else:
        #     return render_template('index.html', error='Please upload an image file')
        if request.form['go'] == 'videoSteganography' :
            return redirect(url_for('videoSteganography'))
        if request.form['go'] == 'audioSteganography' :
            return redirect(url_for('audioSteganography'))
        if request.form['go'] == 'imageSteganography' :
            return redirect(url_for('imageSteganography'))
        if request.form['go'] == 'textSteganography' :
            return redirect(url_for('textSteganography'))
    
    return render_template('index.html')

@app.route('/videoSteganography', methods=['GET', 'POST'])
def videoSteganography():
    if request.method == 'POST':
        userVideoFile = request.files['file']
        userVideoFile.save(os.path.join(app.config['UPLOAD_FOLDER'],'userVideoFile.mp4'))
        if request.form['go'] == 'encrypt' :
            encodeVideo()
            return send_file(STEGANOGRAPHIC_VIDEO_FILE,as_attachment=True)
        if request.form['go'] == 'decrypt' :
            decodedMessage = decode_string(USER_VIDEO_FILE)
            return render_template('decode.html',msg=decodedMessage)
    return render_template('videoSteganography.html')

@app.route('/audioSteganography', methods=['GET', 'POST'])
def audioSteganography():
    if request.method == 'POST':
        userAudioFile = request.files['file']
        userAudioFile.save(os.path.join(app.config['UPLOAD_FOLDER'],'userAudioFile.mp3'))
        if request.form['go'] == 'encrypt' :
            encodeAudio(USER_AUDIO_FILE)
            return send_file(STEGANOGRAPHIC_AUDIO_FILE,as_attachment=True)
        if request.form['go'] == 'decrypt' :
            decodedMessage = decodeAudio(USER_AUDIO_FILE)
            return render_template('decode.html',msg=decodedMessage)
    return render_template('audioSteganography.html')

@app.route('/imageSteganography', methods=['GET', 'POST'])
def imageSteganography():
    if request.method == 'POST':
        userTextFile = request.files['file']
        userTextFile.save(os.path.join(app.config['UPLOAD_FOLDER'],'userImageFile.jpg'))
        if request.form['go'] == 'encrypt' :
            encrypt(USER_IMAGE_FILE,"Image Hidden Text")
            # encryptAndEncodeDataIntoImage(USER_IMAGE_FILE,"Secret To be encoded")
            return send_file(STEGANOGRAPHIC_IMAGE_BMP_FILE,as_attachment=True)
        if request.form['go'] == 'decrypt' :
            decodedMessage = decrypt(STEGANOGRAPHIC_IMAGE_BMP_FILE)
            return render_template('decode.html',msg=decodedMessage)
    return render_template('imageSteganography.html')

@app.route('/textSteganography', methods=['GET', 'POST'])
def textSteganography():
    if request.method == 'POST':
        userTextFile = request.files['file']
        print(request.form['userText'],request.form['userSecret'])
        userTextFile.save(os.path.join(app.config['UPLOAD_FOLDER'],'userTextFile.txt'))
        if request.form['go'] == 'encrypt' :
            encodeText(USER_TEXT_FILE)
            return send_file(STEGANOGRAPHIC_TEXT_FILE,as_attachment=True)
        if request.form['go'] == 'decrypt' :
            decodedMessage = decodeText(USER_TEXT_FILE)
            return render_template('decode.html',msg=decodedMessage)
    return render_template('textSteganography.html')

# @app.route('/decode')
# def decode1():
#     image1 = Image.open(UPLOAD_FOLDER+'download.jpg')
#     msg1= decrypt(image1)
#     return render_template('decode.html',msg=msg1)

if __name__ == '__main__':
   app.run(debug = True)

