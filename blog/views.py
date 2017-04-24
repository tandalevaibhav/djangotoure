from django.shortcuts import render,get_object_or_404
from .models import Post  
from django.utils import timezone
from .forms import PostForm,UserForm 
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


# Create your views here.
def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'blog/post_list.html',{'posts':posts})

def post_detail(request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
           # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
def signup(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        form=UserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(user.password)
            user.save()
            register=True
            posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
            return render('blog/post_list.html',{'posts':posts})
        else:
            print(form.errors)

    else:
        form=UserForm()
    return render(request,'blog/signup.html',{'user_form':form,'registered': registered},context)
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})
@login_required
def post_publish(request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.publish()
        return redirect('post_detail', pk=pk)
@login_required
def post_remove(request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('post_list')

    
