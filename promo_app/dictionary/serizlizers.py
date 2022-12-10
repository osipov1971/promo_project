from rest_framework import serializers
from am_app.models import (
    CategoryDictionary,
    GroupProductDictionary,
    ArticleStockUnitDictionary,
    AssortStateDictionary,
    AssortGroupStateDictionary
)


class CategoryDictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryDictionary
        fields = ('id', 'translation')


class GroupProductDictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupProductDictionary
        fields = ('id', 'translation')


class ArticleStockUnitDictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleStockUnitDictionary
        fields = ('id', 'translation')


class AssortStateDictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssortStateDictionary
        fields = ('id', 'translation')


class AssortGroupStateDictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssortGroupStateDictionary
        fields = ('id', 'translation')
