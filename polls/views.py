from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404

# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from polls.models import Question, Choice


def index(request, test):
    return HttpResponse('Hello,world,you are at the pools index %s' % test)


def mytest(request):
    return redirect(reverse('index'))


def detail(request, question_id):
    return HttpResponse("You're looking at quesion %s" % question_id)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F('votes') + 1
        # selected_choice.votes += 1
        selected_choice.save()

        return redirect(reverse('polls:results', args=(question_id,)))


# def index(request, myname):
#     latest_question_list = Question.objects.order_by('pub_date')  # [:5]
#     context = {'latest_question_list': latest_question_list, 'myname': myname}
#     # assert False
#     return render(request, 'polls/index.html', context)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist.")
#     context = {'question': question}
#     return render(request, 'polls/detail.html', context)


class DetaiView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
