from django.shortcuts import render, redirect
from .models import TweetModel
from django.contrib.auth.decorators import login_required # 로그인되어 있어야만 함수가 발동하게 함


# Create your views here.
def home(request):
    user = request.user.is_authenticated # 사용자가 로그인했는지 인증함
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # 사용자가 로그인했는지 인증함
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at') # order_by 생성된 시간을 역순으로 불러옴(역순으로 정렬하도록 - 를 붙여줌)
            return render(request, 'tweet/home.html', {'tweet': all_tweet})
        else:
            return redirect('/sign-in')
    elif request.method == 'POST':
        user = request.user
        my_tweet = TweetModel()
        my_tweet.author = user
        my_tweet.content = request.POST.get('my-content','')
        my_tweet.save()
        return redirect('/tweet')


@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id = id)
    my_tweet.delete()
    return redirect('/tweet')