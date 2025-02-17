from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from products.serializers import (ProductSerializer,
                                  ProductValidateSerializer)
from django.db import transaction
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        return Response(data={'error': 'Product not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductSerializer(product, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data.get('title')
        product.text = serializer.validated_data.get('text')
        product.price = serializer.validated_data.get('price')
        product.is_active = serializer.validated_data.get('is_active')
        product.category_id = serializer.validated_data.get('category_id')
        product.tags.set(serializer.validated_data.get('tags'))
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'id': product.id, 'title': product.title})
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_list_create_api_view(request):
    print(request.user)
    if request.method == 'GET':
        # step 1: Collect products from DB (QuerySet)
        products = Product.objects.select_related('category').prefetch_related('tags', 'reviews').all()

        # step 2: Reformat QuerySet to List of dictionaries
        data = ProductSerializer(products, many=True).data

        # step 3: Return Response
        return Response(data=data,
                        status=status.HTTP_200_OK)  # data = dict / list of dict
    elif request.method == 'POST':
        # step 0: Validation (Existing, Typing and Extra)
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})

        # step 1: Receive data from Validated Data
        title = serializer.validated_data.get('title')  # None
        text = serializer.validated_data.get('text')
        price = serializer.validated_data.get('price')
        is_active = serializer.validated_data.get('is_active')  # Y
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')

        # step 2: Create product by received data
        with transaction.atomic():
            product = Product.objects.create(
                title=title,
                text=text,
                price=price,
                is_active=is_active,
                category_id=category_id,
            )
            product.tags.set(tags)
            product.save()

        # step 3: Return Response as product (optional) and status
        return Response(status=status.HTTP_201_CREATED,
                        data={'id': product.id, 'title': product.title})
