### gravatar.py ###############
### place inside a 'templatetags' directory inside the top level of a Django app (not project, must be inside an app)
### at the top of your page template include this:
### {% load gravatar %}
### and to use the url do this:
### <img src="{% gravatar_url 'someone@somewhere.com' %}">
### or
### <img src="{% gravatar_url sometemplatevariable %}">
### just make sure to update the "default" image path below

from django import template
import urllib, hashlib
from django.core.urlresolvers import reverse, resolve

register = template.Library()

@register.simple_tag
def navactive(request, urls):
    if request.path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""

class GravatarUrlNode(template.Node):
    def __init__(self, email):
        self.email = template.Variable(email)

    def render(self, context):
        try:
            email = self.email.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        default = "retro"
        size = 40

        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'s':str(size), 'd' : 'monsterid'})

        return gravatar_url

@register.simple_tag(takes_context=True)
def metadata(context):
    request = context['request']
    if resolve(request.path).url_name  == 'activity_details':
        activity = context['activity']
        meta = metadatos_generico(activity.title,activity.get_description_text,activity.get_keywords, "https://maps.googleapis.com/maps/api/staticmap?center=" + str(activity.position.latitude) + "," +  str(activity.position.longitude) + "&zoom=13&size=250x250&maptype=roadmap&markers=color:red%7Clabel: %7C" + str(activity.position.latitude) + "," +  str(activity.position.longitude),request.build_absolute_uri(reverse('activity_details',args=[activity.id])))
    else:
        meta = metadatos_generico("Druzi","Druzi, un lugar donde conocer gente acudiendo a actividades o creando tus propias actividades","actividades,social,amigos,eventos","http://127.0.0.1:8000/static/webapp/images/logo-color.png", "http://127.0.0.1:8000")
    return meta

def metadatos_generico(title,description,keywords, image, url):
    meta = '<title>%s</title>' \
           '<meta name="title" content="%s"></meta>' \
           '<meta name="description" content="%s"></meta>' \
            '<meta name="keywords" content="%s"></meta>' \
           '<meta name="og:locale" content="es_ES"></meta>' \
           '<meta name="og:type" content="article"></meta>' \
           '<meta name="og:title" content="%s"></meta>' \
           '<meta name="og:description" content="%s"></meta>' \
           '<meta name="og:url" content="%s"></meta>' \
           '<meta name="og:site_name" content="Druzi"></meta>' \
           '<meta name="article:publisher" content="https://www.facebook.com/elestudiodelpintor/"></meta>' \
           '<meta name="fb:admins" content="1024020701"></meta>' \
           '<meta name="og:image" content="%s"></meta>' \
            '<meta name="twitter:card" content="summary_large_image"></meta>' \
            '<meta name="twitter:title" content="%s"></meta>' \
            '<meta name="twitter:site" content="@BeevaDruzi"></meta>' \
            '<meta name="twitter:domain" content="Druzi"></meta>' \
            '<meta name="twitter:image:src" content="%s"></meta>' % (title,title,description, keywords, title, description, url,image, title,image)
    return meta

@register.tag
def gravatar_url(parser, token):
    try:
        tag_name, email = token.split_contents()

    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]

    return GravatarUrlNode(email)