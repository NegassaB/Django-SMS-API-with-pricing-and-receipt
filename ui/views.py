from django.shortcuts import render

# Create your views here.


"""
This method is called by the urlpattern in the urls.py file to redirect and present
the view for the root request. It will render the html file found in the templates/
commons/homepage and return it w/ all it's necessary components. Notice that it
doesn't have a context dictionary object in the returned render object b/c the it's
just a simple placeholder display.
"""


def homepage(request):
    return render(request, "ui/homepage.html")


def ui_login(request):
    return render(request=request, template_name="ui/login.html")
