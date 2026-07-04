from django.shortcuts import render, redirect, get_object_or_404
from .models import DevTool

def devtool_list(request):
    devtools = DevTool.objects.all()
    return render(request, 'devtools/devtool_list.html', {'devtools': devtools})

def devtool_form(request):
    if request.method == 'POST':
        name = request.POST['name']
        kind = request.POST['kind']
        content = request.POST['content']
        DevTool.objects.create(name=name, kind=kind, content=content)
        return redirect('devtool_list')
    return render(request, 'devtools/devtool_form.html')

def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    return render(request, 'devtools/devtool_detail.html', {'devtool': devtool})

def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == 'POST':
        devtool.name = request.POST['name']
        devtool.kind = request.POST['kind']
        devtool.content = request.POST['content']
        devtool.save()
        return redirect('devtool_detail', pk=pk)
    return render(request, 'devtools/devtool_update.html', {'devtool': devtool})

def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    devtool.delete()
    return redirect('devtool_list')