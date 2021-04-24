# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 20:35:53 2021

@author: Administrator
"""

import os,fnmatch
from win32com import client as wc
from win32com.client import Dispatch

def WordTxt(filePath,savePath):
    #切割路径和文件名
    dirs,filename = os.path.split(filePath)#切割目录和文件名，这里os.path.split是一个分割函数
    print(dirs,'\n',filename)
    #修改装换后的文件名
    new_name = ''
    if fnmatch.fnmatch(filename,'*.docx'):#fnmatch.fnmatch(filename,pattern),判断filename是否匹配pattern格式
        new_name = filename[:-5]+'.txt'
    elif fnmatch.fnmatch(filename,'*.doc'):
        new_name = filename[:-4]+'.txt'
    else:
        return
    print('->',new_name)
    #文件转换后的保存路径
    if savePath == '':
        savePath = dirs
    else:
        savePath = savePath
    word_to_txt = os.path.join(savePath,new_name)#连接路径名
    print('->',word_to_txt)
    #加载处理运用，word装换为txt
    wordapp = wc.Dispatch('Word.Application')
    mytxt = wordapp.Documents.Open(filePath)#Documents就是打开的文档对象
    mytxt.SaveAs(word_to_txt,FileFormat = 4)
    mytxt.Close()#关闭文件
if __name__=='__main__':
    filePath = os.path.abspath(r'C:\Users\Administrator\Documents\python\python文档\程序案例1.docx')
    #os.path.abspath返回绝对路径，但是还是需要在括号内写路径,r防止将\读成转义字符
    savepath = ''
    print(filePath)
    WordTxt(filePath,savepath)