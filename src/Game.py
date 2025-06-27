class Game:

    def __init__(self, name, ranges):
        self.name = name
        self.nplayers_str = ranges
        self.nplayers = []
        self._parse_nplayer_range(ranges)
        self.early_start = False
        self.owner_name = None

    def add_option(self, option):
        if option == "early":
            self.early_start = True
        elif option.startswith("owner="):
            self.owner_name = option[len("owner="):]
        else:
            raise Exception(f"Option {option} for game unknown")

    def _parse_nplayer_range(self, string):
        ranges = string.split(',')
        for r in ranges:
            subr = r.split('-')
            if len(subr) == 1:
                self.nplayers.append(int(subr[0]))
            elif len(subr) == 2:
                self.nplayers += range(int(subr[0]), int(subr[1]) + 1)
            else:
                raise Exception(
                    "A range should be either 'a' or 'a-b', chained by ','. {} is incorrect".format(string))

    def nplayer_min(self):
        return self.nplayers[0]

    def nplayer_max(self):
        return self.nplayers[-1]

    def nplayer_smallest_max(self, val):
        res = self.nplayers[0]
        for i in range(1, len(self.nplayers)):
            if self.nplayers[i] > val:
                break
        return res

    def nplayer_str(self, nplayer):
        if nplayer in self.nplayers:
            return "{}p".format(nplayer)
        elif self.nplayer_max() < nplayer:
            return "{}/{}p".format(self.nplayer_max(), nplayer)
        elif nplayer not in self.nplayers:
            return "{}/{}p".format(self.nplayer_smallest_max(nplayer), nplayer)
        else:
            raise Exception("Full game error")

    def __str__(self):
        return "{}: ({}p)".format(self.name, "/".join(str(self.nplayers)))

    def __repr__(self):
        return "{}: ({}p)".format(self.name, "/".join(map(str, self.nplayers)))
