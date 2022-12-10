from rest_framework import serializers


class FilterRightListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by('level')
        return super().to_representation(data)
