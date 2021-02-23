from django.shortcuts import render
from django.http.response import StreamingHttpResponse

from .clean_Video import *
from .rec_recognition import *
from .diff_recognigion import *

# Create your views here.


dbj_clr = Clean_Video()
obj_rr = Rectangle_Recognition()
obj_dr = Diff_Recognition()


def index(request):
    return render(request, 'video/video.html')


def gen_clean():
    print('실행')

    while True:
        frame = dbj_clr.stream()

        frame = (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        yield frame


def gen_rec():
    print('실행')

    while True:
        frame = obj_rr.stream()

        frame = (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        yield frame


def gen_diff():
    print('실행')

    while True:
        frame = obj_dr.stream()

        frame = (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        yield frame


def http1(request):
    return StreamingHttpResponse(gen_clean(), content_type='multipart/x-mixed-replace; boundary=frame')


def http2(request):
    return StreamingHttpResponse(gen_rec(), content_type='multipart/x-mixed-replace; boundary=frame')


def http3(request):
    return StreamingHttpResponse(gen_diff(), content_type='multipart/x-mixed-replace; boundary=frame')
