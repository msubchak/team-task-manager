from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from tasks.models import Worker


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_worker = Worker.objects.all().count()
    context = {
        "num_worker": num_worker,
    }
    return render(request, "tasks/index.html", context=context)

