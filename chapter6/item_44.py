import copyreg
import pickle


# Version 1
# class GameStart(object):
#
#     def __init__(self, level=0, lives=4, points=0):
#         self.level = level
#         self.lives = lives
#         self.points = points


class GameStart(object):

    def __init__(self, level=0, points=0):
        self.level = level
        self.points = points


def unpickle_game_state(kwargs):
    version = kwargs.pop('version', 1)
    if version == 1:
        kwargs.pop('lives')
    return GameStart(**kwargs)


def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    kwargs['version'] = 2
    return unpickle_game_state, (kwargs,)

state = GameStart()
state.level += 1

copyreg.pickle(GameStart, pickle_game_state)
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)

print(state_after.__dict__)
