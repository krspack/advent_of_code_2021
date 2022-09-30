
with open('10_input.txt') as txt:
    lines = [line.strip() for line in txt]
    lines[0] = lines[0][1:]
    if len(lines[-1]) == 0:
        lines = lines[:-1]

class Character:
    def __init__(self, value):
        self.value = value
        self.opening = True
        self.opened_couple = True
        self.ind = None

    def reset_status(self):
        if self.value in ['(', '[', '{', '<']:
            self.opening = True
        else:
            self.opening = False
        if self.opening == False:
            assert self.value in [")", "]", "}", ">"]

    def get_type(self):
        if self.value in ['(', ')']:
            self.type = 'a'
        if self.value in ['[', ']']:
            self.type = 'b'
        if self.value in ['{', '}']:
            self.type = 'c'
        if self.value in ['<', '>']:
            self.type = 'd'
        return self.type

    def get_points(self):
        self.get_type()
        if self.type == 'a':
            self.points = 3
        if self.type == 'b':
            self.points = 57
        if self.type == 'c':
            self.points = 1197
        if self.type == 'd':
            self.points = 25137
        return self.points

    def find_mistake(self, list_of_Characters):
        opened_types = []
        # part a: finding faulted characters
        for character in list_of_Characters:
            character.reset_status()
            if character.opening == True and character.opened_couple == True:
                opened_types.append(character.get_type())
            if character.opening == False:
                current_char_type = character.get_type()
                if opened_types[-1] == current_char_type:
                    del opened_types[-1]
                else:
                    return character.get_points(), 0
        # part b: completing incomplete lines
        opened_types.reverse()
        d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        opened_types = [d.get(item) for item in opened_types]
        def completion_score(lst = opened_types):
            result = 0
            for i in range(len(lst)):
                result = result*5 + lst[i]
            return result
        return 0, completion_score()


def count_scores(input_lines):
    syntax_error_score = 0
    completion_scores = []
    for line in input_lines:
        line = [Character(x) for x in line]
        both_scores = line[0].find_mistake(line)
        syntax_error_score += both_scores[0]
        completion_scores.append(both_scores[1])
    completion_scores = sorted([x for x in completion_scores if x != 0])
    completion_score = completion_scores[round((len(completion_scores)-1) / 2)]
    return syntax_error_score, completion_score
print(count_scores(lines))










