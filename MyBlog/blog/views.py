from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.views.generic import(DeleteView,UpdateView,TemplateView,CreateView,ListView,DetailView)
from blog.models import Comment,Post
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import CommentForm,PostForm,UserForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
# Create your views here.

class AboutView(TemplateView):
    template_name='blog/about.html'

class PostListView(ListView):
    model=Post
    template_name='blog/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()) #.order_by('-published_date')

class PostDetailView(DetailView):
    model=Post
    template_name='blog/post_detail.html'



class CreatePostView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    model=Post
    redirect_field_name='blog/post_detail.html'

    form_class=PostForm

    def form_valid(self,form):
        self.object =form.save(commit=False)
        self.object.author=self.request.user
        self.object.save()
        return super().form_valid(form)







class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    model=Post
    #redirect_field_name='blog/post_detail.html'
    form_class=PostForm

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post
    success_url=reverse_lazy('post_list')

"""class DraftListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name='block/post_draft_list.html'
    model=Post

    #def get_queryset(self):
        #return Post.objects.filter(published_date__lte=timezone.now())
"""
@login_required
def alluserpost(request,*args,**kwargs):
    email=kwargs['email']
    values=Post.objects.filter(author__email__exact = email,published_date__isnull=True)

    return render(request,'blog/post_draft_list.html',{'posts':values})

@login_required
def draftListView(request,*args,**kwargs):
    email=kwargs['email']
    values=Post.objects.filter(author__email__exact = email,published_date__lte=timezone.now())
    return render(request,'blog/post_draft_list.html',{'posts':values})





##################################################
##################################################
@login_required
def add_comments_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.author=request.user
            comment.post=post
            comment.save()
            return redirect('blog:post_detail',pk=post.pk)
        else:
            form=CommentForm()
        return render(request,'blog/comment_form.html',{'form':form})
    else:
        form=CommentForm()
        return render(request,'blog/comment_form.html',{'form':form})


@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('blog:post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('blog:post_detail',pk=post_pk)

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('blog:post_detail',pk=pk)

"""
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('post_list'))

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('post_list'))

            else:
                HttpResponse("account is not active")
        else:
            return HttpResponse("Invalid login")
    else:
        return render(request,'registration/login.html',{})

def user_register(request):
    registered=False

    if request.method=='POST':

        user_form=UserForm(data=request.POST)

        if user_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            registered=True

            return HttpResponseRedirect(reverse('post_list'))

        else:
            print(user_form.errors)
    else:
        user_form=UserForm()
        return render(request,'registration/register.html',{'user_form':user_form})

        """
