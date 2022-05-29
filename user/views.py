from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse # 화면에 글자를 띄울 때 사용
from django.contrib.auth import get_user_model # 사용자가 데이터베이스 안에 있는지 검사하는 함수(중복 확인)
from django.contrib import auth # 암호화된 비밀번호가 일치하는지 검사하는 함수
from django.contrib.auth.decorators import login_required # 로그인되어 있어야만 함수가 발동하게 함

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        bio = request.POST.get('bio', None)

        if password != password2:
            return render(request, 'user/signup.html')
        else:
            exist_user = get_user_model().objects.filter(username = username)

            if exist_user:
                return render(request, 'user/signup.html')
            else:
                UserModel.objects.create_user(username = username, password = password, bio = bio)
            return redirect('/sign-in')

def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        me = auth.authenticate(request, username = username, password = password)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            return redirect('/sign-in')

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})

@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user) # 팔로우 취소
    else:
        click_user.followee.add(request.user) # 팔로우
    return redirect('/user')