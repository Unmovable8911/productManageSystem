from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("new-catagory/", views.new_catagory, name="new_catagory"),
    path("picture/<uuid:product_identity>", views.full_picture, name="full_picture"),
    path("delete_product/<uuid:product_identity>", views.delete_product, name="delete_product"),
    path("delete_catagory/<uuid:catagory_identity>", views.delete_catagory, name="delete_catagory"),
    path("search-result/", views.search_result, name="search_result")
]
