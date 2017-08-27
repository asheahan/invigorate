
from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Idea, Inspiration

def index(request):
    user_ideas = Idea.objects.order_by('-created_date')[:5]
    context = {'user_ideas': user_ideas}
    return render(request, 'ideas/index.html', context)

def detail(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    inspirations = get_list_or_404(Inspiration, idea=idea)
    context = {'idea': idea, 'inspirations': inspirations}
    return render(request, 'ideas/detail.html', context)
