#!/usr/bin/env python
# coding=utf-8

from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import HttpResponse
from . import settings
import logging 
import subprocess 
import os
import string
import shutil
rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
nas = os.path.join(rootpath,'nas')
staticpath = os.path.join(rootpath,'static')
midipath = os.path.join(rootpath,'static/midi')
midibackpath = os.path.join(rootpath,'static/midiback')
print(midipath)
def hello(request):
    context = {}
    context['hello']='hello World'
    return render(request,'hello.html',context)
def upload_file(request):  
    if request.method == "POST":    # 请求方法为POST时，进行处理  
        myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None  
        if not myFile:  
            return HttpResponse("no files for upload!")  
        destination = open(os.path.join(nas,myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作  
        for chunk in myFile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()  
        return HttpResponse("upload over!") 
def music(request):
    context = {}
    context['hello']='hello World'
    return render(request,'index.html',context)
def upload_midis(request):
    context = {}
    context['hello']='playwave'
    if request.method == "POST":
        midistart = request.POST.get("midistart",None)
        midis = '--primer_melody='+midistart 
        log = logging.getLogger("Core.Analysis.Processing")
        if os.path.exists(midibackpath):
            shutil.rmtree(midibackpath,True)
        shutil.move(midipath,midibackpath)
        os.mkdir(midipath)
        INTERPRETER = "/usr/bin/python"
        TIMIDITY = "/usr/bin/timidity"
        print(midipath)
        if not os.path.exists(INTERPRETER): 
            log.error("Cannot find INTERPRETER at path \"%s\"." % INTERPRETER)  
        processor = "/home/pingan/chen/magenta/magenta/models/performance_rnn/performance_rnn_generate.py"
        cmd_2 = [INTERPRETER] + [processor] + ['--run_dir=/home/pingan/Desktop/light_music/light_music_cp'] + ['--config=performance'] + ['--num_outputs=1'] + ['--num_steps=6000'] + ['--output_dir=/home/pingan/workspace/musicserver/static/midi'] + [midis]
        print(cmd_2)
        outputs = subprocess.check_output(cmd_2, stderr=subprocess.STDOUT)
        for root, dirs, files in os.walk(midipath):
            print(files)
        midifile=os.path.join(midipath,files[0])
        print(midifile)
        wavefile=os.path.join(midipath,'1.wav')
        print(wavefile)
        cmd_3 = [TIMIDITY] + [midifile] + ['-Ow'] + ['-o'] + [wavefile]
        print(cmd_3)
        outputs = subprocess.check_output(cmd_3, stderr=subprocess.STDOUT)
        #outputs = outputs.split('\n')
    return render(request,'wavplayer.html',context)
def midi_player(request):
    context = {}
    context['hello']='midiplayer'
    return render(request,'midiplayer.html',context)
