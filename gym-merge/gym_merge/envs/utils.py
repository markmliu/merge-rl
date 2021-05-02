import random as ra

def getStartingS():
  #return -100.0
  return ra.uniform(-150.0, -50.0)

def getStartingV():
  # return 20.0
  return ra.uniform(10.0,30.0)

class Actor():
  def __init__(self):
    self.s = getStartingS()
    self.v = getStartingV()

  def step(self, accel, dt):
    self.s += (self.v * dt)
    self.v += (accel * dt)


# takes two actors travel as cost
def collision(s1, s2):
  # lets say both cars are about 4m long.
  CAR_LENGTH = 4.0

  # collision checking only begins at critical point (0 travel)
  if s1 < 0 or s2 < 0:
    return False
  return abs(s1 - s2) < CAR_LENGTH

# TODO: do we need some cost to encourage progress?
def calculate_cost(state, accel):
  accel_cost = -10.0 * abs(accel)
  collided = collision(state[0], state[2])
  collision_cost = -1000.0 if collided else 0
  return accel_cost + collision_cost, collided

def episode_over(t, collision):
  return t > 15.0 or collision
