from django import forms
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
# from django.core.exceptions import ValidationError

from . import util


class NewArticleForm(forms.Form):
    title = forms.CharField(label='Title')
    content = forms.CharField(widget=forms.Textarea)

    # First error validation, that I find on Internet
    # def clean_title(self):
    #     title = self.cleaned_data['title'] 
    #
    #     if title in util.list_entries():
    #        raise ValidationError('The article already exists!')
    # 
    #     return title


def index(request):
    return render(request, 'encyclopedia/index.html', {
        'entries': util.list_entries()
    })


def article(request, title):
    import markdown2

    if (not title.upper() in (
        entry.upper() for entry in util.list_entries()
    )):
        return render(request, 'encyclopedia/page_does_not_exists.html')
        

    for entry in util.list_entries():
        if entry.upper() == title.upper():
            title = entry
            break

    if request.path.split('/')[2].upper() == title.upper():
        return render(request, 'encyclopedia/article.html', {
            'title': title,
            'content': markdown2.markdown(util.get_entry(title)),
        })


def search(request):
    query = request.GET.get('q')
    
    if query in util.list_entries():
        return HttpResponseRedirect(reverse('encyclopedia:article', args=[query]))
   
    return render(request, 'encyclopedia/index.html', {
        'entries': [entry for entry in util.list_entries() if query.upper() in entry.upper()] 
    })


def create_article(request):
    if request.method == 'POST':
        form = NewArticleForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            # Second error validation
            if title in util.list_entries():
                form.add_error('title', 'The article already exists!')

                return render(request, 'encyclopedia/create_article.html', {
                    'form': form
                })

            util.save_entry(title, content)
            
            return HttpResponseRedirect(reverse('encyclopedia:article', args=[title])) 
    
    return render(request, 'encyclopedia/create_article.html', {
        'form': NewArticleForm()
    })


def edit_article(request, title):
    content = util.get_entry(title)
 
    if request.method == 'POST':
        form = NewArticleForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            util.save_entry(title, content)

            return HttpResponseRedirect(reverse('encyclopedia:article', args=[title]))
        else:
            return render(request, 'encyclopedia/edit_article.html', {
                'title': title,
                'form': form
            })

    return render(request, 'encyclopedia/edit_article.html', {
        'title': title,
        'form': NewArticleForm({ 'content': content }) 
    })


def random_article(request):
    import random

    entries = util.list_entries()

    if entries:
        random_entry = random.choice(entries)

        return HttpResponseRedirect(reverse('encyclopedia:article', args=[random_entry])) 


def custom_not_found_view(request, exception):
    title = request.path.split('/')[1]

    return render(request, 'encyclopedia/404.html', {
        'title': title,
    })

