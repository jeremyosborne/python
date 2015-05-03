from django.shortcuts import render_to_response
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from jsonserial import json_response_from
from django.views.decorators.csrf import csrf_exempt

# TODO: Checkout ensure_csrf_cookie() when we update to Django 1.4.
# TODO: Stop ignoring the csrf cookie.
# Since this handles an ajax request, we ignore the csrf tag (for now).
@csrf_exempt
def auth_login(request):
    """Handle a login request via an HTTP POST.

    Required POST arguments:
    username -> Name of the user.
    password -> Password of the user to authenticate.

    A JSON response will be returned for interpretation by the client, and
    any required session cookies will be set.
    """
    context = {
        # Authorization signal.
        "auth": False,
        # If there is an error, this will not be null.
        "error": None,
        # Information about the user.
        "info": {},
    }

    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(username=username, password=password)
    
        if user is not None and user.is_active:
            login(request, user)
            # signal the authentication success.
            context["auth"] = True
            # Make the timeout far in the future (in number of seconds).
            request.session.set_expiry(60*60*24*365)
            
            # TODO: Formalize the user info object.
            context["info"]["username"] = username
        else:
            context["error"] = "_Incorrect username or password."
    else:
        context["error"] = "_Service only accepts HTTP POST requests."

    return json_response_from(context)



# TODO: Stop ignoring the csrf cookie.
# Since this handles an ajax request, we ignore the csrf tag (for now).
@csrf_exempt
def auth_logout(request):
    """Handle a logout request via an HTTP POST.

    There are no required POST arguments.

    A JSON response will be returned for interpretation by the client, and
    any required session cookies will be set.
    """
    context = {
        # Authorization signal.
        # NOTE: We always indicate false from this method, even if the requester
        # attempts a GET request.
        "auth": False,
        # If there is an error, this will not be null.
        "error": None,
    }

    if request.method == "POST":
        if request.user.is_authenticated():
            logout(request)
    else:
        context["error"] = "_Service only accepts HTTP POST requests."

    return json_response_from(context)



# TODO: Stop ignoring the csrf cookie.
# Since this handles an ajax request, we ignore the csrf tag (for now).
@csrf_exempt
def auth_info(request):
    """Test, via HTTP POST, to see whether the browser has a currently logged 
    in user session, and provide basic information about the user.

    There are no required POST arguments.

    A JSON response will be returned for interpretation by the client, and
    any required session cookies will be set.
    """
    context = {
        # Authorization signal.
        "auth": False,
        # If there is an error, this will not be null.
        "error": None,
        # Information about the user.
        "info": {},
    }

    if request.method == "POST":
        if request.user.is_authenticated():
            context["auth"] = True

            # TODO: Formalize the user info object.
            context["info"]["username"] = request.user.username
    else:
        context["error"] = "_Service only accepts HTTP POST requests."

    return json_response_from(context)
