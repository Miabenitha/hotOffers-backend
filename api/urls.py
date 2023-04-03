from django.urls import path
from django.conf.urls import handler404
from knox import views as knox_view
from api.exceptions import custom404
from django.urls import re_path
from api.views import (
    signup, 
    signin,
    verify_email,
    get_user_data, 
    create_profile_avatar
    )


urlpatterns = [
    path("signup", signup),
    path("signin", signin),
    path("user", get_user_data),
    path('verify-email/<slug:token>', verify_email),
    path('create-profile-picture', create_profile_avatar),
    path("signout", knox_view.LogoutView.as_view()),
    path("signoutall", knox_view.LogoutAllView.as_view()),
]

urlpatterns += [re_path(r'^.*/$',custom404)]
