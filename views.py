from social.forms import SocialCommentForm, ShareForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from .models import SocialPost, SocialComment
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from .forms import EncuestaForm
from django.contrib.auth import logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from accounts.models import Profile


class MisPublicacionesRecientesView(View):
    template_name = 'pages/social/publicaciones_recientes.html'

    def get(self, request, *args, **kwargs):
        publicaciones_recientes = SocialPost.objects.filter(author=request.user).order_by('-created_on')[:10]
        return render(request, self.template_name, {'publicaciones_recientes': publicaciones_recientes})

class PublicacionesRecientesView(LoginRequiredMixin, View):
    template_name = 'pages/social/publicaciones_recientes.html'
    #login_url = '/tu-pagina-de-login/'  # Reemplaza con tu URL de página de inicio de sesión

    def get(self, request, *args, **kwargs):
        # Obtén las publicaciones recientes del usuario actual
        publicaciones_recientes = SocialPost.objects.filter(author=request.user).order_by('-created_on')[:10]
        return render(request, self.template_name, {'publicaciones_recientes': publicaciones_recientes})

class LogoutView(View):
    template_name = 'account/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, self.template_name)  # Renderiza la plantilla directamente

class EncuestaView(FormView):
    template_name = 'pages/social/formulario.html'
    form_class = EncuestaForm
    success_url = reverse_lazy('home')  # Reemplázalo con el nombre de tu URL de éxito
    
    def form_valid(self, form):
        # Aquí puedes manejar la respuesta del usuario
        respuesta = form.cleaned_data['pregunta']
        # Hacer algo con la respuesta
        return super().form_valid(form)


class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)
        form = SocialCommentForm()

        comments = SocialComment.objects.filter(post=post).order_by('-created_on')

        context= {
            'post':post,
            'form':form,
            'comments':comments
        }
        return render(request, 'pages/social/detail.html', context)

    def post(self, request, pk,*args, **kwargs):
        post = SocialPost.objects.get(pk=pk)
        form = SocialCommentForm(request.POST)

        comments = SocialComment.objects.filter(post=post).order_by('-created_on')

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        context= {
            'post':post,
            'form':form,
            'comments':comments
        }
        return render(request, 'pages/social/detail.html', context)

class SharedPostView(View):
    def post(self, request, pk, *args, **kwargs):
        original_post = SocialPost.objects.get(pk=pk)
        form = ShareForm(request.POST)

        if form.is_valid():
            new_post = SocialPost(
                shared_body=self.request.POST.get('body'),
                body=original_post.body,
                author=original_post.author,
                created_on=original_post.created_on,
                shared_user=request.user,
                shared_on=timezone.now(),
            )
            new_post.save()

            for img in original_post.image.all():
                new_post.image.add(img)

            new_post.save()

        return redirect('home')

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=SocialPost
    fields=['body']
    template_name='pages/social/edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('social:post-detail', kwargs={'pk':pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=SocialPost
    template_name='pages/social/delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostReportView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=SocialPost
    template_name='pages/social/report.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)

        is_dislike = False
        
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = SocialComment.objects.get(pk=pk)

        is_dislike = False
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False
        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = SocialComment.objects.get(pk=pk)

        is_like = False
        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post=SocialPost.objects.get(pk=post_pk)
        parent_comment = SocialComment.objects.get(pk=pk)
        form=SocialCommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        return redirect('social:post-detail', pk=post_pk)     

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=SocialComment
    template_name="pages/social/comment_delete.html"

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('social:post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentEditView(UpdateView):
    model = SocialComment
    fields = ['comment']
    template_name = 'pages/social/comment_edit.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('social:post-detail', kwargs={'pk':pk})     
    

class UserSearch(View):
    def get(self,request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = Profile.objects.filter(Q(user__username__icontains=query))
        context={
            'profile_list':profile_list
        }
        return render(request, 'pages/social/search.html', context)

           