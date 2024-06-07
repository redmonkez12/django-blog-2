from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('comment/<int:id>/remove', views.delete_comment, name='remove_comment'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
]
