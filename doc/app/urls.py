from django.urls import include, path

from . import views

app_name = "app"

urlpatterns = [
     path("affinda/", views.AffindaNER.as_view()),
      ]

