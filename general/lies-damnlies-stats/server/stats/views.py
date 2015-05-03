from django.db import models
from django.shortcuts import render_to_response
import stats.models
from stats.models import Eggs
from django.core.exceptions import ValidationError
#from django.contrib.auth import authenticate
from jsonencoderdelegator import JSONEncoderDelegator
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def json_response_from(context):
    """Wrapper used to convert the context object to JSON and send back as
    an HTTP response.
    """
    json = JSONEncoderDelegator()
    return HttpResponse(json.encode(context), mimetype='application/json')


def get(request):
    """Handle retreival request for the egg statistics via an HTTP GET.
    
    On a get request, an array will be returned containing
    all of the egg days that have been added to the database.
    
    Required GET arguments (for eggs):
        -> statName {string} A valid stat name.
    """
    context = {
        # Error by default.
        "error": "_Could not retrieve data.",
        # Will always be a list for a general get request,
        # or null if there is an auth error.
        "stats": None,
    }
    user = request.user
    statName = request.GET.get("statName", "")
    try:
        if user.is_authenticated() and user.is_active and getattr(stats.models, statName).is_ajax_accessible:
            context["stats"] = getattr(stats.models, statName).objects.all().order_by('-date').filter(user=user)
            # Turn off the error.
            context["error"] = None
    except AttributeError:
        # We fail by default.
        pass
    return json_response_from(context)



# TODO: Checkout ensure_csrf_cookie() when we update to Django 1.4.
# TODO: Stop ignoring the csrf cookie.
# Since this handles an ajax request, we ignore the csrf tag (for now).
@csrf_exempt
def save(request):
    """Handle the save statistics request via an HTTP POST. 
    
    This request does double duty for create and update, there is no external 
    distinction between the two.

    The request requires previous authentication, and validates authentication
    via cookie.
    
    A JSON response will be returned for interpretation by the client.

    Required POST arguments must match the fields of the model being updated.
    """
    context = {
        # If there is an error, this will not be null.
        "error": None,
        # What was the model that was modified (created or updated)?
        "stat": None,
    }
    statModel = None
    statFields = None
    if request.method == "POST":
        user = request.user
        statName = request.POST.get("statName", "")
        # Due to the nature of query params, where multiple values can be
        # sent in during a request, the values of each key will be in a list.
        statData = dict(request.POST)
        try:
            if getattr(stats.models, statName).is_ajax_accessible:
                statModel = getattr(stats.models, statName)
            # Remove the statName from the input.
            del statData["statName"]
        except (AttributeError, KeyError):
            context["error"] = "_Incorrect statName %s" % statName
        
        if statModel and statData and user.is_authenticated() and user.is_active:
            try:
                stat = statModel.objects.filter(date=statData["date"][0]).filter(user=user)
                if len(stat) > 0:
                    # This is an update to an existing record.
                    stat = stat[0]
                else:
                    # This is a new record.
                    stat = statModel()
    
                stat.user = user
                # copy the fields into the array and pray for the best.
                for k, v in statData.items():
                    setattr(stat, k, v[0])
                # Make sure validators are called (not sure if this is needed).
                stat.clean_fields()
                stat.save()
                context["stat"] = stat
            except (ValidationError, KeyError) as err:
                context["error"] = "".join(err.__str__()[0])
    
        # Deal with non-content and non-error state
        if context["error"] == None and context["stat"] == None:
            context["error"] = "_Could not save the data. Please check your input."
    else:
        context["error"] = "_Service only accepts HTTP POST requests."

    return json_response_from(context)



# TODO: Checkout ensure_csrf_cookie() when we update to Django 1.4.
# TODO: Stop ignoring the csrf cookie.
# Since this handles an ajax request, we ignore the csrf tag (for now).
@csrf_exempt
def delete(request):
    """Handle the delete statistics request via an HTTP POST. 
    
    If a record exists, it is deleted.

    The request requires previous authentication, and validates authentication
    via cookie.
    
    A JSON response will be returned for interpretation by the client.

    Required DELETE arguments:
        -> date (as a YYYY-MM-DD string, must be unique)
    """
    context = {
        # If there is an error, this will not be null.
        "error": None,
        # What was the model that was deleted?
        "stat": None,
    }
    statModel = None
    statFields = None
    if request.method == "POST":
        user = request.user
        # We only need the date, a unique field, to delete
        date = request.POST.get("date", None)
        statName = request.POST.get("statName", "")
        try:
            if getattr(stats.models, statName).is_ajax_accessible:
                statModel = getattr(stats.models, statName)
        except AttributeError:
            context["error"] = "_Incorrect statName %s" % statName

        if statModel and date and user.is_authenticated() and user.is_active:
            # Validate and attempt to find all at once.
            try:
                stat = statModel.objects.filter(date=date).filter(user=user)
                # Only continue if we have a stat to delete
                if len(stat):
                    # Get ourselves the stat from the returned list
                    stat = stat[0]
                    # Delete the stat
                    stat.delete()
                    # Object still exists in memory and we can serialize it.
                    context["stat"] = stat
            except ValidationError as err:
                # Validation Errors return a list of error strings.
                context["error"] = "".join(err.__str__())
    
        # Deal with non-content and non-error state
        if context["error"] == None and context["stat"] == None:
            context["error"] = "_No record to delete."
    else:
        context["error"] = "_Service only accepts HTTP POST requests."

    return json_response_from(context)



def describe(request):
    """Return a JSON friendly description of a model available to the user 
    via an HTTP GET.
    
    The request requires previous authentication, and validates authentication
    via cookie.
    
    A JSON response will be returned for interpretation by the client.
    
    The names of the models returned will be suitable for use in web requests,
    although may not be human readable.
    
    Required arguments:
        -> model (string)
    """
    # Register the available models below (for now).
    available_models = [
        "Eggs",
        "Weight",
    ]
    context = {
        # If there is an error, this will not be null.
        "error": None,
        # Will always be an object.
        "description": {},
    }
    user = request.user
    if user.is_authenticated() and user.is_active:
        for available_model in available_models:
            for m in models.get_models():
                if available_model == m.__name__:
                    # Instance method, need an instance to call desribe.
                    context["description"][available_model] = m().describe()
                    # Match the first only and move on.
                    break

    # Deal with errors of some kind.
    if context["error"] == None and context["description"] == {}:
        context["error"] = "_No stat description available."

    return json_response_from(context)
