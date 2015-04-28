Web Applications with Django
============================
Django is a web application framework. One would use django for when you need something more than a simple web page: a web based todo list, you want to write your own blog engine, a dynamic social feed, an interactive family tree for your family, etc.

There are many frameworks out there. Django is a big one, and a well supported one, in the Python community. Whether or not you specifically use Django after the class, working with Django will give you an idea of how to roll your own web application should you need to. If you do not do a lot of work on the web, it will also give you a chance to hone your web skills.

* see [Django homepage](https://www.djangoproject.com/)
* see [Django tutorial](https://docs.djangoproject.com/en/1.5/intro/tutorial01/)



Note on folder organization
---------------------------
While each piece of Django is well constructed and easy to understand, Django itself is large and has a lot of depth to it. In this case, the `examples` folder contains the finished version of what we're going to build, as reference. We will implement small pieces of our application over the example, testing along the way. This will allow us to explore the major pieces of Django, how they work, and what we can use them for, while cutting down on the number of potential typos due to the shear amount of code.



Prequisites
-----------
Django, like many frameworks, can be a bit specific about what code they allow, and what they depricate, between versions. These examples are based on the following specific version of Django:

    pip install django==1.5.1
    # This code is part of the Django community:
    pip install django-registration==1.0

* see [Django install](https://docs.djangoproject.com/en/1.5/topics/install/)
* see [Django registration application](https://django-registration.readthedocs.org/en/v1.0/)



What we are building: a "bulletin board"
----------------------------------------
In the "old days" bulletin boards were where people stuck notes. We're going to make a bulletin board that allows pepole to leave notes for us. This project will not only give us an overview of Django, it will provide an opportunity to learn about the various topics we need to think about when developing a web application.

To see our final product, let's go into `examples/bulletin` and run the following command:

    python manage.py runserver
    
Take a walkthrough of our sample application at:

    http://localhost:8000/



Getting Started
---------------
Django expects you to structure your code in a particular way. The `django-admin.py` tool can be used to get us going with the boiler plate code for our project. Let's build the scaffolding for our project:

    django-admin.py startproject bulletin

NOTE: If you have trouble running django-admin.py on Windows, try running it literally. Depending on your Python install, the command above might look like:

    python c:\Python27\Scripts\django-admin.py startproject bulletin

This should give us a directory that looks something like:

    bulletin/
        manage.py
        bulletin/
            __init__.py
            settings.py
            urls.py
            wsgi.py

We have a barebones web application. Most commands will be run from inside of the root `bulletin` directory from here on out, and we'll do quite a bit from the commandline. Let's do the following and see what happens:

    cd bulletin
    python manage.py runserver

Open a web browser and visit our hello world application at:

    http://127.0.0.1:8000/

Yay!



Configuring our server
----------------------
Files will always be referred to as if we're already inside of the root `bulletin` directory. Open the `bulletin/settings.py` file in an editor and make the following changes noted in the `#CHANGEME` comments:

```python
# Django settings for bulletin project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # CHANGEME - use a simple backend for now.
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # CHANGEME - name the database.
        'NAME': 'bulletin.db3',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}
```

Let's see if things work. There is a `manage.py` script that we just used to start the server. Let's use it to create our database and create our admin user.

    python manage.py syncdb

When asked if you want to create a superuser, say yes. Create the following user (to make things easy to remember):

    name: root
    email: root@devnull.com
    password: password

Excellent!

Let's make a couple more changes to `bulletin/settings.py`:

```python
# snip....
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # CHANGEME: uncomment.
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # CHANGEME: uncomment.
    'django.contrib.admindocs',
)
# snip...
```

And a change to `bulletin/urls.py`:

```python
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# CHANGEME uncomment
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bulletin.views.home', name='home'),
    # url(r'^bulletin/', include('bulletin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # CHANGEME uncomment
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # CHANGEME uncomment
    url(r'^admin/', include(admin.site.urls)),
)
```

The `bulletin/urls.py` file is important for determining how our application reacts to URLs as part of the HTTP request. Many frameworks refer to url interpretation as routing, and the url patterns themselves as routes. We will return to this file later.

Let's test out our application now:

    python manage.py runserver

And visit `http://127.0.0.1:8000/` in a web browser. Not much has changed. Let's try visiting the admin page at:

    http://127.0.0.1:8000/admin

Ahh, some things have changed. We've activated our admin control panel. Log in with your superuser name that you created, which is hopefully `root` and `password`.

Click around. One thing that Django is known for is all of the builtin stuff, like a full admin console that is ready to go before our app is.

The admin console is turned off by default, and given the power, you can probably see why.



What is an App
--------------
Django has the concept of projects and apps. 

* A project is equivalent to an entire website.
* The project provides overall configuration: settings.py, urls.py, management via manage.py, etc.
* An application is a single, macro feature that is part of an entire website.
* Apps are pluggable/removeable, fitting with the dynamic nature of python.
* A project might have a single app, but can also have multiple applications that fit together to make one complete project (website).

The app layer is where we have the most power in Django. We already saw our first app: the admin page. But we don't want to expose the admin page to the world as our main app. We also installed the `django-registration` app when we first started.

An app is made up of two main conceptual parts: the model layer, which is our database layer; the view layer, which provides the logic for interpreting requests and returns a response, usually a web page, to the requester.



Users and user registration
---------------------------
We'll want users to be able to login to our application to add notes to our board. Let's configure the `django-registration` app to work for us, but using a simple and toned down version. We must tell Django to use our application within `bulletin/settings.py`:

```python
# snip....
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    
    # CHANGEME: add registration module.
    'registration',
    # CHANGEME: here's the other module we're about to make to handle
    # the registration.
    'simpleauth',
)

# CHANGEME: redirect successful logins to the homepage, too.
LOGIN_REDIRECT_URL = '/'

# snip...
```

And in `bulletin/urls.py`:

```python
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# CHANGEME include our new application.
from simpleauth.views import SimpleAuthRegistrationView
# CHANGME include code to help us login and logout.
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bulletin.views.home', name='home'),
    # url(r'^bulletin/', include('bulletin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # CHANGEME allow registration and authentication.
    url(r'^register/$', SimpleAuthRegistrationView.as_view(), name='registration_register'),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='auth_logout'),

)
```

Whenever we add an application, we need to setup our database to make use of the models within that application. Run the following commands:

    python manage.py syncdb
    python manage.py runserver

Doh? What happened? Looks like we got ahead of ourselves. The `django-registration` module provides a lot of help, but we need to help ourselves, too, and supply some of our own code.


Authentication, and Templates, and views
----------------------------------------
Django differentiates views, which are the python code that manage the logic for a particular HTTP request, and templates, which are the HTML pages and HTML fragments that are displayed to the user. To allow a user to register, we need to subclass one of the `django-registration` views and override some things.

Let's create our first application: one that will be responsible for allowing user registration and authentication.

    python manage.py startapp simpleauth

Excellent. Let's create our first view, which is the missing view that caused the error in `bulletin/urls.py` above. Open up `simpleauth/views.py` and:

```python
# Importing from the django-registration package.
# We're going to use the one step registration process, not the
# two step registration process.
from registration.backends.simple.views import RegistrationView

# We inherit almost everything. The biggest thing that we want to
# override is where the user goes after they register.
class SimpleAuthRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        # Redirect the user to our home page.
        return "/"
```

The registration view handles the logic of the HTTP request, but the HTML that gets returned to the user still needs to be defined. Let's make ourselves a templates directory at:

    mkdir -p simpleauth/templates/registration

And let's add the following files in the `simpleauth/templates/registration` folder, first `registration_form.html`:

```djangotemplate
{% extends "registration/base.html" %}

{% comment %}
**registration/registration_form.html**
Used to show the form users will fill out to register. By default, has
the following context:

``form``
    The registration form. This will be an instance of some subclass
    of ``django.forms.Form``; consult `Django's forms documentation
    <http://docs.djangoproject.com/en/dev/topics/forms/>`_ for
    information on how to display this in a template.
{% endcomment %}

{% block content %}

<h1>Create new account</h1>
<form action="" method="POST">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
    </table>
    <input type="submit" name="submit" value="Submit">
</form>

{% endblock %}
```

Followed by `base.html`:

```djangotemplate
<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="utf-8">
        <title>Bulletin</title>
        {% block extra_head %}
        {% endblock %}
    </head>
    <body>
        <h1>Bulletin</h1>
        <div class="content">
            {% block content %}        
            {% endblock %}
        </div>
    </body>
</html>
```

And `login.html`:

```djangotemplate
{% extends "registration/base.html" %}

{% block title %}Log in{% endblock %}

{% block content %}
<h1>Log in</h1>
{% if form.errors %}
<p class="error">Please correct the errors below:</p>
{% endif %}
<form method="post" action="?next={{ next|default:"/" }}">
    {% csrf_token %}
    <dl>
        <dt>
            <label for="id_username">Username:</label>
            {% if form.username.errors %} <span class="error">{{ form.username.errors|join:", " }}</span>{% endif %}
        </dt>
        <dd>{{ form.username }}</dd>
        <dt>
            <label for="id_password">Password:</label>
            {% if form.password.errors %} <span class="error">{{ form.password.errors|join:", " }}</span>{% endif %}
        </dt>
        <dd>{{ form.password }}</dd>
        <dt>
            <input type="submit" value="Log in" />
        </dt>
    </dl>
</form>
{% endblock %}

{% block content-related %}
<p>If you don't have an account, you can <a href="/register/">sign up</a> for one.
{% endblock %}
```

And `logout.html`:

```djangotemplate
{% extends "registration/base.html" %}

{% block title %}Logged out{% endblock %}

{% block content %}
<h1>You've been logged out.</h1>
<p>Thanks for stopping by; when you come back, don't forget to <a href="/login/">log in</a> again.</p>
{% endblock %}
```

This introduces us to the Django templating language. There are many templating meta-languages/frameworks out there. All templating languages boil down to the same thing: they allow the user to insert dynamically generated content within existing, and generalized, static content (usually HTML).

* see [Django Templating](https://docs.djangoproject.com/en/1.5/topics/templates/)

Try out what we have:

    python manage.py runserver

    # Point a browser to
    http://localhost:8000/register/
    
Correctly registering will take us to a 404 because our application doesn't exist. Just for fun, try logging in:

    http://localhost:8000/login/
    
This will also take us to a 404 at root `/`, but that is good and proves our application will work. Let's add the main part of our application: the notes.



Our own, custom app: notes
--------------------------
Our third party registration application handles registration. Our notes application, which we will develop ourselves, will manage the notes people leave on the bulletin board.

    python manage.py startapp notes



Models - our database layer
---------------------------
Django, like SQLAlchemy, provides an ORM layer that allows us to model our objects, and as such our databases, using regular Python classes. This doesn't mean that you can't, or shouldn't, use SQL, but it does cut out a layer that is present in many older web applications without ORM:

* Build a bunch of SQL statements.
* Protect your SQL statements from attacks.
* Build data models that represent your database records within your code.

The SQL is still executed in the background, but we don't need to write it into our code if we don't want to. 

* see [Django Model Documentation](https://docs.djangoproject.com/en/1.5/topics/db/models/)

Open up `notes/models.py` and make the following changes:

```python
from django.db import models
# CHANGEME: Notes models need authors.
from django.contrib.auth.models import User
# CHANGME: To auto set dates.
from datetime import datetime

class Note(models.Model):
    """A single note on our bulletin board.
    """
    # Not shown: all models have an id field by default.
    # Who wrote the note.
    author = models.ForeignKey(User)
    # When the note was written, defaulting to the callback now.
    date = models.DateField('creation date', default=datetime.now)
    # All notes must have unique titles.
    title = models.CharField(max_length=200, unique=True, help_text='Each note title must be unique.')
    # The body of the note.
    body = models.TextField(help_text='Write as much as you want.')
```

This code change also represents a structural change to our database. When we have new tables to create, we need to run:

    python manage.py syncdb
    
Ooops. Our application isn't yet recognized by Django. Let's open `bulletin/settings.py` and have Django work with our app:

```python
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    
    'registration',
    'simpleauth',
    # CHANGEME: Recognize our notes application.
    'notes',
)
```

And let's try this again:

    python manage.py syncdb

It's subtle, but we should have seen a `notes_note` table get created. Excellent!



Creating a few test models
--------------------------
By default, the admin view has access to only the tables we allow it to have access to. Let's create a `notes/admin.py` file and add the following to it:

```python
from django.contrib import admin
from notes.models import Note

admin.site.register(Note)
```

Restart the development server:

    python manage.py runserver

And visit the admin page at:

    http://localhost:8000/admin

Use the admin interface to do a couple of things:

* Check out the user table and make sure a user that you registered earlier exists (click on the change button).
* Add a few notes to the notes table (click on the add button).

Excellent! Now we have some data to work with. 

Bonus: If you are facile with sqlite3, feel free to use the client to open up our database file and browse the database. You can confirm that our models are being saved, and they look like one would expect in an SQL database. Please don't change the data directly though (at least right now).



Building our homepage view and first template
---------------------------------------------
We could have built the homepage first, but it would have been empty. We now have the infrastructure we need to finish our application. Let's start with our homepage.

When HTTP requests come in, Django first needs to decide where to send them to. They're always routed to some function or method. Let's modify `bulletin/urls.py`:

```python
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bulletin.views.home', name='home'),
    # url(r'^bulletin/', include('bulletin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^register/$', SimpleAuthRegistrationView.as_view(), name='registration_register'),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='auth_logout'),

    # CHANGEME: Our homepage is managed by the notes app.
    url(r'^$', 'notes.views.index', name='home'),
)
```

We've informed django to send all root path `/` requests to the function named `home` in `notes.views`. We've identified this route by the name of "home", although for our simple application this isn't really necesary.

* see [Django URL dispatcher](https://docs.djangoproject.com/en/1.5/topics/http/urls/)

Let's open `notes.views` and build our first view:

```python
from django.shortcuts import render

from notes.models import Note

def index(request):
    context = {
        # Get all of the notes in the database, in descending order.
        # Instead of SQL, this is how Django provides a cross-database
        # query engine.
        'notes': Note.objects.all().order_by('-date')
    }
    # Map our context object that we just built, with all of our models,
    # into our template. Whatever the results will be passed back as
    # the response to this particular HTTP request.
    return render(request, 'notes/index.html', context)
```

We could always send straight text, but why do that when we have Django templates? Assuming you are within the root bulletin directory (next to manage.py), make the following directories:

    mkdir -p notes/templates/notes

The reason for the double notes has to do with how Django searches for templates. Each app can have a templates folder, and it's good to namespace an apps templates even within its own templates folder.

Create the files `notes/templates/notes/index.html` and add the code within:

```djangotemplate
{% comment %}
Display note cards if any notes exist in the database.

By default, has the following context:

* notes
    * List of all Note models.
{% endcomment %}
{% if notes %}
    <h2>{{ notes|length }} notes for you</h2>
{% comment %} Condensed formatting for notes due to inline-block styling. {% endcomment %}
{% for note in notes %}<div class="note">
    <h2>{{ note.title }}</h2>
    <p>
        {{ note.body }}
    </p>
    <small>created {{ note.date }} by {{ note.author }}</small>
</div>{% endfor %}
{% else %}
    <h2>No notes for you</h2>
{% endif %}
```

Excellent! Try out our simple home page now.

    python manage.py runserver
    # then browse to http://localhost:8000/

Excellent! You have a page!



Building a better homepage
--------------------------
The templates that we used in the registration page were a bit better formed. Let's change our template to be more like them and take a look at exactly what this provides us. Open up `notes/templates/notes/index.html` and drop in the new line at the top of the template:

```djangotemplate
{% extends "notes/base.html" %}
{% comment %} CHANGME: Inherit a base template. {% endcomment %}

{% comment %}
Display note cards if any notes exist in the database.

By default, has the following context:

* notes
    * List of all Note models.
{% endcomment %}
{% comment %} CHANGME: Add block tags. {% endcomment %}
{% block content %}
{% if notes %}
    <h2>{{ notes|length }} notes for you</h2>
{% comment %} Condensed formatting for notes due to inline-block styling. {% endcomment %}
{% for note in notes %}<div class="note">
    <h2>{{ note.title }}</h2>
    <p>
        {{ note.body }}
    </p>
    <small>created {{ note.date }} by {{ note.author }}</small>
</div>{% endfor %}
{% else %}
    <h2>No notes for you</h2>
{% endif %}
{% endblock %}
```

Now create the `notes\templates\notes\base.html` template with the following:

```djangotemplate
<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="utf-8">
        <title>Bulletin</title>
        {% block extra_head %}
        {% endblock %}
    </head>
    <body>
        <h1>Bulletin</h1>
        <div class="content">
            {% block content %}        
            {% endblock %}
        </div>
    </body>
</html>
```

And test. This is one of those "if all goes well, everything looks the same."

Excellent. Now that things work, let's make things a bit prettier. To deploy static files: css, images, JavaScript, etc... with our site, we want to be able to serve static files. Open `bulletin/settings.py` and make the following change:

```djangotemplate
# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    
    # CHANGEME: Add a location for a main set of static files.
    os.path.join(os.path.realpath(os.path.dirname(__file__)), "../static"),
)
```

Create the `static/` directory. 

Create `static/main.css` and add the following content to it:

```css
* {
    -moz-box-sizing: border-box;
    box-sizing: border-box;
}
html, body {
    margin: 0;
    padding: 0;
}

body > h1 {
    padding: 1em;
    background-color: #555;
    text-align: right;
    color: #eee;
    margin: 0;
}

.content {
    width: 80%;
    margin: auto;
}

.content > h2 {
    text-align: center;
}

.note {
    display: inline-block;
    vertical-align: top;
    
    width: 18%;

    margin: 1%;
    padding: 0.3em;
    
    overflow: auto;
    border: 1px solid #aaa;
}
.note > h2 {
    margin: 0;
    
    text-shadow: 1px 1px 0 #aaa;
}
.note > p {
    min-height: 10em;
    margin: 0;
    color: #444;
}
.note > small {
    display: block;
    text-align: right;
    padding: 0.2em;
    color: #aaa;
}



@media screen and (max-width: 960px) {
    .note {
        width: 31%;
    }
}



@media screen and (max-width: 768px) {
    .content {
        width: 88%;
    }
    .note {
        width: 48%;
    }
}



@media screen and (max-width: 550px) {
    .content {
        width: 96%;
    }
    .note {
        width: 100%;
    }
}
```

Modify `notes/templates/notes/base.html` to include the following:

```djangotemplate
<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="utf-8">
        <title>Bulletin</title>
        {% block extra_head %}
        {% endblock %}
        
        {% comment %} CHANGEME: Add styling {% endcomment %}
        {% load staticfiles %}
        <link href="{% static "main.css" %}" rel="stylesheet"/>
    </head>
    <body>
        <h1>Bulletin</h1>
        <div class="content">
            {% block content %}        
            {% endblock %}
        </div>
    </body>
</html>
```

Same thing for `simpleauth/templates/registration/base.html`:

```djangotemplate
<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="utf-8">
        <title>Bulletin</title>
        {% block extra_head %}
        {% endblock %}
        
        {% comment %} CHANGEME: Add styling {% endcomment %}
        {% load staticfiles %}
        <link href="{% static "main.css" %}" rel="stylesheet"/>
    </head>
    <body>
        <h1>Bulletin</h1>
        <div class="content">
            {% block content %}        
            {% endblock %}
        </div>
    </body>
</html>
```

This is a great time to check out the home page and the other pages like `login/`. They should look different.



Adding notes
------------
We want to allow logged in users to be able to add notes. Create `notes/templates/notes/add.html` and add the contents to the file:

```djangotemplate
{% extends "notes/base.html" %}

{% comment %}
Allow logged in users to add notes.

Context properties expected:

* user: Should be provided by django.
* form: provided by view.
{% endcomment %}

{% block content %}
{% if user.is_authenticated %}
    <h2>Add a note</h2>
    <form action="{% url 'add_note' %}" method="post">
        {% csrf_token %}
        <table>
            {{ form.as_table }}
        </table>
        <input type="submit" value="add new note" />
    </form>
{% else %}
    <h2>Only logged in users can add notes.</h2>
{% endif %}
{% endblock %}

```

Append the following to `notes/views.py` (which isn't the best practice in coding, especially importing below existing code, but it will do right now):

```python
# CHANGEME: Class based instead of functional based view.
from django import forms

# A form that excludes fields we want to populate ourself via session data.
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ('author','date',)

# We only allow creation of notes.
from datetime import datetime
from django.views.generic.edit import CreateView

class NoteCreate(CreateView):
    form_class = NoteForm
    model = Note
    template_name = 'notes/add.html'
    success_url = '/'
    
    def form_valid(self, form):
        # Populate the information ourselves that was excluded.
        form.instance.author = self.request.user
        form.instance.date = datetime.now()
        # Delegate validation to parent class.
        return super(NoteCreate, self).form_valid(form)
```

And we need to add a route in `bulletin/urls.py`:

```python
# snip....

# CHANGEME: Must include the view class.
from notes.views import NoteCreate

urlpatterns = patterns('',

    # snip....
    
    # CHANGEME: allow logged in users to add notes.
    url(r'^add/$', NoteCreate.as_view(), name='add_note'),
)
```

Excellent! With the dev server running, test the following flow:

    http://localhost:8000/logout
    http://localhost:8000/login
    http://localhost:8000/add

Try adding a valid note, and try adding an invalid note.



Lab
---
Django is a very large framework. There is a lot you can do with it, and a lot to learn. You don't even need to know the entire framework to make use of it, as you can see we've done quite a bit with a relatively small portion of Django.

Let's add some cohesiveness to our main page. Your job is to:

* Add a login link to the bottom of `notes/templates/notes/index.html` if the user is not logged in, and have that link send the user to the login page. Don't use hardcoded links.
* Add the following to `notes/templates/notes/index.html` if the user is logged in (again not using hard coded links):
    * A logout link to the bottom, and have that link send the user to the logout page.
    * An add link that sends the user to the add a note page.
* Change the `base.html` pages to allow for clicking on the banner text to send the user home.
    * Bonus: change the CSS to make the banner link look more like a banner, not like a giant link.
* Try to add a priority column to the Note model that is a number between the values of 1 through 5. As you work through this process, what are the various steps you need to take. NOTE: this is intended to be more of a thought experiment, but see how far you can get. Be ready to talk about the immediate problems you run into with existing data, various steps you would do to get through this process, the files you would need to change, and why.

* see [Django template tags and filters](https://docs.djangoproject.com/en/1.5/ref/templates/builtins/)
* see [Notes on syncdb](https://docs.djangoproject.com/en/1.5/ref/django-admin/#syncdb)
* see [data migration with South](http://south.aeracode.org/)
