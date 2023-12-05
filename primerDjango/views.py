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
from django.conf import settings
from .algoritmo import modelo
from notifications.signals import notify




class HomeView(LoginRequiredMixin, View):
    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        logged_in_user=request.user
        posts = SocialPost.objects.filter(
            Q(author__profile__followers__in=[logged_in_user.id]) |
            Q(author=logged_in_user)
        ).order_by('-created_on')
         # Aquí, analizas cada post y almacenas el resultado
        for post in posts:
            post.analisis_resultado = modelo.analizar_texto(post.body)

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

            # Aquí es donde analizas el texto de la publicación
            texto_publicacion = new_post.body  # Asegúrate de que 'body' es el campo correcto
            resultado_analisis = modelo.analizar_texto(texto_publicacion)
            print(f"Resultado del análisis para la publicación: {resultado_analisis}")

            # Aquí podrías decidir qué hacer con el resultado del análisis
            # Por ejemplo, podrías almacenar este resultado en la base de datos si tu modelo SocialPost tiene un campo para ello

            new_post.save()

            # Guardar imágenes asociadas, si las hay
            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()
            
            # Enviar notificaciones a los seguidores
            followers = logged_in_user.profile.followers.all()
            for follower in followers:
                notify.send(logged_in_user, recipient=follower, verb='ha creado una nueva publicación', target=new_post)
            return redirect('home')

        context = {
            'form': form,
            'share_form': share_form
        }
        return render(request, 'pages/index.html', context)