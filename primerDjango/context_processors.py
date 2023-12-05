def notification_count(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications_count': request.user.notifications.unread().count()
        }
    else:
        return {}
