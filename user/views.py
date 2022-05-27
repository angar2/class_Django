from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse # 화면에 글자를 띄울 때 사용
from django.contrib.auth import get_user_model # 사용자가 데이터베이스 안에 있는지 검사하는 함수(중복 확인)

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
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

        me = UserModel.objects.get(username=username) # 데이터베이스에서 데이터 불러오기
        if me.password == password:
            request.session['user'] = me.username # 세션에 저장
            return HttpResponse(username)
        else:
            return redirect('/sign-in')

    elif request.method == 'GET':
        return render(request, 'user/signin.html')