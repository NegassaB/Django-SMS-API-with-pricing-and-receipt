from django.shortcuts import render

# Create your views here.

base_url = "http://localhost:8055/"


def homepage(request):
    return render(request=request, template_name="commons/index.html")
