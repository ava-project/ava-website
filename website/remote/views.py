from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render

# Create your views here.
class LoginView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'data': 'Success !'})
            # Redirect to a success page.
        else:
            return JsonResponse({'error': 'Wrong credentials'})
