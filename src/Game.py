class Game:

  def __init__(self, name, ranges):
    self.name = name
    self.nplayers_str = ranges
    self.nplayers = []
    self._parse_nplayer_range(ranges)

  def _parse_nplayer_range(self, string):
      ranges = string.split(',')
      for r in ranges:
        subr = r.split('-')
        if len(subr) == 1:
          self.nplayers.append(int(subr[0]))
        elif len(subr) == 2:
          self.nplayers += range(int(subr[0]), int(subr[1]) + 1)
        else:
          raise Exception("A range should be either 'a' or 'a-b', chained by ','. {} is incorrect".format(string))


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


  def __str__(self):
    return "{}: ({}p)".format(self.name, "/".join(self.nplayers))


  def __repr__(self):
    return "{}: ({}p)".format(self.name, "/".join(map(str, self.nplayers)))


