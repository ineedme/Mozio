import json

from drf_yasg import openapi
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point

from providers_service_area.models import Provider, ServiceArea
from providers_service_area.serializers import ProviderSerializer, ServiceAreaSerializer, ResultsSerializer

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema



@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      operation_description="List All Providers",
                      operation_summary="list")
                  )
@method_decorator(name='create',
                  decorator=swagger_auto_schema(
                      operation_description="Create new Provider",
                      operation_summary="create")
                  )
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(
                      operation_description="Retrieve Provider by id",
                      operation_summary="retrieve")
                  )
@method_decorator(name='update',
                  decorator=swagger_auto_schema(
                      operation_description="Update Provider by id",
                      operation_summary="update")
                  )
@method_decorator(name='destroy',
                  decorator=swagger_auto_schema(
                      operation_description="Destroy Provider by id",
                      operation_summary="destroy")
                  )
@method_decorator(name='partial_update',
                  decorator=swagger_auto_schema(auto_schema=None)
                  )

class ProviderViewSet(viewsets.ModelViewSet):
    """
    Provider Resource

    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()

@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      operation_description="List All Service Areas",
                      operation_summary="list")
                  )
@method_decorator(name='create',
                  decorator=swagger_auto_schema(
                      operation_description="Create new Service Area",
                      operation_summary="create")
                  )
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(
                      operation_description="Retrieve Service Area by id",
                      operation_summary="retrieve")
                  )
@method_decorator(name='update',
                  decorator=swagger_auto_schema(
                      operation_description="Update Service Areas by id",
                      operation_summary="update")
                  )
@method_decorator(name='destroy',
                  decorator=swagger_auto_schema(
                      operation_description="Destroy Service Area by id",
                      operation_summary="destroy")
                  )
@method_decorator(name='partial_update',
                  decorator=swagger_auto_schema(auto_schema=None)
                  )
class ServiceAreaViewSet(viewsets.ModelViewSet):
    """
    Service Area Resource

    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = ServiceAreaSerializer
    queryset = ServiceArea.objects.all()

    # Cache Request for 2 hours
    long = openapi.Parameter('long', in_=openapi.IN_QUERY, description='string', type=openapi.TYPE_STRING,)
    lat = openapi.Parameter('lat', in_=openapi.IN_QUERY, description='string', type=openapi.TYPE_STRING,)


    @swagger_auto_schema(operation_id="get_providers_in_the_area",
                         manual_parameters=[lat, long],
                         responses={200: ResultsSerializer(many=True)},
                         operation_summary="")
    @method_decorator(cache_page(60 * 60 * 2))
    @action(detail=False, methods=['get'], name="Get providers in the area")
    def get_providers_in_the_area(self, request):
        """
        Endpoint that takes a lat/lng pair as arguments and return a list of all polygons that include the given lat/lng
        """
        x_coords = request.GET.get('long', None)
        y_coords = request.GET.get('lat', None)
        if x_coords and y_coords:
            location = Point(float(x_coords), float(y_coords), srid=4326)
            providers_in_the_area = ServiceArea.objects.filter(area__contains=location)
            serialized = ResultsSerializer(providers_in_the_area, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
