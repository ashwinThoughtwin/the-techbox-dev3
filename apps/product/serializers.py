from .models import Item,ItemAssign,Employee
from rest_framework import serializers

class Item_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id',"name","status"]

class ItemAssignSerializer(serializers.ModelSerializer):
    # assign_to = serializers.ReadOnlyField(source='assign_to.name', read_only=True)
    # assign_item = serializers.ReadOnlyField(source='assign_item.name', read_only=True)
    class Meta:
        model = ItemAssign
        fields = ['id',"assign_to","assign_item"]
       