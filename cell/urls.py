from django.urls import path, include
from . import views
# CellUserCreateView
urlpatterns = [
    path('', views.home, name="home"),
    path('groups/create/', views.CreateCellGroupView.as_view(), name="create-cell-group"),
    path('members/create/', views.CreateMemberView.as_view(), name="create-member"),
    path('members/<member_id>/user/', views.CellUserCreateView.as_view(), name="create-member-user"),
    path('members/upload/', views.MembersUploadView.as_view(), name="upload-members"),
    path('contributions/create/', views.CreateContributionView.as_view(), name="create-contribution"),
    path('payments/create/', views.CreatePaymentView.as_view(), name="create-payment"),
]
