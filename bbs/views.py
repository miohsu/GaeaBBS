from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Board
from .models import Topic
from .models import Post
from .forms import NewTopicForm, PostForm
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.

def home(request):
    """
    板块列表
    :param request:
    :return:
    """
    board = Board.objects.all()
    return render(request, 'home.html', {'boards': board})


def board_topics(request, pk):
    """
    主题列表
    :param request:
    :param pk:
    :return:
    """
    board = get_object_or_404(Board, id=pk)
    return render(request, 'topics.html', {'board': board})


@login_required
def new_topic(request, pk):
    """
    创建主题贴
    :param request:
    :param pk:
    :return:
    """
    board = get_object_or_404(Board, id=pk)
    user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.id)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    """
    主题回复
    :param request:
    :param pk: 板块pk
    :param topic_pk: 主题pk
    :return:
    """
    topic = get_object_or_404(Topic, board__id=pk, id=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    """

    :param request:
    :param pk:
    :param topic_pk:
    :return:
    """
    topic = get_object_or_404(Topic, board__id=pk, id=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'form': form, 'topic': topic})
