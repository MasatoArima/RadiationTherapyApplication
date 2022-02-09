from django.urls import path
from . import views
from .views import(
    RtdataCreateView, RtdataUpdateView, RtdataDeleteView, RtdataListView, RtdataDetailView, RtdataFormView, ToridogRedirectView, delete_plandata, delete_stracturedata, delete_ctdata
)


app_name = 'analytics'

urlpatterns = [
    # path('create_rtdata', views.create_rtdata, name='create_rtdata'),
    # path('list_rtdatas', views.list_rtdatas, name='list_rtdatas'),
    # path('edit_rtdata/<int:id>', views.edit_rtdata, name='edit_rtdata'),
    # path('delete_rtdata/<int:id>', views.delete_rtdata, name='delete_rtdata'),
    path('post_memo/<int:user_id>', views.post_memo, name='post_memo'),
    path('save_memo', views.save_memo, name='save_memo'),
    path('detail_rtdata/<int:pk>', RtdataDetailView.as_view(), name='detail_rtdata'),
    path('list_rtdatas/', RtdataListView.as_view(), name='list_rtdatas'),
    path('list_rtdatas/<name>', RtdataListView.as_view(), name='list_rtdatas'),
    path('create_rtdata', RtdataCreateView.as_view(), name='create_rtdata'),
    path('edit_rtdata/<int:pk>', RtdataUpdateView.as_view(), name='edit_rtdata'),
    path('delete_rtdata/<int:pk>', RtdataDeleteView.as_view(), name='delete_rtdata'),
    path('rtdata_form/', RtdataFormView.as_view(), name='rtdata_form'),
    path('toridog_redirect_view/', ToridogRedirectView.as_view(), name='toridog_redirect_view'),
    path('delete_plandata/<int:pk>', delete_plandata, name='delete_plandata'),
    path('delete_stracturedata/<int:pk>', delete_stracturedata, name='delete_stracturedata'),
    path('delete_ctdata/<int:pk>/<int:rtdata>', delete_ctdata, name='delete_ctdata'),
]

