
# part A
# ======


initial_xy = {'x': 0, 'y': 0}
target_area_xs = [282, 314]
target_area_ys = [-45, -80]
velocity_x_max_min = [0, max(target_area_xs) + 1]
velocity_y_max_min = [min(target_area_ys) - 1, 100]
number_of_steps = 1000


def is_in_target_area(probe_coordinates):
    if (min(target_area_xs) <= probe_coordinates['x'] <= max(target_area_xs)) and (min(target_area_ys) <= probe_coordinates['y'] <= max(target_area_ys)):
        return True
    return False

def update_velocity_x(velo_x):
    drag = lambda x: (x - 1) if x > 0 else ((x + 1) if x < 0 else x)
    return drag(velo_x)

def update_velocity_y(velo_y):
    return velo_y - 1

def get_best_x_velocity(initial_velocity_x):
    sum_of_velo_x = 0
    current_velocity_x = initial_velocity_x
    shortlisted_velocities_x = []
    while current_velocity_x > 0:
        shortlisted_velocity  = {}
        sum_of_velo_x += current_velocity_x
        if target_area_xs[0] <= sum_of_velo_x <= target_area_xs[-1]:
            shortlisted_velocity['initial_velocity'] = initial_velocity_x
            shortlisted_velocity['last velocity'] = current_velocity_x
            shortlisted_velocity['steps'] = initial_velocity_x - current_velocity_x + 1
            shortlisted_velocity['sum_of_x_velocities'] = sum_of_velo_x
            shortlisted_velocities_x.append(shortlisted_velocity)
        if sum_of_velo_x > target_area_xs[-1]:
            return shortlisted_velocities_x
        new_velocity_x = update_velocity_x(current_velocity_x)
        current_velocity_x = new_velocity_x
    return shortlisted_velocities_x

def repeat():
    velocities_x = []
    for _ in reversed(range(target_area_xs[-1])):
        velocities_x += get_best_x_velocity(_)
    return velocities_x
best_velocity_x = [repeat()[-1]][0]['initial_velocity']


def one_step(initial_position, velocity_x, velocity_y):
    velocity_copy = {'x': velocity_x, 'y': velocity_y}
    trajectories = {tuple(velocity_copy.values()): []}
    velocity = {'x': velocity_x, 'y': velocity_y}
    for i in range(number_of_steps):
        new_coordinates = {'x': initial_position['x'] + velocity['x'], 'y': initial_position['y'] + velocity['y']}
        trajectories[tuple(velocity_copy.values())].append(new_coordinates)
        if is_in_target_area(initial_position) == True:
            return trajectories
        initial_position = new_coordinates
        velocity_x = update_velocity_x(velocity['x'])
        velocity_y = update_velocity_y(velocity['y'])
        velocity = {'x': velocity_x, 'y': velocity_y}
    return None

def pick_all_viable_velocities(initial_xy, best_x_velocity, y_velocities):
    velocities_shortlist = []
    for y in y_velocities:
        viable_velocity_dict = one_step(initial_xy, best_x_velocity, y)
        if viable_velocity_dict != None:
            velocities_shortlist.append(viable_velocity_dict)
    return velocities_shortlist
shortlisted_velocities = pick_all_viable_velocities(initial_xy, best_velocity_x, range(min(velocity_y_max_min), max(velocity_y_max_min)))

def pick_highest(shortlisted):
    heights = set()
    for d in shortlisted:
        trajectory = list(d.values())
        trajectory = trajectory[0]
        trajectory = [item.get('y') for item in trajectory]
        heights.add(max(trajectory))
    highest = max(heights)
    return highest
print(pick_highest(shortlisted_velocities))


# part B
# ======

initial_xy = {'x': 0, 'y': 0}
target_area_xs = [282, 314]
target_area_ys = [-45, -80]

# some values to try out:
velocity_x_max_min = [0, max(target_area_xs) + 1]
velocity_y_max_min = [min(target_area_ys) - 1, 100]
number_of_steps = 1000

def is_in_target_area(probe_coordinates):
    if (min(target_area_xs) <= probe_coordinates['x'] <= max(target_area_xs)) and (min(target_area_ys) <= probe_coordinates['y'] <= max(target_area_ys)):
        return True
    return False

def update_velocity_x(velo_x):
    drag = lambda x: (x - 1) if x > 0 else ((x + 1) if x < 0 else x)
    return drag(velo_x)

def update_velocity_y(velo_y):
    return velo_y - 1

def get_best_x_velocity(initial_velocity_x):
    sum_of_velo_x = 0
    current_velocity_x = initial_velocity_x
    shortlisted_velocities_x = []
    while current_velocity_x > 0:
        shortlisted_velocity  = {}
        sum_of_velo_x += current_velocity_x
        if target_area_xs[0] <= sum_of_velo_x <= target_area_xs[-1]:
            shortlisted_velocity['initial_velocity'] = initial_velocity_x
            shortlisted_velocity['last velocity'] = current_velocity_x
            shortlisted_velocity['steps'] = initial_velocity_x - current_velocity_x + 1
            shortlisted_velocity['sum_of_x_velocities'] = sum_of_velo_x
            shortlisted_velocities_x.append(shortlisted_velocity)
        if sum_of_velo_x > target_area_xs[-1]:
            return shortlisted_velocities_x
        new_velocity_x = update_velocity_x(current_velocity_x)
        current_velocity_x = new_velocity_x
    return shortlisted_velocities_x

def repeat():
    velocities_x = []
    for _ in reversed(range(target_area_xs[-1] + 1)):
        velocities_x += get_best_x_velocity(_)
    velocities_x = [item['initial_velocity'] for item in velocities_x]
    velocities_x = set(velocities_x)
    return velocities_x
all_x_velocities = repeat()

def one_step(initial_position, velocity_x, velocity_y):
    velocity_copy = {'x': velocity_x, 'y': velocity_y}
    trajectories = {tuple(velocity_copy.values()): 0}
    velocity = {'x': velocity_x, 'y': velocity_y}
    for i in range(number_of_steps):
        new_coordinates = {'x': initial_position['x'] + velocity['x'], 'y': initial_position['y'] + velocity['y']}
        trajectories[tuple(velocity_copy.values())] += 1
        if is_in_target_area(initial_position) == True:
            return trajectories
        initial_position = new_coordinates
        velocity_x = update_velocity_x(velocity['x'])
        velocity_y = update_velocity_y(velocity['y'])
        velocity = {'x': velocity_x, 'y': velocity_y}
    return None


def pick_all_viable_velocities(initial_xy, x_velocities, y_velocities):
    velocities_shortlist = []
    for x in x_velocities:
        for y in y_velocities:
            viable_velocity_dict = one_step(initial_xy, x, y)
            if viable_velocity_dict != None:
                velocities_shortlist.append(viable_velocity_dict)
    return velocities_shortlist
shortlisted_velocities = pick_all_viable_velocities(initial_xy, all_x_velocities, range(min(velocity_y_max_min), max(velocity_y_max_min)))

all = set()
for d in shortlisted_velocities:
    for key in d.keys():
        all.add(key)
print(len(all))












