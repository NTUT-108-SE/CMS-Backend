from app.modules.domain.management import Management
from app.modules.database import ManagementModel


def test_unit(db):
    management = Management()
    assert management.title == "Default_title"
    assert management.description == "Default_description"

    data = {"title": "title", "description": "description"}

    management.update(data)
    assert management.title == "title"
    assert management.description == "description"
    assert management.time == "19:00"
    assert management.URLs == [
        "https://google.com", "https://google.com", "https://google.com", "https://google.com"
    ]
    assert management.images == [
        "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg",
        "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg",
        "https://cdn.vuetifyjs.com/images/carousel/bird.jpg",
        "https://cdn.vuetifyjs.com/images/carousel/planet.jpg"
    ]
    assert management.doctor_description == "Default_doctor_description"
    assert management.clinic_address == "Default_clinic_address"

    assert management._management == management.get()
