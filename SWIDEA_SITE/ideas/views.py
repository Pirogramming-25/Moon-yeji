from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Idea, IdeaStar
from devtools.models import DevTool

def idea_list(request):
    sort = request.GET.get('sort', 'latest')
    if sort == 'name':
        ideas = Idea.objects.all().order_by('title')
    elif sort == 'oldest':
        ideas = Idea.objects.all().order_by('created_at')
    elif sort == 'star':
        ideas = Idea.objects.all().annotate(star_count=Count('ideastar')).order_by('-star_count')
    else:  # latest
        ideas = Idea.objects.all().order_by('-created_at')
    return render(request, 'ideas/idea_list.html', {'ideas': ideas, 'sort': sort})

def idea_form(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        interest = request.POST['interest']
        devtool_id = request.POST['devtool']
        image = request.FILES.get('image')
        devtool = get_object_or_404(DevTool, pk=devtool_id)
        idea = Idea.objects.create(
            title=title,
            content=content,
            interest=interest,
            devtool=devtool,
            image=image,
        )
        return redirect('idea_detail', pk=idea.pk)
    devtools = DevTool.objects.all()
    return render(request, 'ideas/idea_form.html', {'devtools': devtools})

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    is_starred = False
    if request.user.is_authenticated:
        is_starred = IdeaStar.objects.filter(user=request.user, idea=idea).exists()
    return render(request, 'ideas/idea_detail.html', {'idea': idea, 'is_starred': is_starred})

def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        idea.title = request.POST['title']
        idea.content = request.POST['content']
        idea.interest = request.POST['interest']
        devtool_id = request.POST['devtool']
        idea.devtool = get_object_or_404(DevTool, pk=devtool_id)
        if request.FILES.get('image'):
            idea.image = request.FILES['image']
        idea.save()
        return redirect('idea_detail', pk=pk)
    devtools = DevTool.objects.all()
    return render(request, 'ideas/idea_update.html', {'idea': idea, 'devtools': devtools})

def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect('idea_list')

@login_required
def idea_star(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    star, created = IdeaStar.objects.get_or_create(user=request.user, idea=idea)
    if not created:
        star.delete()
    return redirect('idea_detail', pk=pk)

def idea_interest(request, pk, action):
    idea = get_object_or_404(Idea, pk=pk)
    if action == 'up':
        idea.interest += 1
    elif action == 'down':
        idea.interest -= 1
    idea.save()
    return redirect('idea_list')