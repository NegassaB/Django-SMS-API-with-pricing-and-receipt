"""
The acutal urls.py file that will do most of the work.
"""
from django.urls import path, include

from commons.apiviews import TypeList, TypeDetail

"""
describe the entire urlpattern here.
"""

app_name = "commons"

urlpatterns = [
    path("types/", TypeList.as_view(), name="type_list"),
    path("types/<int:pk>/", TypeDetail.as_view(), name="type_details"),
    # path("prices/", PriceList.as_view(), name="price_list"),
    # path("prices/<int:pk>/", PriceDetail.as_view(), name="price_details"),
]
