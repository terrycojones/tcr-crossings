from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed)
from django.shortcuts import get_object_or_404, render
from django.core import serializers

from .models import Crossing, Comment
from .forms import CommentForm


def index(request):
    crossings_list = Crossing.objects.order_by('name')[:5]
    context = {'crossings_list': crossings_list}
    return render(request, 'crossings/index.html', context)


def detail(request, crossingId):
    crossing = get_object_or_404(Crossing, pk=crossingId)
    # return HttpResponse("You're looking at crossing %s." % crossingId)
    return render(request, 'crossings/detail.html', {'crossing': crossing})


def comments(request, crossingId):
    return HttpResponse(
        serializers.serialize(
            'json', Comment.objects.filter(
                crossingId=crossingId).order_by('lastUpdate')),
        content_type='application/json')


def addComment(request, crossingId):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = Comment(crossingId=form.cleaned_data['crossingId'],
                              text=form.cleaned_data['text'])
            comment.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(['POST'])
