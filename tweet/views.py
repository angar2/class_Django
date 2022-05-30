from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
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
        content = request.POST.get('my-content','')
        tags = request.POST.get('tag', '').split(',')

        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request,'tweet/home.html', {'error': '내용을 작성해주세요', 'tweet': all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip() # 공백 제거
                if tag != '':
                    my_tweet.tags.add(tag)

            # my_tweet = TweetModel()
            # my_tweet.author = user
            # my_tweet.content = request.POST.get('my-content','')
            my_tweet.save()
            return redirect('/tweet')


@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id = id)
    my_tweet.delete()
    return redirect('/tweet')


@login_required
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request, 'tweet/tweet_detail.html', {'tweet': my_tweet, 'comment': tweet_comment})


@login_required
def write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get("comment", "")
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()

        return redirect('/tweet/' + str(id))


@login_required
def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/tweet/' + str(current_tweet))


# 태그 보여주기
class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'

class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context