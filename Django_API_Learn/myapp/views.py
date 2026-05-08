from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
# Create your views here.


@api_view(['GET'])  # this decorator is used to specify that this view will only accept GET requests. If a different HTTP method is used, it will return a 405 Method Not Allowed response.
@permission_classes([AllowAny])  # this decorator is used to specify that this view can be accessed by anyone, regardless of whether they are authenticated or not. This overrides the default permission classes set in the settings.py file for this specific view.
def product_list(request):
    products = Product.objects.filter(is_active=True) # this line retrieves all Product objects from the database where the is_active field is set to True. This means that only products that are currently active will be included in the list.
    serializer = ProductListSerializers(products, many=True) # many=True means accept multiple objects and products means we pass the queryset of active products to the serializer to convert them into a format that can be easily rendered into JSON for the API response.
    return Response(serializer.data)

from django.shortcuts import get_object_or_404
@api_view(['GET'])
def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk) # this line attempts to retrieve a single Product object from the database based on the primary key (pk) provided in the URL. If a product with the specified pk does not exist, it will return a 404 Not Found response instead of raising an exception.
    serializers = ProductSerailizer(product)
    return Response(serializers.data)

from rest_framework import status
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # this decorator is used to specify that this view can only be accessed by authenticated users. If an unauthenticated user tries to access this view, it will return a 401 Unauthorized response. This ensures that only logged-in users can create new products.
def created_product(request):
    serializer = ProductSerailizer(data=request.data)  # request.data = json body
    if serializers.is_valid():
        serializer.save(created_by=request.user)  # 
        return Response(serializers.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    partial = request.method == 'PATCH'   # partial update allows you to update only specific fields of a product without having to provide all the fields in the request body. If the request method is PATCH, the partial variable will be set to True, allowing for partial updates. If the request method is PUT, the partial variable will be set to False, which means that all fields must be provided in the request body for a complete update.
    serializer = ProductSerailizer(
        product,
        data = request.data,
        partial = partial  # partial=True allow updating one field and this field work when we use PATCH method 
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return Response(
        {'message':'Product deleted successfully!'},
        status=status.HTTP_204_NOT_CONTENT
    )