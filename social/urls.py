from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostDeleteView, 
    PostDetailView, 
    PostEditView, 
    PostReportView,
    AddDislike, 
    AddLike, 
    CommentDeleteView, 
    CommentEditView, 
    CommentReplyView, 
    AddCommentDislike, 
    AddCommentLike,
    SharedPostView,
    EncuestaView,
    LogoutView, 
    PublicacionesRecientesView
    )


app_name="social"

urlpatterns = [
    path('train_model/', views.TrainModelView.as_view()),
    path('encuesta/', EncuestaView.as_view(), name="encuesta_view"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name="post-edit"),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name="post-delete"),
    path('post/report/<int:pk>', PostReportView.as_view(), name="post-report"),

     path('publicaciones_recientes/', PublicacionesRecientesView.as_view(), name='publicaciones_recientes'),

    path('post/<int:pk>/like', AddLike.as_view(), name='like'),
    path('post/<int:pk>/dislike', AddDislike.as_view(), name='dislike'),

    path('post/<int:pk>/share', SharedPostView.as_view(), name='share-post'),

    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name="comment-delete"),
    path('post/<int:post_pk>/comment/edit/<int:pk>/', CommentEditView.as_view(), name="comment-edit"),

    path('post/<int:post_pk>/comment/<int:pk>/like', AddCommentLike.as_view(), name="comment-like"),
    path('post/<int:post_pk>/comment/<int:pk>/dislike', AddCommentDislike.as_view(), name="comment-dislike"),
    path('post/<int:post_pk>/comment/<int:pk>/reply',CommentReplyView.as_view(), name='comment-reply'),


]