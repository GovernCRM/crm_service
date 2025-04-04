from lists.models import List


class ListSerializer:
    class Meta:
        model = List
        fields = '__all__'