from rest_framework import serializers
from products.models import Product, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    tags = TagSerializer(many=True)
    tag_names = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title price category tags tag_names category_name reviews'.split()
        depth = 1

    def get_tag_names(self, product):
        return [tag.name for tag in product.tags.all()][0:2]
        # return TagSerializer(product.tags.order_by('name'), many=True).data[0:2]
