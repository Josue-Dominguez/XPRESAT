from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from accounts.forms import EditProfileForm
from accounts.models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
User = get_user_model()
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from .models import User
from notifications.signals import notify
from notifications.models import Notification

# Create your views here.

class NotificationView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/social/notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notifications'] = self.request.user.notifications.unread()
        return context

def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.mark_as_read()
    return redirect('accounts:notifications')  # Asegúrate de usar el nombre correcto de la URL aquí

def notifications(request):
    user_notifications = request.user.notifications.unread()
    # Aquí podrías tener lógica para marcar las notificaciones como leídas si es lo que deseas.
    return render(request, 'notifications.html', {'notifications': user_notifications})



@login_required
def UserProfileView(request, username):
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)

        followers = profile.followers.all()

        if len(followers) == 0:
                is_following = False
            
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)


        template = loader.get_template('users/detail.html')

        context = {
            'profile':profile,
            'number_of_followers':number_of_followers,
            'is_following': is_following,
        }

        return HttpResponse(template.render(context, request))

@login_required
def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    user_basic_info = User.objects.get(id=user)

    if request.method == 'POST':
        form=EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user_basic_info.first_name = form.cleaned_data.get('first_name')
            user_basic_info.last_name = form.cleaned_data.get('last_name')

            profile.picture = form.cleaned_data.get('picture')
            profile.banner = form.cleaned_data.get('banner')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.birthday = form.cleaned_data.get('birthday')
            profile.bio = form.cleaned_data.get('bio')

            profile.save()
            user_basic_info.save()
            return redirect('users:profile', username=request.user.username)
    else:
        form = EditProfileForm(instance=profile)

    context={
        'form':form,
    }
    return render(request, 'users/edit.html', context)


class AddFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = Profile.objects.get(pk=pk)
		profile.followers.add(request.user)
		messages.add_message(
            self.request,
            messages.SUCCESS,
            'Empezaste a seguir a este usuario'
        )
		return redirect('users:profile', username=request.user.username)

class RemoveFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = Profile.objects.get(pk=pk)
		profile.followers.remove(request.user)
		messages.add_message(
            self.request,
            messages.SUCCESS,
            'Dejaste de seguir a este usuario'
        )
		return redirect('users:profile', username=request.user.username)

class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        followers = profile.followers.all()

        context = {
            'profile': profile,
            'followers': followers
        }

        return render(request, 'pages/social/followers_list.html', context)
    
