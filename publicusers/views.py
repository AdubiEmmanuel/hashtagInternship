from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from django.shortcuts import get_object_or_404

from . models import Question, Choice

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'publicusers/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return the last five published questions.
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'publicusers/detail.html'

class ResultView(generic.DetailView):
    model = Question
    template_name = 'publicusers/results.html'

  


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'publicusers/detail.html',{
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a user hits the back button 
        return HttpResponseRedirect(reverse('publicusers:results', arg=(question.id,)))
