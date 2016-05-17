class Agreement:
    def __init__(self, particles, corrections):
        self.cases = []
        for part in particles:
            self.cases.append((particles[part], corrections[part]))


    def part_agreement(self, previous_syl, particle):
        """
        proposes the right particle according to the previous syllable.
            In case of an invalid previous syllable, returns the particle preceded by *
            limitation : particle needs to be a separate syllabes. (the problems with wrong merged agreement will be flagged by get_mingzhi )
            input : previous syllable, particle
        :param previous: preceding syllable
        :param particle: particle at hand
        :return: the correct agreement for the preceding syllable
        """
        previous = self.get_info(previous_syl)
        final = ''
        if previous == 'dadrag':
            final = 'ད་དྲག'
        elif previous == 'thame':
            final = 'མཐའ་མེད'
        else:
            final = previous[-1]
            if final not in ['ག', 'ང', 'ད', 'ན', 'བ', 'མ', 'འ', 'ར', 'ལ', 'ས']:
                final = None

        if final:
            # added the ད་དྲག་ for all and the མཐའ་མེད་ for all in provision of all cases
            # where an extra syllable is needed in verses
            # dadrag added according to Élie’s rules.

            correction = ''
            for case in cases:
                if particle in case[0]:
                    correction = case[1][final]
            return correction
        else:
            return '*' + particle


def main():
    print(Agreement().part_agreement('ཤིག', 'ཀྱི'))

if __name__ == "__main__":
    main()