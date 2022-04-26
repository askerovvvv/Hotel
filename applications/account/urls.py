from django.urls import path

from applications.account.views import *

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('activate/<uuid:activation_code>/', ActivateView.as_view()), # /<uuid:activation_code>
    path('login/', LoginView.as_view()),
    path('custom/', CustomView.as_view()),

]

