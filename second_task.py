import pygame
import requests

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


def get_image(geocords, zoom):
    map_request = "http://static-maps.yandex.ru/1.x/"

    map_params = {
        "ll": ",".join([str(el) for el in geocords]),
        "l": "map",
        "z": str(zoom)
    }

    response = requests.get(map_request, params=map_params)
    return response


if __name__ == '__main__':
    coords = tuple(input("Введите ширину и долготу объекта ").split())
    zoom = input("Укажите приближение от 0 до 21 ")
    response = get_image(coords, zoom)
    print(coords, zoom)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEDOWN:
                    zoom = str(int(zoom) - 1)
                    if zoom == "-1":
                        zoom = "0"
                    response = get_image(coords, zoom)
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response.content)
                    screen.blit(pygame.image.load(map_file), (0, 0))
                elif event.key == pygame.K_PAGEUP:
                    zoom = str(int(zoom) + 1)
                    if zoom == "22":
                        zoom = "21"
                    response = get_image(coords, zoom)
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response.content)
                    screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()

    pygame.quit()
