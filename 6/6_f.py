
import collections

with open('day_6_input.txt') as text:
    timers = text.read()


timers = timers.split(",")
timers[-1] = timers[-1].replace('\n', '')
timers = [int(i) for i in timers]


def count_fish(timers_input, number_of_days):
    frequencies = dict(collections.Counter(timers_input))
    overview = []
    for k, v in frequencies.items():
        overview.append({'current_timer': k, 'frequency': v})
    overview.append({'current_timer': 0, 'frequency': 0})
    overview.append({'current_timer': 8, 'frequency': 0})
    overview.append({'current_timer': 7, 'frequency': 0})
    overview.append({'current_timer': 6, 'frequency': 0})

    fish_sum = 0
    for fish_group in overview:
        fish_sum += fish_group['frequency']     # number of fish at the beginning. To be updated later with every new generation.

    for i in range(number_of_days):
        overview_updated = []
        fish_daily_surplus = 0
        for fish_group in overview:
            if (fish_group['current_timer'] > 0 and fish_group['current_timer'] != 7):
                fish_group_updated = {'current_timer': fish_group['current_timer'] - 1, 'frequency': fish_group['frequency']}
                overview_updated.append(fish_group_updated)
            if (fish_group['current_timer'] == 0 or fish_group['current_timer'] == 7):
                fish_daily_surplus += fish_group['frequency']
            if fish_group['current_timer'] == 0:
                fish_group_born_today = {'current_timer': 8, 'frequency': fish_group['frequency']}
                overview_updated.append(fish_group_born_today)
                fish_sum += fish_group['frequency']
        overview_updated.append({'current_timer': 6, 'frequency': fish_daily_surplus})  # since 6 stems both from 7 and 0, it has to be treated separately
        overview = overview_updated
    return fish_sum
print(count_fish(timers, 256))