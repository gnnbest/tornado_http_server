import subprocess
import json
import time
import platform
import sys
import logging
import requests
import zipfile
import os


process_ocr_url = "http://172.16.1.60:8888/ocr/process"

WORK_DIR = os.path.dirname(os.path.abspath(__file__))

# 切到工作目录,删除存放的日志文件
targetDirect = WORK_DIR + "/runtime/bin"
time_str = time.strftime("%Y%m%d%H%M%S")
time_num = int(time_str)
for file in os.listdir(targetDirect):
    if "zkocr_" in file:
        templist = file.split("_")
        templist = templist[1].split(".")
        if (time_num - int(templist[0])) > 3 * 24 * 3600:
            targetFile = os.path.join(targetDirect, file)
            if os.path.isfile(targetFile):
                os.remove(targetFile)


log_file_name = targetDirect + "/zkocr_" + time_str + ".log"

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', filename=log_file_name, filemode='w')


# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)

logging.getLogger('').addHandler(console)


class VideoOcr:

    def video_general(self, payload = None):
        r = requests.post(process_ocr_url, data = json.dumps(payload))
        result_dic = json.loads(r.content.decode("utf-8"))# 如果有汉字一定要这样写
        return result_dic


if __name__ == "__main__":

    # 请求传输的内容
    payload = {'VGA_url':'/home/ocr/OCR/OCR_class/split_video/video.mp4',
               'subject':'数学', 'grade':'九年级', 'curriculumId':'1234' }
    v_ocr = VideoOcr()
    
    result_dic = v_ocr.video_general(payload)
   
    print(result_dic) 
