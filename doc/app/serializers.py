
from rest_framework import serializers

from .models import Affinda


class AffindaSerializer(serializers.ModelSerializer):
    """
    AffindaSerializer class is created with Affinda Model and added
    all field from AffindaSerializer Model
    """

    class Meta:
        model = Affinda
        fields = "__all__"
