import os
import re
from urllib import urlencode
import logging

from django.conf import settings
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.shortcuts import redirect, render_to_response
from django.db.models import Q

from eliotdb_app.models import Name, Document, Mention
from eliotdb_app.forms import SearchForm, NameForm, DocumentForm, MentionForm

logger = logging.getLogger(__name__)
# test edit

def index(request):
  return render_to_response('index.html', context_instance=RequestContext(request))

def searchform(request):
    "Search for name or document."
    form = SearchForm(request.GET)
    response_code = None
    context = {'searchform': form}
    number_of_results = 100

    if form.is_valid():
        name = form.cleaned_data['name']
        document = form.cleaned_data['document']
        names_s = Name.objects.only("tei_id", "surname", "forename", "birth", "death").filter(surname__icontains="%s" % name)
        names_f = Name.objects.only("tei_id", "surname", "forename", "birth", "death").filter(forename__icontains="%s" % name)
        # documents = Document.objects("tei_id", ...

        context['name'] = name
        context['names_s'] = names_s
        context['names_f'] = names_f
        # context['document'] = document
        # context['documents']= documents
        context['name_count'] = len(names_s) + len(names_f)

        response = render_to_response('search_results.html', context, context_instance=RequestContext(request))                         
    else:
        response = render(request, 'index.html', {"searchform": form})       
    if response_code is not None:
        response.status_code = response_code
    return response

def names(request):
     return render_to_response('names.html', context_instance=RequestContext(request))

def documents(request):
     return render_to_response('documents.html', context_instance=RequestContext(request))

def name_record(request, tei_id):
    name = Name.objects.get(tei_id__exact=tei_id)
    return render_to_response('name_record.html', {'name': name}, context_instance=RequestContext(request))

def edit_name(request, tei_id):
    if request.method == "POST":
        name_form = NameForm(request.POST)
        # valid data submitted    
        if name_form.is_valid():
            name = Name.object.get(tei_id=tei_id)
            name_form.save()
            return redirect('/names/' + tei_id)
        # invalid data submitted
        else:
            name = Name.objects.get(tei_id=tei_id)
            name_form = NameForm(instance=name)
            errors = name_form.errors
            what = 'invalid form submitted.'
    # no data submitted
    else:
        name = Name.objects.get(tei_id=tei_id)
        name_form = NameForm(instance=name)
        errors = 'no errors to print'
        what = 'no request'
 
    return render_to_response('edit_name.html', {'form' : name_form, 'name': name, 'errors' : errors, 'what' : what}, context_instance=RequestContext(request))

    
def add_name(request):
    if request.method == "POST":
        nform = NameForm(request.POST, instance=Name())


def save_name(request, tei_id):
    name = Name.objects.get(tei_id__exact=tei_id)
    return render_to_response('save_name.html', {'name' : name}, context_instance=RequestContext(request))

