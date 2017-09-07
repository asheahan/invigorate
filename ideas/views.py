
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone

from .models import Idea, Inspiration

def home(request):
    return render(request, 'ideas/home.html')


class IndexView(generic.ListView):
    template_name = 'ideas/index.html'
    context_object_name = 'user_ideas'

    def get_queryset(self):
        """Return the 5 latest ideas."""
        return Idea.objects.filter(
            created_by=self.request.user.id
        ).order_by('-created_date')[:5]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


def detail(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    inspirations = list(Inspiration.objects.filter(idea=idea))
    context = {'idea': idea, 'inspirations': inspirations}
    return render(request, 'ideas/detail.html', context)


class NewIdeaView(generic.edit.CreateView):
    model = Idea
    fields = ['label', 'description']
    success_url = '/ideas/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.created_date = timezone.now()
        return super(NewIdeaView, self).form_valid(form)


class EditIdeaView(generic.edit.UpdateView):
    model = Idea
    fields = ['label', 'description']
    success_url = '/ideas/'

    def get_queryset(self):
        base_qs = super(EditIdeaView, self).get_queryset()
        return base_qs.filter(created_by=self.request.user)
