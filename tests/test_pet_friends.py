import os
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    # Проверяем на статус 200 и получения ключа-key в ответе
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    # Проверка на то, что общий список не пустой
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet():
    # Проверка на создание нового питомца с верными данными
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_name = 'Zora'
    animal_type = 'Dog'
    pet_age = '14'
    pet_photo_path = r'C:\Users\tiama\PycharmProjects\test_project_skill\PetFriends3\tests\images\wwe.png'
    status, result = pf.add_new_pet(auth_key['key'], pet_name, animal_type, pet_age, pet_photo_path)
    assert status == 200
    assert result['name'] == pet_name

def test_get_my_pets_with_valid_key(filter="my_pets"):
    # Проверяем, что список созданных нами питомцев не пустой
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_list = pf.get_list_of_pets(auth_key, "my_pets")
    if len(pet_list['pets']) == 0:
        # Если  нет питомцев, добавляем нового для теста
        pf.add_new_pet(auth_key['key'], "Vasy", "Kot", "77", r'C:\Users\tiama\PycharmProjects\test_project_skill\Petfriends3\tests\images\wwe.png')
        _, pet_list = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = pet_list['pets'][0]['id']
    status = pf.delete_pet(auth_key['key'], pet_id)
    _, pet_list_updated = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    # Проверяем, что удалённого питомца нет в списке
    assert pet_id not in [pet['id'] for pet in pet_list_updated['pets']]

def test_update_pet_info():
    # Проверяем возможность внести изменения о питомце
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_list = pf.get_list_of_pets(auth_key, 'my_pets')
    # Если список питомцев пуст, добавляем нового питомца
    if len(pet_list['pets']) == 0:
        pet_name = 'Viski'
        pet_type = 'Volk'
        pet_age = '2'

        _, pet = pf.add_new_pet_no_photo(auth_key['key'], pet_name, pet_type, pet_age)
        pet_id = pet['id']
    else:
        pet_id = pet_list['pets'][0]['id']
    # Новые данные для обновления информации о питомце
    new_name = 'Fedot'
    new_animal_type = 'Sosiska'
    new_age = '56'
    status, result = pf.update_pet_info(auth_key['key'], pet_id, new_name, new_animal_type, new_age)

    assert status == 200
    assert result['name'] == new_name
    assert result['animal_type'] == new_animal_type
    assert result['age'] == new_age

def test_add_new_pet_no_photo():
    # Проверяем возможность добавить питомца без фотографии
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_name = 'Grib'
    animal_type = 'Los'
    pet_age = '15'
    status, result = pf.add_new_pet_no_photo(auth_key['key'], pet_name, animal_type, pet_age)
    assert status == 200
    assert result['name'] == pet_name
    assert result['animal_type'] == animal_type
    assert result['age'] == pet_age

def test_successful_add_photo(pet_photo = r'C:\Users\tiama\PycharmProjects\test_project_skill\PetFriends3\tests\images\wwe.png'):
    # Проверяем возможность добавить фото в карточку питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Grib', 'Los', 15)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo(auth_key, pet_id, pet_photo)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert 'photo' in result or 'pet_photo' in result

def test_get_api_key_for_invalid_email(email="wrongemail@example.com", password="correctpassword"):
    # Получение API-ключа с неправильным адресом электронной почты
    status, result = pf.get_api_key(email, password)
    assert status == 403 or status == 401
    assert 'key' not in result

def test_get_api_key_for_invalid_password(email="correctemail@example.com", password="wrongpassword"):
    # Получение API-ключа с неправильным паролем
    status, result = pf.get_api_key(email, password)
    assert status == 403 or status == 401
    assert 'key' not in result

def test_negative_create_pet_simple_wrong_age(name='Жлоб', animal_type='Жаба', age=-88):
    # Проверяем возможность создания питомца с отрицательным возрастом
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_photo(auth_key['key'], name, animal_type, age)
    assert status == 400

def test_create_pet_with_age_as_string(name='Чили', animal_type='Филин', age='пять'):
    # Проверяем возможность создания питомца с возрастом в формате строки
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_photo(auth_key['key'], name, animal_type, age)
    assert status == 400

def test_create_pet_with_missing_fields(name = '', animal_type= '', age = ''):
    # Проверяем возможность создания питомца без заполнения обязательных полей
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_photo(auth_key['key'], name, animal_type, age)
    assert status == 400


def test_update_pet_animal_type_to_empty():
    # Проверяем возможность обновить тип питомца на пустое значение
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем список моих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Берем первого питомца из списка
    pet_id = my_pets['pets'][0]['id']
    # Пытаемся обновить тип животного на пустую строку
    status, result = pf.update_pet_info(auth_key['key'], pet_id, name='Жорик', animal_type='', age = 17)
    assert status == 400

def test_negative_update_pet_info_too_large(name='Meow', animal_type='cat'*100, age=1):
    # Проверяем возможность обновить данные своего питомца на данные с большим значением
    _, auth_key_response = pf.get_api_key(valid_email, valid_password)
    assert 'key' in auth_key_response
    auth_key = auth_key_response

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key['key'], "Муська", "котяра", 7)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.update_pet_info(auth_key['key'], pet_id, name, animal_type, age)
    assert status == 400

def test_create_pet_with_very_large_name_no_photo():
    # Проверяем возможность создать питомца с большим\длинным именем

    _, auth_key_response = pf.get_api_key(valid_email, valid_password)
    assert 'key' in auth_key_response
    auth_key = auth_key_response['key']

    very_large_name = 'Fil' * 100
    animal_type = 'slon'
    age = '8'
    status, result = pf.add_new_pet_no_photo(auth_key, very_large_name, animal_type, age)
    assert status == 400


















