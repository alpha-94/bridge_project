from django.shortcuts import render
from django.http.response import StreamingHttpResponse, HttpResponse

from .clean_Video import *
from .rec_recognition import *
from .diff_recognigion import *


# Create your views here.


def index(request):
    return render(request, 'video/video.html')


def gen_clean():
    print('gen_clean 실행')
    dbj_clr = Clean_Video()
    while True:
        frame = dbj_clr.stream()

        frame = (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        yield frame


def gen_rec():
    print('gen_rec 실행')
    obj_rr = Rectangle_Recognition()
    while True:
        frame, text = obj_rr.stream()

        frame = (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        yield frame


def gen_diff():
    print('gen_diff 실행')
    obj_dr = Diff_Recognition()
    while True:
        frame, _ = obj_dr.stream()

        frame = (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        yield frame


def gen_text():
    print('gen_rec 실행')
    obj_rr = Rectangle_Recognition()
    while True:
        frame, text = obj_rr.stream()

        text = (b'--frame\r\n'
                b'Content-Type: text/html\r\n\r\n' + text.encode() + b'\r\n\r\n')
        yield text


def http1(request):
    return StreamingHttpResponse(gen_clean(), content_type='multipart/x-mixed-replace; boundary=frame')


def http2(request):
    return StreamingHttpResponse(gen_rec(), content_type='multipart/x-mixed-replace; boundary=frame')


def http3(request):
    return StreamingHttpResponse(gen_diff(), content_type='multipart/x-mixed-replace; boundary=frame')


def http_text(request):
    return StreamingHttpResponse(gen_text(), content_type='multipart/x-mixed-replace; boundary=frame')
