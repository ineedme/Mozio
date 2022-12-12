from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers

from providers_service_area.models import Provider, ServiceArea


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"


#class ServiceAreaSerializer(GeoFeatureModelSerializer):
class ServiceAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceArea
        fields = "__all__"
        #geo_field = 'area'


class ResultsSerializer(serializers.ModelSerializer):
    # Serializer get_providers_in_the_area return
    provider = serializers.SerializerMethodField('get_provider_name')

    class Meta:
        model = ServiceArea
        fields = ["name", "price", "provider"]

    def get_provider_name(self, obj):
        return obj.provider.name
