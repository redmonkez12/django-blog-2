from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('comment/<int:id>/remove', views.delete_comment, name='remove_comment'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # profile
    path('profile/', views.user_profile, name='user_profile'),
    # others
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact/thank-you/', TemplateView.as_view(template_name='others/contact_thank_you.html'),
         name='contact_thank_you'),
]
