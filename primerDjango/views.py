import torch
from multiprocessing import context
from social.models import Image, SocialPost, SocialComment
from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from social.forms import SocialPostForm, ShareForm
from django.db.models import Q
from django.http import HttpResponseRedirect
import numpy as np
from .mytorchmodel import train_and_save_model
from django.conf import settings



def train_model(request):
    # Asegúrate de que solo un usuario autorizado pueda iniciar el entrenamiento
    if not request.user.is_authenticated:
        return redirect('login')  # O alguna otra respuesta adecuada

    # Llamamos a la función train_and_save_model con los parámetros necesarios
    train_and_save_model(request.user, settings.MODEL_PATH, settings.LEARNING_RATE, settings.EPOCHS)

    # Devuelve una respuesta HTTP, por ejemplo, redirigir a la página de inicio
    return redirect('home')


class HomeView(LoginRequiredMixin, View):
    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        logged_in_user=request.user

        posts = SocialPost.objects.filter(
            Q(author__profile__followers__in=[logged_in_user.id]) |
            Q(author=logged_in_user)
        ).order_by('-created_on')

        form = SocialPostForm()
        share_form = ShareForm()

        context={
            'posts':posts,
            'form':form,
            'share_form':share_form 
        }
        return render(request, 'pages/index.html', context)

    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        form = SocialPostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        share_form = ShareForm()

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = logged_in_user
            new_post.save()

            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()
            return redirect('home')

        context = {
            'form': form,
            'share_form': share_form
        }
        return render(request, 'pages/index.html', context)
