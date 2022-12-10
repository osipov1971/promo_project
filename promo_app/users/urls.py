from django.urls import path
from .views import *

urlpatterns = [
    path('roles/', RoleWithUserView.as_view()),
    path('roles/list/', RoleListView.as_view({'get': 'list', 'post': 'create'})),
    path('roles/list/<int:pk>/', RoleListView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('rights/', CreateRightRoleView.as_view()),
    path('rights/<int:role_id>/', UpdateRightRoleView.as_view()),

    path('', CreateUserView.as_view({'post': 'create'})),
    path('<int:pk>/', UserDetailView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('delete/', RemoveSelectedUsers.as_view()),
    path('me/', CurrentUserDetailView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('me/password/', ChangePasswordView.as_view()),
]
