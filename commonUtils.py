from jinja2 import Undefined
import numpy as np
import os

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FRAME_NUMBER_ENCODING = 10
USER_VIDEO_FILE = UPLOAD_FOLDER + 'userVideoFile.mp4'
USER_AUDIO_FILE = UPLOAD_FOLDER + 'userAudioFile.mp3'
USER_TEXT_FILE = UPLOAD_FOLDER + 'userTextFile.txt'
USER_IMAGE_FILE = UPLOAD_FOLDER + 'userImageFile.jpg'
STEGANOGRAPHIC_VIDEO_FILE = UPLOAD_FOLDER + 'steganographicVideo.mp4'
STEGANOGRAPHIC_AUDIO_FILE = UPLOAD_FOLDER + 'steganographicAudio.mp3'
STEGANOGRAPHIC_TEXT_FILE = UPLOAD_FOLDER + 'steganographicText.txt'
STEGANOGRAPHIC_IMAGE_FILE = UPLOAD_FOLDER + 'steganographicImage.jpg'
SAMPLE_FRAME = Undefined
STEGANOGRAPHIC_IMAGE_BMP_FILE = UPLOAD_FOLDER + "userImageFile_hidden.bmp"

def msgtobinary(msg):
    if type(msg) == str:
        result= ''.join([ format(ord(i), "08b") for i in msg ])
    
    elif type(msg) == bytes or type(msg) == np.ndarray:
        result= [ format(i, "08b") for i in msg ]
    
    elif type(msg) == int or type(msg) == np.uint8:
        result=format(msg, "08b")

    else:
        raise TypeError("Input type is not supported in this function")
    
    return result

def setSampleFrame(frame_):
    SAMPLE_FRAME = frame_
