# from django.urls import path
# from . import views

# urlpatterns = [
#     path("map/", views.ramen_map, name="ramen_map"),
#     path("shop/<int:shop_id>/", views.shop_detail, name="shop_detail"),
#     path("shop/<int:shop_id>/add_review/", views.add_review, name="add_review"),
#     path("search/", views.search_shops, name="search_shops"),
#     path("add_review/<int:shop_id>/", views.add_review, name="add_review"),
#     path("generate_csv/", views.generate_csv, name="generate_csv"),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path("map/", views.ramen_map, name="ramen_map"),
    path("shop/<int:shop_id>/", views.shop_detail, name="shop_detail"),
    path("shop/<int:shop_id>/add_review/", views.add_review, name="add_review"),
    path("search/", views.search_shops, name="search_shops"),
    path("generate_csv/", views.generate_csv, name="generate_csv"),
]
