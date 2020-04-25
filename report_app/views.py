from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def index(request):

    context = {
        'todos': 'todos',
        'user': request.user
    }
    return render(request, 'report_app/index.html', context)

