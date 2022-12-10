from rest_framework import serializers
from promo_app.models import *


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name', 'code')


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class TypeCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150, source='type_name')

    class Meta:
        model = TypeCategory
        fields = ('id', 'name')


class CategoryListWithActiveBundleSerializer(serializers.ModelSerializer):
    type = TypeCategorySerializer()
    categorydictionary = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='translation'
    )
    children = RecursiveSerializer(many=True, source='active_children')

    class Meta:
        model = Category
        fields = ('id', 'type', 'categorydictionary', 'children')
