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
