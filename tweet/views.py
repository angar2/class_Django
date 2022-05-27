from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    user = request.user.is_authenticated # 사용자가 로그인했는지 인증함
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')

def tweet(request):
    if request.method == 'GET':
        return render(request, 'tweet/home.html')
