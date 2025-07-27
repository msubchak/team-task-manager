from django.urls import path

from tasks.views import index

app_name = "taxi"

urlpatterns = [
    path("", index, name="index"),
]