
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views import generic

from .models import Idea, Inspiration

def home(request):
    return render(request, 'ideas/home.html')


class IndexView(generic.ListView):
    template_name = 'ideas/index.html'
    context_object_name = 'user_ideas'

    def get_queryset(self):
        """Return the 5 latest ideas."""
        return Idea.objects.order_by('-created_date')[:5]


def detail(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    inspirations = list(Inspiration.objects.filter(idea=idea))
    context = {'idea': idea, 'inspirations': inspirations}
    return render(request, 'ideas/detail.html', context)
