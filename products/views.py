from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image

import os
from .models import Product, Catagory
from .forms import ProductForm

# Create your views here.
def product_list(request):
    # query all products and categories
    products = Product.objects.order_by("name")
    catagories = Catagory.objects.order_by("title")

    # paginator
    paginator = Paginator(products, 20)
    page = request.GET.get('page')

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, diliver first page
        paginated_products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_products = paginator.page(paginator.num_pages)


    # handle the product form
    if request.method != "POST":
        product_form = ProductForm()
    else:
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            # edit the uploaded image
            try:
                uploaded_image = request.FILES["picture"] # get image
                image = Image.open(uploaded_image) # load image
                aspect_ratio = image.width / image.height # calculate image ratio
                image.thumbnail((100, int(100 / aspect_ratio))) # resize image
                file_name = product_form.cleaned_data["name"] # name of the product
                extension = (uploaded_image.name).split('.')[-1]
                # save the resized image to the temporary directory
                image.save(f"media/temp/{file_name}.{extension}")
                # save the image to the database
                product_form.instance.thumnail.save(file_name, open(f"media/temp/{file_name}.{extension}", "rb"))
                os.remove(f"media/temp/{file_name}.{extension}")
            except MultiValueDictKeyError:
                pass
            
            # save the form and redirect to home page
            product_form.save()
            return redirect(reverse("product_list"))
    context = {
        "products": paginated_products,
        "catagories": catagories,
        "product_form": product_form,
    }
    return render(request, "product_list.html", context)

def new_catagory(request):
    new = Catagory(title=request.POST.get("catagory-title"))
    new.save()
    return redirect(reverse("product_list"))

def delete_product(request, product_identity):
    product = Product.objects.get(identity=product_identity)
    product.delete()
    return redirect(reverse("product_list"))

def delete_catagory(request, catagory_identity):
    catagory = Catagory.objects.get(identity=catagory_identity)
    catagory.delete()
    return redirect(reverse("product_list"))

def search_result(request):
    query = request.GET.get("query", "")
    products = Product.objects.filter(
        name__icontains=query
    ) | Product.objects.filter(
        catagory__title__icontains=query
    ) | Product.objects.filter(
        remark__icontains=query
    )

    # paginator
    paginator = Paginator(products, 20)
    page = request.GET.get('page')

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, diliver first page
        paginated_products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_products = paginator.page(paginator.num_pages)

    context = {"query": query, "products": paginated_products}
    return render(request, "search_result.html", context)

def full_picture(request, product_identity):
    # show the full size picture of the product
    product = Product.objects.get(identity=product_identity)
    picture_url = product.picture.url
    product_name = product.name
    context = {"picture_url": picture_url, "product_name": product_name}
    return render(request, "full_picture.html", context)
