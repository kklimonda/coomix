from django.template.response import TemplateResponse

from rack.models import Strip

def home(request):
    context = {}

    if request.user.is_authenticated():
        context['unread_strips'] = \
            Strip.objects.filter(comic=request.user.subscriptions.all()).order_by('added_at')
        print(context['unread_strips'])

    return TemplateResponse(request, "core/home.html", context)
