from django.urls import path
from .import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('signup',views.UserRegisterView.as_view(),name='signup'),
    path('signin', views.signin,name='signin'),
    path('signout', views.signout,name='signout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('user/<int:pk>/update', view=views.PersonalInfoUpdate.as_view(), name='user-update'),
    path('change-password/',view=views.PasswordChangeView.as_view(),name='password-change')
]
