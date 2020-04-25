import youtube_dl
import os
import sys

print("url: ",end='')
origin_url=input()

print("解析中...")
info=youtube_dl.YoutubeDL().extract_info(origin_url,download=False)
name=info["title"]
print(name)
list=info["formats"]

def aria2c(url,filename):
    cmd="aria2c --max-connection-per-server=16 --referer=\"%s\" -o \"%s\" \"%s\""%(origin_url,filename,url)
    os.system(cmd)
    while((not os.path.exists(filename)) or os.path.exists(filename+".aria2")):
        print("下载被中断,是否继续下载?(Y|n)")
        if(input()=='n'): sys.exit(0)
        os.system(cmd)

def ffmpeg(video_filename,sound_filename,filename):
    os.system("ffmpeg -i \"%s\" -i \"%s\" -c copy \"%s\""%(video_filename,sound_filename,filename))

def download_best():
    list=info['requested_formats']
    print(list[0]['format_note'])
    if(len(list)>1):
        f0=name+'.0.%s'%list[0]['ext']
        f1=name+'.1.%s'%list[1]['ext']
        print('开始下载视频部分...')
        aria2c(list[0]['url'],f0)
        print('开始下载音频部分...')
        aria2c(list[1]['url'],f1)
        ffmpeg(f0,f1,name+'.'+list[0]['ext'])
        print('删除多余文件?(y|N)')
        if(input()=='y'):
            os.remove(f0)
            os.remove(f1)
    else:
        print("开始下载...")
        aria2c(list[0]['url'],name+'.'+list[0]['ext'])
        
def download_tag(typ,tag,filename):
    for i in list:
        if(i['ext']==typ and tag in i['format_note']):
            aria2c(i['url'],filename)
            return 1
    return 0

def download_itag(itag,filename):
    for i in list:
        if(i['format_id']==itag):
            aria2c(i['url'],filename)
            return 1
    return 0

###############################################################

itag_v=['272','313','271','248','247','244','243','242','278']
tag_v=['4320','2160','1440','1080','720','480','360','240','144']
itag_s=['251','250','249']

if("www.bilibili.com" in origin_url): #bilibili 特判
    download_itag('1',name+".flv")
    sys.exit(0)

print("itag - format - type")
for i in list:
    print(i["format"]+' - '+i["ext"]+
    (" - Including video and audio" if(i["format_id"]=='18' or i["format_id"]=='22') else ""))

name=name.replace('"',"''")
video_filename=name+".0.webm"
sound_filename=name+".1.webm"
print(
'''
a/auto: 自动下载最高分辨率(默认)
c/custom: 自定义视频质量和音频质量
i/itag: 下载指定itag
'''
)
opt=input()
if(opt==None or opt=='' or opt[0]=='a'): 
    print('开始下载视频部分...')
    for i in tag_v:
        if(download_tag("webm",i,video_filename)): break
    print('开始下载音频部分...')
    for i in itag_s:
        if(download_itag(i,sound_filename)): break
    print('合并中...')
    ffmpeg(video_filename,sound_filename,name+".webm")

    print('删除多余文件?(y|N)')
    if(input()=='y'):
        os.remove(video_filename)
        os.remove(sound_filename)
elif(opt[0]=='c'):
    print('请输入视频部分itag')
    download_itag(input(),video_filename)
    print('请输入音频部分itag')
    download_itag(input(),sound_filename)
    print('合并中...')
    ffmpeg(video_filename,sound_filename,name+".webm")
    print('删除多余文件?(y|N)')
    if(input()=='y'):
        os.remove(video_filename)
        os.remove(sound_filename)
elif(opt[0]=='i'):
    print("itag: ")
    download_itag(input(),name+".webm")
