import tornado.ioloop
import tornado.web
import json
import logging
from OCR_test import OCR
import os

# 服务器端，监听等待请求

WORK_DIR = os.path.dirname(os.path.abspath(__file__))


class MainHandler(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        error_dic = {"error_code": 1, "error_msg": "requst body error"}
        info_dic = {}
        try:
            logging.debug(self.request.body)
            info_dic = json.loads(self.request.body.decode('utf-8'))

        except Exception as ex:
            error_dic['error_msg'] = "request body error, body=%s".format(self.request.body)
            logging.error(ex)
            return self.finish(error_dic)

        video_url = info_dic.get("VGA_url", None)
        if video_url == None:
            error_dic['error_code'] = 2
            error_dic['error_msg'] = "video_url is None"
            return self.finish(error_dic)

        subject = info_dic.get("subject", None)
        if subject == None:
            error_dic['error_code'] = 3
            error_dic["error_msg"] = "subject is None"
            return self.finish(error_dic)

        grade = info_dic.get("grade", None)
        if grade == None:
            error_dic['error_code'] = 4
            error_dic["error_msg"] = "grade is None"
            return self.finish(error_dic)

        curriculumId = info_dic.get("curriculumId", None)
        if curriculumId == None:
            error_dic['error_code'] = 5
            error_dic["error_msg"] = "curriculumId is None"
            return self.finish(error_dic)

        # 调用客户端给的信息经过如下处理返回消息给请求端（该函数没有传上来，只是一个例子）
        v_ocr = OCR(video_url, subject, grade, curriculumId)
        result_dic = v_ocr.main()

        print("*********result_dic:", result_dic)
        return self.finish(result_dic)


def make_app():
    return tornado.web.Application([
        (r'/ocr/process', MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
