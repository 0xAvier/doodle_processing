class Group:

  def __init__(self, players, hosts):
    self.players = players 
    self.hosts = hosts


  def find(self, name):
    try:
      player = next(filter(lambda p: p.name.lower() == name.lower(), self.players))
      return player
    except:
      names = ', '.join(self.names())
      print("Player {} not found in player list {}".format(name, names))
      raise


  def names(self):
    return [p.name for p in self.players]


  def __str__(self):
    return "\n".join(map(str, self.players))


