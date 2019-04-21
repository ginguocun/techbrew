from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from ratelimit.decorators import ratelimit
from django.views.decorators.http import require_http_methods
import requests as req


@ratelimit(key='ip', rate='5/m', method=['POST'], block=True)
@ratelimit(key='ip', rate='100/h', method=['POST'], block=True)
@ratelimit(key='post:username', rate='5/m', method=['POST'], block=True)
@ratelimit(key='post:username', rate='20/h', method=['POST'], block=True)
def tb_login(request):
    template_name = 'registration/login.html'
    redirect_to = 'public'
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return redirect(redirect_to)
    else:
        form = AuthenticationForm()
    return render(request, template_name=template_name, context={'form': form})


def tb_logout(request):
    redirect_to = 'public'
    logout(request)
    return redirect(redirect_to)


def brix_plato(request):
    template_name = 'public/tools/brix-plato.html'
    return render(request, template_name=template_name)


@require_http_methods(["GET"])
def get_img(request):
    img_src = request.GET.get('img_src')
    if img_src:
        response = req.get(img_src)
        if response:
            return HttpResponse(response, content_type="image/png")
    return HttpResponse('No image')

