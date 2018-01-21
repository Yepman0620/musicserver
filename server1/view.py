#!/usr/bin/env python
# coding=utf-8

from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import HttpResponse
import os
nas = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'nas')
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
    if request.method == "POST":
        midistart = request.POST.get("midistart",None)
        print(midistart)
        return HttpResponse(midistart)
