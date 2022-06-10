from stegano import lsb

# time                                                                 #install time ,opencv,numpy modules
import cv2
import numpy as np
import math
import os
import shutil
from subprocess import call,STDOUT

from commonUtils import UPLOAD_FOLDER, USER_VIDEO_FILE
from cryptographyAlgorithms import decryptData, encryptData

def split_string(s_str,count=10):
    per_c=math.ceil(len(s_str)/count)
    c_cout=0
    out_str=''
    split_list=[]
    for s in s_str:
        out_str+=s
        c_cout+=1
        if c_cout == per_c:
            split_list.append(out_str)
            out_str=''
            c_cout=0
    if c_cout!=0:
        split_list.append(out_str)
    return split_list

def frame_extraction(video):
    if not os.path.exists("./tmp"):
        os.makedirs("tmp")
    temp_folder="./tmp"
    print("[INFO] tmp directory is created")

    vidcap = cv2.VideoCapture(video)
    count = 0

    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
        count += 1

def encode_string(input_string,root="./tmp/"):
    split_string_list=split_string(input_string)
    for i in range(0,len(split_string_list)):
        f_name="{}{}.png".format(root,i)
        secret_enc=lsb.hide(f_name,split_string_list[i])
        secret_enc.save(f_name)
        print("[INFO] frame {} holds {}".format(f_name,split_string_list[i]))

def decode_string(userVideo):
    frame_extraction(userVideo)
    secret=[]
    root="./tmp/"
    for i in range(len(os.listdir(root))):
        f_name="{}{}.png".format(root,i)
        secret_dec=lsb.reveal(f_name)
        if secret_dec == None:
            break
        secret.append(secret_dec)
        
    decodedString = ''.join([i for i in secret])
    data = bytes(decodedString,'utf-8')
    data = decryptData(data)
    data = str(data,'utf-8')
    print(data)
    clean_tmp()
    return data
    
def clean_tmp(path="./tmp"):
    if os.path.exists(path):
        shutil.rmtree(path)
        print("[INFO] tmp files are cleaned up")

def encodeVideo():
    input_string = "THIS IS A TEST"
    byteInputString = bytes(input_string,'utf-8')
    data = encryptData(byteInputString)
    input_string = data.decode('utf-8')
    print("Video Encrypted Input String : ",input_string)
    frame_extraction(USER_VIDEO_FILE)
    call(["ffmpeg", "-i",USER_VIDEO_FILE, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
    
    encode_string(input_string)
    call(["ffmpeg", "-i", "tmp/%d.png" , "-vcodec", "png", "tmp/video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
    
    call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
    shutil.copyfile("./tmp/video.mov","./uploads/video.mov")
    old_file = os.path.join(UPLOAD_FOLDER,"video.mov")
    new_file = os.path.join(UPLOAD_FOLDER,"steganographicVideo.mp4")
    os.rename(old_file,new_file)
    clean_tmp()