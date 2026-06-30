from django.shortcuts import render, get_object_or_404, redirect
from .models import Review

def review_list(request):
    reviews = Review.objects.all().order_by('-id')
    return render(request, 'review/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'review/review_detail.html', {'review': review})

def review_create(request):
    if request.method == 'POST':
        Review.objects.create(
            title=request.POST.get('title'),
            director=request.POST.get('director'),
            actor=request.POST.get('actor'),
            genre=request.POST.get('genre'),
            release_year=request.POST.get('release_year'),
            rating=request.POST.get('rating'),
            running_time=request.POST.get('running_time'),
            content=request.POST.get('content'),
        )
        return redirect('review-list')
    return render(request, 'review/review_form.html')

def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.director = request.POST.get('director')
        review.actor = request.POST.get('actor')
        review.genre = request.POST.get('genre')
        review.release_year = request.POST.get('release_year')
        review.rating = request.POST.get('rating')
        review.running_time = request.POST.get('running_time')
        review.content = request.POST.get('content')
        review.save()
        return redirect('review-detail', pk=pk)
    return render(request, 'review/review_form.html', {'review': review})

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review-list')
    return render(request, 'review/review_delete.html', {'review': review})