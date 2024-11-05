from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer, ProductDetailSerializer


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    data = ProductDetailSerializer(product, many=False).data
    return Response(data=data)


@api_view(['GET'])
def product_list_api_view(request):
    # step 1: Collect products (QuerySet)
    products = (Product.objects.select_related('category')
                .prefetch_related('tags', 'reviews').all())

    # step 2: Reformat(Serialize) QuerySet to list of Dictionaries (QueryDict)
    data = ProductSerializer(instance=products, many=True).data

    # step 3: Return response as JSON
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_api_view(request):
    dict_ = {
        'str': 'Hello world',
        'int': 100,
        'float': 2.77,
        'bool': True,
        'list': [1, 2],
        'dict': {"key": "value"}
    }
    return Response(data=[dict_])
