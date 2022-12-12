import json
from django.contrib.gis.geos import Point
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import caches
from model_bakery import baker
import os


from providers_service_area.models import Provider, ServiceArea
from providers_service_area.serializers import ProviderSerializer, ServiceAreaSerializer, ResultsSerializer


from rest_framework.test import APITestCase

class GetAllProvidersTest(APITestCase):
    """ Test module for GET all Providers API """

    def setUp(self):
        baker.make(Provider, name="Uber")
        baker.make(Provider, name="Lyft")
        baker.make(Provider, name="InDriver")

    def test_get_all_providers(self):
        response = self.client.get(reverse('provider-list'))
        providers = Provider.objects.all()
        serializer = ProviderSerializer(providers, many=True)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_providers_empty(self):
        Provider.objects.all().delete()
        response = self.client.get(reverse('provider-list'))
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllServiceAreasTest(APITestCase):
    """ Test module for GET all ServiceAreas API """

    def setUp(self):
        provider = baker.make(Provider, name="Uber")
        baker.make(ServiceArea, name="Florida", provider=provider)
        baker.make(ServiceArea, name="Texas", provider=provider)
        baker.make(ServiceArea, name="California", provider=provider)

    def test_get_all_serviceareas(self):
        response = self.client.get(reverse('servicearea-list'))
        serviceareas = ServiceArea.objects.all()
        serializer = ServiceAreaSerializer(serviceareas, many=True)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_serviceaea_empty(self):
        ServiceArea.objects.all().delete()
        response = self.client.get(reverse('servicearea-list'))
        serviceareas = ServiceArea.objects.all()
        serializer = ServiceAreaSerializer(serviceareas, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewProviderTest(APITestCase):
    """ Test module for inserting a new provider """

    def setUp(self):
        self.valid_payload = {
            "name": "Uber",
            "email": "example@example.com",
            "phone_number": "18338738237",
            "language": "English",
            "currency": "Dollar",
        }
        self.invalid_payload = {
            "name": "Uber",
            "phone_number": "18338738237",
            "language": "English",
            "currency": "Dollar",
        }

    def test_create_valid_provider(self):
        response = self.client.post(
            reverse('provider-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_provider_missing_value(self):
        response = self.client.post(
            reverse('provider-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_provider_invalid_phone(self):
        wrong_phone_payload = self.valid_payload
        wrong_phone_payload['phone_number'] = "ABC"
        response = self.client.post(
            reverse('provider-list'),
            data=json.dumps(wrong_phone_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_provider_invalid_email(self):
        wrong_phone_payload = self.valid_payload
        wrong_phone_payload['email'] = "ABC"
        response = self.client.post(
            reverse('provider-list'),
            data=json.dumps(wrong_phone_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateNewServiceAreaTest(APITestCase):
    """ Test module for inserting a new provider """

    def setUp(self):
        provider = baker.make(Provider, name="Uber")
        geo_fl = open("./json/fl.json").read()
        self.valid_payload = {
            "name": "Florida",
            "price": 25.00,
            "area": geo_fl,
            "provider": provider.id,
        }
        self.invalid_payload = {
            "name": "Texas",
            "area": geo_fl,
            "provider": provider.id,
        }

    def test_create_valid_servicearea(self):
        response = self.client.post(
            reverse('servicearea-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_servicearea_missing_value(self):
        response = self.client.post(
            reverse('servicearea-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_servicearea_invalid_area(self):
         wrong_area_payload = self.valid_payload
         wrong_area_payload['area'] = "ABC"
         response = self.client.post(
             reverse('servicearea-list'),
             data=json.dumps(wrong_area_payload),
             content_type='application/json'
         )
         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_servicearea_invalid_provider(self):
         wrong_provider_payload = self.valid_payload
         wrong_provider_payload['provider'] = 2
         response = self.client.post(
             reverse('servicearea-list'),
             data=json.dumps(wrong_provider_payload),
             content_type='application/json'
         )
         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetSingleProviderTest(APITestCase):
    """ Test GET single provider API """

    def setUp(self):
        self.provider = baker.make(Provider, name="Uber")

    def test_get_valid_single_provider(self):
        response = self.client.get(
            reverse('provider-detail', kwargs={'pk': self.provider.pk}))
        serializer = ProviderSerializer(self.provider)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_provider(self):
        response = self.client.get(
            reverse('provider-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetSingleServiceAreaTest(APITestCase):
    """ Test GET single Service Area API """

    def setUp(self):
        self.service_area = baker.make(ServiceArea, name="Florida")

    def test_get_valid_single_service_area(self):
        response = self.client.get(
            reverse('servicearea-detail', kwargs={'pk': self.service_area.pk}))
        serializer = ServiceAreaSerializer(self.service_area)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_service_area(self):
        response = self.client.get(
            reverse('servicearea-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSingleProviderTest(APITestCase):
    """ Test updating an existing Provider record """

    def setUp(self):
        self.provider = baker.make(Provider)
        self.valid_payload = {
            "name": "Uber",
            "email": "example@example.com",
            "phone_number": "18338738237",
            "language": "English",
            "currency": "Dollar",
        }
        self.invalid_payload = {
            "name": "Uber",
            "phone_number": "18338738237",
            "language": "English",
            "currency": "Dollar",
        }

    def test_valid_update_provider(self):
        response = self.client.put(
            reverse('provider-detail', kwargs={'pk': self.provider.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_provider_missing_value(self):
        response = self.client.put(
            reverse('provider-detail', kwargs={'pk': self.provider.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_update_no_existing_provider(self):
        response = self.client.put(
            reverse('provider-detail', kwargs={'pk': 30}),
            data=json.dumps(self.valid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSingleServiceAreaTest(APITestCase):
    """ Test updating an existing Servicio Area record """

    def setUp(self):
        self.servicearea = baker.make(ServiceArea)
        provider = baker.make(Provider, name="Uber")
        geo_fl = open("./json/fl.json").read()
        self.valid_payload = {
            "name": "Florida",
            "price": 25.00,
            "area": geo_fl,
            "provider": provider.id,
        }
        self.invalid_payload = {
            "name": "Texas",
            "area": geo_fl,
            "provider": provider.id,
        }

    def test_valid_update_service_area(self):
        response = self.client.put(
            reverse('servicearea-detail', kwargs={'pk': self.servicearea.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_service_area_missing_value(self):
        response = self.client.put(
            reverse('servicearea-detail', kwargs={'pk': self.servicearea.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_update_no_existing_service_area(self):
        response = self.client.put(
            reverse('servicearea-detail', kwargs={'pk': 30}),
            data=json.dumps(self.valid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteSingleProviderTest(APITestCase):
    """ Test deleting an existing provider record """

    def setUp(self):
        self.provider = baker.make(Provider)

    def test_valid_delete_provider(self):
        response = self.client.delete(
            reverse('provider-detail', kwargs={'pk': self.provider.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_provider(self):
        response = self.client.delete(
            reverse('provider-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteSingleServiceAreaTest(APITestCase):
    """ Test deleting an existing service area record """

    def setUp(self):
        self.service_area = baker.make(ServiceArea)

    def test_valid_delete_service_area(self):
        response = self.client.delete(
            reverse('servicearea-detail', kwargs={'pk': self.service_area.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_service_area(self):
        response = self.client.delete(
            reverse('servicearea-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProvidersInTheAreaTest(APITestCase):
        """Test endpoint that takes a lat/lng pair and return a list of all polygons that include the given lat/lng"""

        def setUp(self):
            self.provider = baker.make(Provider, name="Uber")
            servicearea1 = baker.make(ServiceArea,
                                      name="Florida",
                                      area=open("./json/fl.json").read(),
                                      provider=self.provider)
            servicearea2 = baker.make(ServiceArea,
                                      name="Texas",
                                      area=open("./json/tx.json").read(),
                                      provider=self.provider)
            servicearea3 = baker.make(ServiceArea, name="US",
                                      area=open("./json/us.json").read(),
                                      provider=self.provider)

        def test_valid_request_single_provider_in_the_area(self):
            # NY lat:40.757880 long:-73.985580
            new_york = {"lat":40.757880, "long":-73.985580}
            response = self.client.get(
                reverse('servicearea-get-providers-in-the-area'), new_york,
                content_type='application/json'
            )
            location = Point(new_york["long"], new_york["lat"], srid=4326)
            providers_in_the_area = ServiceArea.objects.filter(area__contains=location)
            serialized = ResultsSerializer(providers_in_the_area, many=True)
            self.assertEqual(len(response.data), len(serialized.data))
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data, serialized.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            #print(response.data[1])

        def test_valid_request_multiple_providers_in_the_area(self):
            # Miami lat=25.763834 long=-80.205429
            miami = {"lat": 25.763834, "long": -80.205429}
            response = self.client.get(
                reverse('servicearea-get-providers-in-the-area'), miami,
                content_type='application/json'
            )
            location = Point(miami["long"], miami["lat"], srid=4326)
            providers_in_the_area = ServiceArea.objects.filter(area__contains=location)
            serialized = ResultsSerializer(providers_in_the_area, many=True)
            self.assertEqual(len(response.data), len(serialized.data))
            self.assertEqual(len(response.data), 2)
            self.assertEqual(response.data, serialized.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

