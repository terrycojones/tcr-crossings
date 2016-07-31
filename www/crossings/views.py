from collections import Counter

from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed,
    HttpResponseNotFound)
from django.shortcuts import get_object_or_404, render
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from .models import Crossing, Comment
from .forms import CommentForm


def goodCrossings():
    return Crossing.objects.filter(active=True).exclude(
        latitude=-1.0).exclude(longitude=-1.0)


def index(request):
    context = {}
    return render(request, 'crossings/index.html', context)


def detail(request, crossingId):
    crossing = get_object_or_404(Crossing, pk=crossingId)
    return render(request, 'crossings/detail.html', {'crossing': crossing})


def allCrossings(request):
    """
    Get all crossings, in JSON.
    """
    return HttpResponse(
        serializers.serialize(
            'json', goodCrossings()),
        content_type='application/json')


def comments(request, crossingId):
    return HttpResponse(
        serializers.serialize(
            'json', Comment.objects.filter(
                crossing_id=crossingId).order_by('lastUpdate')),
        content_type='application/json')


def addComment(request, crossingId):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = Comment(crossing_id=int(form.cleaned_data['crossingId']),
                              text=form.cleaned_data['text'])
            comment.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(['POST'])


def text(request):
    """
    Render a simple textual listing of from/to countries.
    """
    countryPairs = Counter()
    for crossing in goodCrossings():
        countryPairs[(crossing.countryFrom, crossing.countryTo)] += 1

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
    crossings = []
    for crossing in goodCrossings():
        if (crossing.countryFrom == countryFrom and
                crossing.countryTo == countryTo):
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
    try:
        crossing = goodCrossings().get(countryFrom=countryFrom,
                                       countryTo=countryTo,
                                       name=name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    return render(request, 'crossings/textCrossing.html',
                  {'crossing': crossing})
