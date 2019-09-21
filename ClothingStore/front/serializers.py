from rest_framework.serializers import ModelSerializer

from front.models import ShopCat


class ShopSerializer(ModelSerializer):
    class Meta:
        model = ShopCat
        fields = ['cid','uid']


