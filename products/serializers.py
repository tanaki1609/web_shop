from rest_framework import serializers
from products.models import Product, Category, Tag
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name parent'.split()


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


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=5, max_length=255)
    text = serializers.CharField(default='no text')
    price = serializers.FloatField(min_value=1, max_value=1000000)
    is_active = serializers.BooleanField(default=False)
    category_id = serializers.IntegerField(min_value=1)
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))

    # def validate(self, attrs):
    #     category_id = attrs['category_id']
    #     try:
    #         Category.objects.get(id=category_id)
    #     except Category.DoesNotExist:
    #         raise ValidationError('Category does not exist!')
    #     return attrs

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist!')
        return category_id

    def validate_tags(self, tags):  # [1,2,100]
        tags_from_db = Tag.objects.filter(id__in=tags)  # [1,2]
        if len(tags_from_db) != len(tags):
            raise ValidationError('Tag does not exist!')
        return tags
