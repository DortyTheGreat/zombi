import requests
import json
import time
import random

TOKEN = '66912b6a10f7166912b6a10f75'
BASE_URL = 'https://games-test.datsteam.dev'


def request(method, endpoint, body=None):
    if body is None:
        body = {}
    url = BASE_URL + endpoint
    headers = {
        'X-Auth-Token': TOKEN
    }
    r = requests.request(method, url, json=body, headers=headers)
    if r.status_code != 200:
        data = json.dumps(r.json(), indent=2)
        raise Exception('Got %d status code from server, server returned\n %s' % (r.status_code, data))
    return r.json()


def participate():
    return request('put', '/play/zombidef/participate')


def command(body):
    return request('post', '/play/zombidef/command', body)

def units():
    #return json.loads(open('1720805915.2333837.txt', 'r').read())
    return request('get', '/play/zombidef/units')


def world():
    return request('get', '/play/zombidef/world')


def rounds():
    return request('get', '/rounds/zombidef')


def pprint(d):
    json_formatted_str = json.dumps(d, indent=2)
    print(json_formatted_str)


def get_zombies(data):
    zombies = data.get('zombies')
    if zombies is None:
        return []
    return zombies


def get_base(data):
    base = data.get('base')
    if base is None:
        return []
    return base


def get_enemy_blocks(data):
    enemy_blocks = data.get('enemyBlocks')
    if enemy_blocks is None:
        return []
    return enemy_blocks


def get_attack(data):
    res = []
    base = get_base(data)
    zombies = get_zombies(data)

    zombies.sort(key=lambda zombie: zombie.get('health'))
    enemy_blocks = get_enemy_blocks(data)


    for tower in base:
        for zombie in zombies:
            tx = tower.get('x')
            ty = tower.get('y')
            r = tower.get('range')
            id = tower.get('id')

            zx = zombie.get('x')
            zy = zombie.get('y')
            if r ** 2 >= (tx - zx) ** 2 + (ty - zy) ** 2:
                res.append({
                    'blockId': id,
                    'target': {
                        'x': zx,
                        'y': zy,
                    }
                })
                break
        for enemy_block in enemy_blocks:
            tx = tower.get('x')
            ty = tower.get('y')
            r = tower.get('range')
            id = tower.get('id')

            bx = enemy_block.get('x')
            by = enemy_block.get('y')
            if r ** 2 >= (tx - bx) ** 2 + (ty - by) ** 2:
                res.append({
                    'blockId': id,
                    'target': {
                        'x': bx,
                        'y': by,
                    }
                })
                break

    return res


def get_build(data):
    availab_spots = set()
    base = get_base(data)

    for tower in base:
        availab_spots.add((tower['x'], tower['y'] + 1))
        availab_spots.add((tower['x'], tower['y'] - 1))
        availab_spots.add((tower['x'] - 1, tower['y']))
        availab_spots.add((tower['x'] + 1, tower['y']))

    for tower in base:
        elem = (tower['x'], tower['y'])
        if elem in availab_spots:
            availab_spots.remove((tower['x'], tower['y']))

    build_com = []

    for i in range(data['player']['gold'] * 2):
        if not availab_spots:
            break
        elem = random.choice(tuple(availab_spots))
        if elem in availab_spots:
            availab_spots.remove(elem)
        build_com.append({'x': elem[0], 'y': elem[1]})

    return build_com


def get_move_base(data):
    base = get_base(data)
    for tower in base:
        if 'isHead' in tower:
            return {
                'x': tower.get('x'),
                'y': tower.get('y')
            }


def get_command():
    data = units()

    build = get_build(data)
    attack = get_attack(data)
    move_base = get_move_base(data)

    r = command(
        {
            'attack': attack,
            'build': build,
            'moveBase': move_base
        }
    )
    pprint(r)


def visual():
    while True:
        data = units()

        myFile = open(f'{time.time()}.txt', 'w')

        myFile.write(str(data))
        myFile.close()

        # Fill the background with white
        screen.fill((255, 255, 255))

        base = get_base(data)
        zombies = get_zombies(data)
        enemy_blocks = get_enemy_blocks(data)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        x_d = 500
        y_d = 500


        print(type(base))
        if (type(base)):
            for tower in base:
                # Draw a solid blue circle in the center
                pygame.draw.circle(screen, (0, 0, 255),(x_d + tower.get('x'), y_d + tower.get('y')), 1)

        if (type(zombies) != None):
            for zombie in zombies:
                # Draw a solid blue circle in the center
                pygame.draw.circle(screen, (0, 255, 0), (x_d + zombie.get('x'), y_d + zombie.get('y')), 1)


        if (type(enemy_blocks) != None):
            for enemy_block in enemy_blocks:
                # Draw a solid blue circle in the center
                pygame.draw.circle(screen, (255, 0, 0), (x_d + enemy_block.get('x'),y_d + enemy_block.get('y')), 1)

        # Flip the display
        pygame.display.flip()

        time.sleep(1)





while True:
    get_command()
    time.sleep(1.5)

