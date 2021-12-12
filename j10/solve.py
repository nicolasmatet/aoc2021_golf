def lines():
    for l in open("input.txt"):
        yield l.strip()


class SpellChecker:
    syntax = {
        "(": ")",
        "{": "}",
        "[": "]",
        "<": ">"
    }

    corrupted_score = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }

    incomplete_score = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }

    def spell_check(self, line):
        expected = []
        for c in line:
            if c in self.syntax.keys():
                expected.append(self.syntax.get(c))
                continue
            if not expected:
                return 'too long', 0
            if not c == expected[-1]:
                return 'corrupted', self.corrupted_score.get(c, 0)
            expected.pop()
        if len(expected):
            return 'incomplete', self._score_incomplete(expected)
        return 'ok', 0

    def _score_incomplete(self, missings):
        total_score = 0
        for c in missings[::-1]:
            total_score = 5 * total_score + self.incomplete_score[c]
        return total_score


def solve():
    spell_checker = SpellChecker()
    corrupted_score = 0
    incomplete_scores = []
    for line in lines():
        state, score = spell_checker.spell_check(line)
        if state == 'corrupted':
            corrupted_score += score
        if state == 'incomplete':
            incomplete_scores.append(score)
    return corrupted_score, sorted(incomplete_scores)[len(incomplete_scores) // 2]


print(solve())
