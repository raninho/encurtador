import base64

from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from core.forms import UrlForm, UserCreateForm
from core.models import Url


def registrar(request, template_name='registrar.html'):
    form = UserCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse('login'))
    return render(request, template_name, {'form': form})


def encurtar_url(request, template_name='encurtador.html'):
    form = UrlForm(request.POST or None)
    if form.is_valid():
        url = form.save(commit=False)
        url.usuario = request.user if request.user.is_authenticated() else None
        url.save()
        return redirect(reverse('core:encurtar'))
    urls = Url.objects.all()[:10]
    return render(request, template_name, {'form': form, 'urls': urls})


@login_required
def listar_urls(request, template_name='listar.html'):
    urls = Url.objects.filter(usuario=request.user)
    return render(request, template_name, {'urls': urls})


def redirecionar_urls(request, token):
    try:
        id = base64.b64decode(str(token))
    except TypeError:
        raise Http404
    url = get_object_or_404(Url, pk=id)
    url = 'http://' + url.url if url.url[:4] != 'http' else url.url
    return HttpResponseRedirect(url)
