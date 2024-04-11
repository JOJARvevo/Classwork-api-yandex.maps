import pygame
import requests

api_key = '40d1649f-0493-4b70-98ba-98533de7710b'
MAP_TYPE = 'map'

def change_zoom(coords, zoom, k):
    zoom += k
    if zoom == -1:
        zoom = 0
    if zoom == 22:
        zoom = 21
    response = get_image(coords, zoom)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file, zoom


def change_dir(coords, zoom, direction, k, w, h):
    print(coords)
    if not direction:
        x = str(float(coords[0]) + float(coords[0]) / zoom * k)
        coords = (x, coords[1])
    else:
        y = str(float(coords[1]) + float(coords[1]) / zoom * k)
        coords = (coords[0], y)
    print(coords)
    response = get_image(coords, zoom)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file, zoom, coords


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


def get_image(zoom, geocords):
    map_request = "http://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": ",".join([str(el) for el in geocords]),
        "l": MAP_TYPE,
        "z": str(zoom)
    }
    map_file = "map.png"
    response = requests.get(map_request, params=map_params)
    with open("map.png", "wb") as file:
        file.write(response.content)
    return map_file


if __name__ == '__main__':
    map_types = {"map": "sat", "sat": "skl", "skl": "map"}
    offset_multipliyer = 2 ** 12
    OFFSET_COORD = 4096 / 100
    prev_coords = (0, 0)
    coords = tuple(map(float, input("Введите ширину и долготу объекта ").split()))
    ZOOM = int(input("Укажите приближение от 0 до 21 "))
    response = get_image(ZOOM, coords)
    # w, h = input('Введите длину онак '), input('Введите ширину окна ')
    print(coords, ZOOM)
    delta_loc = (2.196 ** ZOOM) * 0.038
    map_file = "map.png"
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(get_image(ZOOM, coords)), (0, 0))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                print(ZOOM)
                if event.key == pygame.K_e:
                    MAP_TYPE = map_types[MAP_TYPE]
                if event.key == 1073741906:
                    ZOOM -= 1
                    offset_multipliyer /= 2
                    offset_multipliyer = max(min(2 ** 21, offset_multipliyer), 1)
                    ZOOM = max(min(21, ZOOM), 0)
                if event.key == 1073741905:
                    ZOOM += 1
                    offset_multipliyer *= 2
                    offset_multipliyer = max(min(2 ** 21, offset_multipliyer), 1)
                    ZOOM = max(min(21, ZOOM), 0)
                if event.key == pygame.K_w:
                    x, y = coords
                    coords = x, max(min(89, y + delta_loc), -89)
                if event.key == pygame.K_s:
                    x, y = coords
                    coords = x, max(min(89, y - delta_loc), -89)
                if event.key == pygame.K_d:
                    x, y = coords
                    coords = max(min(84, x + delta_loc), -84), y
                if event.key == pygame.K_a:
                    x, y = coords
                    coords = max(min(84, x - delta_loc), -84), y
                map_file = get_image(ZOOM, coords)
                delta_loc = ((0.03 ** (1 / 7)) ** ZOOM) * 16
                print(coords)
                screen.blit(pygame.image.load(map_file), (0, 0))

        pygame.display.flip()

    pygame.quit()
# ло
