# place inside a 'templatetags' directory inside the top level of a Django app (not project, must be inside an app)
# at the top of your page template include this:
# {% load gravatar %}
# and to use the url do this:
# <img src="{% gravatar_url 'someone@somewhere.com' %}">
# or
# <img src="{% gravatar_url sometemplatevariable %}">
# just make sure to update the "default" image path below

import hashlib

from django import template
from django.utils.six import b
from django.utils.six.moves.urllib.parse import urlencode

register = template.Library()


class GravatarUrlNode(template.Node):
    def __init__(self, email, size=50):
        self.email = template.Variable(email)
        self.size = size

    def render(self, context):
        try:
            email = self.email.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        default = "blank"
        size = int(self.size) * 2 # requested at retina size by default and scaled down at point of use with css

        gravatar_url = "//www.gravatar.com/avatar/" + hashlib.md5(b(email.lower())).hexdigest() + "?"
        gravatar_url += urlencode({'s': str(size), 'd': default})

        return gravatar_url

@register.tag
def gravatar_url(parser, token):
    bits = token.split_contents()

    return GravatarUrlNode(*bits[1:])
