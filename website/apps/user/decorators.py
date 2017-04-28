from django.http import HttpResponse

def remote_login_required(view_func):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    def _wrapped_view(request, *args, **kwargs):
        """
        Decorator for views that checks that the user is logged in, redirecting
        to the log-in page if necessary.
        """
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse(status=401)

    return _wrapped_view
