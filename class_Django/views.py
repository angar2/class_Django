from django.http import HttpResponse
from django.shortcuts import render # HTML 파일을 보여주는 역할


def base_response(request):
    return HttpResponse("안녕하세요! 장고의 시작입니다!")

def first_view(request):
    return  render(request, 'my_test.html')