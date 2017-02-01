from django.http import HttpResponse

def remote_login_required(view_func):

    def _wrapped_view(request, *args, **kwargs):
        print(request.user)
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse(status=401)

    return _wrapped_view
