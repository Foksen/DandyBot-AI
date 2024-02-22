def create_matrix(N, x):
    field = [x] * N
    for i in range(N):
        field[i] = [x] * N
    return field

def print_matrix(field):
    for i in field:
        for j in i:
            print('%3d' %j, end=' ')
        print()

def set_walls(check, field, start_coords, game_coords):
    N = len(field)
    x, y = start_coords
    for i in range(N):
        for j in range(N):
            if check('wall', j - start_coords[0] + game_coords[0], i - start_coords[1] + game_coords[1]):
                field[i][j] = -2

def find_gold_coords(check, field, start_coords, game_coords):
    N = len(field)
    coords = [start_coords]
    field[start_coords[1]][start_coords[0]] = 0
    while (len(coords)):
        current_coords = coords[0]
        x, y = current_coords
        r = field[y][x]
        if check('gold', x - start_coords[0] + game_coords[0], y - start_coords[1] + game_coords[1]):
            return (x, y)
        for i in range(3):
            for j in range(3):
                check_y, check_x = y - 1 + i , x - 1 + j
                if 0 <= check_x < N and 0 <= check_y < N \
                    and abs(check_x - x) + abs(check_y - y) == 1 \
                    and field[check_y][check_x] == -1:
                        field[check_y][check_x] = r + 1
                        coords.append((check_x, check_y))
        coords = coords[1:]

def find_next_coords(field, gold_coords):
    N = len(field)
    x, y = gold_coords
    while (field[y][x] != 1):
        for i in range(3):
            for j in range(3):
                check_y, check_x = y - 1 + i , x - 1 + j
                if 0 <= check_x < N and 0 <= check_y < N \
                    and abs(check_x - x) + abs(check_y - y) == 1 \
                    and field[check_y][check_x] == field[y][x] - 1:
                        x, y = check_x, check_y
                        break
            else:
                continue
            break
    return (x, y)

def choose_dir(start_coords, next_coords):
    start_x, start_y = start_coords
    next_x, next_y = next_coords
    if next_x == start_x - 1:
        return 'left'
    if next_x == start_x + 1:
        return 'right'
    if next_y == start_y - 1:
        return 'up'
    if next_y == start_y + 1:
        return 'down'

def get_dir(check, x, y):
    N = 40
    start_coords = ((N - 1) // 2, (N - 1) // 2)
    game_coords = (x, y)
    field = create_matrix(N, -1)
    set_walls(check, field, start_coords, game_coords)
    gold_coords = find_gold_coords(check, field, start_coords, game_coords)
    if (gold_coords):
        next_coords = find_next_coords(field, gold_coords)
        return choose_dir(start_coords, next_coords)

def script(check, x, y):
    if check('gold', x, y):
        return 'take'
    dir = get_dir(check, x, y)
    if dir:
        return dir
    return 'pass'