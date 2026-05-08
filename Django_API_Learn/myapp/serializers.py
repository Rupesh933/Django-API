from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product

# User Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # only expose these fields

# Category Serializers
class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()  # add a custom field to count the number of products in each category

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count', 'created_at']
    
    def get_product_count(self, obj):  # this method will be called to populate the product_count field for each category
        return obj.products.count()  # use the related_name 'products' to count the number of products in this category
    
# Product Serializers (List)
class ProductListSerializers(serializers.ModelSerializer):  # this serializer is used for listing products, it includes the category name but not the full category details
    category_name = serializers.CharField(  # this field will show the name of the category instead of the category id
        source = 'category.name',  # use the source argument to specify that this field should get its value from the name field of the related category object
        read_only = True  # this field is read-only because it's derived from the category relationship and should not be set directly when creating or updating a product
    )
    created_by = UserSerializer(read_only=True)  # this field will show the details of the user who created the product, it's read-only because it should be set automatically based on the authenticated user

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'stock',
            'category_name', 'created_by',
            'is_active', 'created_at'
        ]

# Product Serializer (Details/Created)
class ProductSerailizer(serializers.ModelSerializer):
    # why category_name is added here? because when we create or update a product, we want to show the category name in the response instead of the category id. This makes the API response more user-friendly and easier to understand, 
    category_name = serializers.CharField(
        source = 'category.name',
        read_only = True
    )

    class Meta:
        model = Product
        fields = '__all__'  # all fields
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    # custom Validation
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('price must be greater than 10')
        return value
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock cannot be negative!')
        return value
    
    # validate multiple field together
    def validate(self, data):  
        if data.get('stock') == 0 and data.get('is_active'):
            raise serializers.ValidationError(
                'Cannot activate product with 0 stock'
            )
        return data
    
# Register serializers
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)  # password field is write-only and must be at least 8 characters long
    password2 = serializers.CharField(write_only=True)  # password2 is a confirmation field to ensure the user enters the same password twice

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['passoword'] != data['password2']:
            raise serializers.ValidationError('Password do not match')
        return data
    
    def create(self, validate_data):
        validate_data.pop('password2')
        user = User.objects.create_user(**validate_data)
        return user
    