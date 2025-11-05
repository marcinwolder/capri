import pytest

from src.data_model.place.place import Place


def test_init_with_full_data():
    data = {
        'name': 'Example Place',
        'id': '123',
        'formattedAddress': '123 Example Street',
        'googleMapsUri': 'http://example.com',
        'websiteUri': 'http://example.com',
        'iconMaskBaseUri': 'http://example.com',
        'displayName': 'Example Place',
        'businessStatus': 'OPERATIONAL',
        'primaryType': 'restaurant',
        'location': {'latitude': 12.34, 'longitude': 56.78},
        
    }
    place = Place(data)
    assert place.name == 'Example Place'
    assert place.id == '123'
    


def test_init_with_partial_data():
    place = Place()
    place.placeInfo.name = 'Example Place'
    place.placeInfo.id = '123'
    place.placeInfo.formattedAddress = ''
    place.location.latitude = 12.34
    place.location.longitude = 56.78

    assert place.placeInfo.name == 'Example Place'
    assert place.placeInfo.id == '123'
    assert place.placeInfo.formattedAddress == ''
    


def test_init_with_no_data():
    place = Place({})
    assert place.name == ''
    assert place.id == ''
    


def test_missing_fields():
    data = {
        
        'name': 'Example Place',
        'id': '123',
        'location': {'latitude': 12.34, 'longitude': 56.78},
    }
    place = Place(data)
    assert place.location is not None  
    


def test_invalid_data_types():
    data = {
        'name': 123,  
        'id': '123',
        'location': {'latitude': 12.34, 'longitude': 56.78},
    }
    place = Place(data)
    assert place.name == ''
    


if __name__ == '__main__':
    pytest.main()
