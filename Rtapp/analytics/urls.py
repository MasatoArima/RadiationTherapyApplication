from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('create_rtdata', views.create_rtdata, name='create_rtdata'),
    path('list_rtdatas', views.list_rtdatas, name='list_rtdatas'),
    path('edit_rtdata/<int:id>', views.edit_rtdata, name='edit_rtdata'),
    path('delete_rtdata/<int:id>', views.delete_rtdata, name='delete_rtdata'),
    path('post_memo/<int:user_id>', views.post_memo, name='post_memo'),
    path('save_memo', views.save_memo, name='save_memo'),
]