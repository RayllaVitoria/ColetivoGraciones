from django.urls import path, include
from django.contrib.auth.decorators import permission_required
from .views import *

app_name='blog'

urlpatterns = [	
	
	path('', IndexView.as_view(), name='index'),
	path('posts/', Post_list.as_view(), name='post_list'),
	path('post/<int:pk>/', Post_detail.as_view(), name='post_detail'),
	path('post/add/', Post_create.as_view(), name='post_add'),
	path('post/edit/<int:pk>/', Post_update.as_view(), name='post_edit'),
	path('post/delete/<int:pk>/', Post_delete, name='post_delete'),
	
]
