from django.shortcuts import redirect

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if hasattr(request, "simple_user") and not request.simple_user:
            return redirect("login")
        
        return view_func(request, *args, **kwargs)
    
    return wrapper