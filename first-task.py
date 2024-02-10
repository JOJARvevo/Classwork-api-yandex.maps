import requests
import pygame

api_key = '40d1649f-0493-4b70-98ba-98533de7710b'


def geocode(adress):
    geocoder_request = f'http://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={adress}&format=json'

    response = requests.get(geocoder_request)
    if response:
        json_req = response.json()
    else:
        raise EOFError

    freatures = json_req['response']['GeoObjectCollection']['featureMember']
    return freatures[0]['GeoObject'] if freatures else None


def get_adress_coords(address):
    toponym = geocode(address)

    # toponym_adress = toponym['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
    toponym_coords = toponym['Point']['pos']
    print(toponym_coords)

    return toponym_coords


def get_image(geocords):
    zoom = input("Укажите приближение от 1 до 30")
    image_req = f'http://static-maps.yandex.ru/1.x/?ll={geocords[0]},{geocords[1]}&spn={zoom},{zoom}&l=map'
    image = requests.get(image_req)
    return image


if __name__ == '__main__':
    response = get_image(tuple(input("Введите ширину и долготу объекта ").split()))
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
