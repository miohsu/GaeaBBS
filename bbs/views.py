from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Board
from .models import Topic
from .models import Post
from .forms import NewTopicForm
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
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('boards_topics', pk=board.id)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form':form})
