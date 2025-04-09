from rest_framework import serializers
from lists.models import List


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        exclude = ['polygon']


class ListLevelSerializer(GroupSerializer):
    sub_lists = serializers.SerializerMethodField()

    class Meta(GroupSerializer.Meta):
        pass

    def get_sub_lists(self, obj):
        return GroupSerializer(obj.sub_lists.all(), many=True).data


class CommunitySerializer(GroupSerializer):
    sub_lists = serializers.SerializerMethodField()

    class Meta(GroupSerializer.Meta):
        pass

    def get_sub_lists(self, obj):
        return ListLevelSerializer(obj.sub_lists.all(), many=True).data
