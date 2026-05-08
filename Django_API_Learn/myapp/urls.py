from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Routers auto generates all URLs for viewSet
route = DefaultRouter()
route.register('products', views.ProductViewSet, basename='products') # this line registers the ProductViewSet with the router, which will automatically generate URLs for all the standard actions (list, create, retrieve, update, partial_update, destroy) based on the viewset's methods and the specified basename.
route.register('categories', views.CategoriesViewSet, basename='category')

urlpatters = [
    # ViewSet URLs (auto generated)
    path('', include(router.urls)),

    # fuction based urls
     path('products-list/',         views.product_list,   name='product-list'),
    path('products/<int:pk>/',     views.product_detail, name='product-detail'),
    path('products/create/',       views.create_product, name='create-product'),
    path('products/<int:pk>/update/', views.update_product, name='update-product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete-product'),

    # Auth
    path('auth/', include('myapp.auth_urls')),
]