from json import load
from os.path import join, dirname
from collections import Counter

from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed,
    HttpResponseNotFound)
from django.shortcuts import get_object_or_404, render
from django.core import serializers

from .models import Crossing, Comment
from .forms import CommentForm

_crossings = None


def index(request):
    # crossings_list = Crossing.objects.order_by('name')[:5]
    # context = {'crossings_list': crossings_list}
    context = {}
    return render(request, 'crossings/index.html', context)


def detail(request, crossingId):
    """
    Currently unused.
    """
    crossing = get_object_or_404(Crossing, pk=crossingId)
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


def _initCrossings():
    global _crossings
    if _crossings is None:
        from . import models
        crossingFile = join(dirname(models.__file__), 'static', 'crossings',
                            'crossings.json')
        with open(crossingFile) as fp:
            _crossings = load(fp)


def text(request):
    """
    Render a simple textual listing of from/to countries.
    """
    _initCrossings()
    countryPairs = Counter()
    for crossing in _crossings['crossings']:
        countryPairs[(crossing['countryFrom'], crossing['countryTo'])] += 1

    context = []
    for countryFrom, countryTo in sorted(countryPairs):
        context.append({
            'countryFrom': countryFrom,
            'countryTo': countryTo,
            'count': countryPairs[(countryFrom, countryTo)],
        })

    return render(request, 'crossings/text.html', {'countryPairs': context})


def textFromTo(request, countryFrom, countryTo):
    """
    Render a simple textual listing of border crossings between countryFrom
    and countryTo.
    """
    _initCrossings()

    crossings = []
    for crossing in _crossings['crossings']:
        if (crossing['countryFrom'] == countryFrom and
                crossing['countryTo'] == countryTo):
            crossings.append(crossing)

    context = {
        'countryFrom': countryFrom,
        'countryTo': countryTo,
        'crossings': crossings,
    }
    return render(request, 'crossings/textFromTo.html', context)


def textCrossing(request, countryFrom, countryTo, name):
    """
    Render a simple textual listing of border crossings between countryFrom
    and countryTo.
    """
    _initCrossings()

    for crossing in _crossings['crossings']:
        if (crossing['countryFrom'] == countryFrom and
                crossing['countryTo'] == countryTo and
                crossing['name'] == name):
            break
    else:
        return HttpResponseNotFound()

    return render(request, 'crossings/textCrossing.html',
                  {'crossing': crossing})
