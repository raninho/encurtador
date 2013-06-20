import urllib, hashlib
from django import template

register = template.Library()

@register.filter(name='avatar_usuario')
def avatar_usuario(email):
    size = 40
    gravatar_url = "https://secure.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'s':str(size)})
    return gravatar_url

