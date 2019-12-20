import graphene
from bson.objectid import ObjectId
from ..database import ManagementModel
from graphene_mongo import MongoengineObjectType
from mongoengine import DoesNotExist


class Management:
    def __init__(self):
        try:
            self._management = ManagementModel.objects.all()[0]
        except Exception:
            self._management = ManagementModel(
                images=[
                    "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg",
                    "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg",
                    "https://cdn.vuetifyjs.com/images/carousel/bird.jpg",
                    "https://cdn.vuetifyjs.com/images/carousel/planet.jpg"
                ],
                URLs=[
                    "https://google.com", "https://google.com", "https://google.com",
                    "https://google.com"
                ],
                title="Default_title",
                time="19:00",
                description="Default_description",
                our_services="Default_our_services",
                doctor_description="Default_doctor_description",
                clinic_address="Default_clinic_address"
            )
            self.save()

    def save(self):
        self._management.save()
        self._management.reload()

    def get(self):
        return self._management

    def set_time(self, new_time):
        self._management['time'] = new_time
        self.save()

    def update(self, management):
        self._management.update(**management)
        self.save()

    @property
    def id(self):
        return self._management['id']

    @property
    def images(self):
        return self._management['images']

    @images.setter
    def images(self, new_images):
        self._management['images'] = new_images

    @property
    def URLs(self):
        return self._management['URLs']

    @URLs.setter
    def URLs(self, new_URLs):
        self._management['URLs'] = new_URLs

    @property
    def title(self):
        return self._management['title']

    @title.setter
    def title(self, new_title):
        self._management['title'] = new_title

    @property
    def time(self):
        return self._management['time']

    @time.setter
    def time(self, new_time):
        self._management['time'] = new_time

    @property
    def description(self):
        return self._management['description']

    @description.setter
    def description(self, new_discription):
        self._management['description'] = new_discription

    @property
    def our_services(self):
        return self._management['our_services']

    @our_services.setter
    def our_services(self, new_our_services):
        self._management['our_services'] = new_our_services

    @property
    def doctor_description(self):
        return self._management['doctor_description']

    @doctor_description.setter
    def doctor_description(self, new_doctor_description):
        self._management['doctor_description'] = new_doctor_description

    @property
    def clinic_address(self):
        return self._management['clinic_address']

    @clinic_address.setter
    def clinic_address(self, new_clinic_address):
        self._management['clinic_address'] = new_clinic_address
