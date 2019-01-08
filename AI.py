from abc import ABC, abstractmethod


class AI(ABC):
    def __init__(self, game_width, game_height, player_size, player_speed):
        self.game_width = game_width
        self.game_height = game_height
        self.player_size = player_size
        self.player_speed = player_speed

    @abstractmethod
    def get_velocity(self, list_mines, list_bullets, list_health, my_pos, opponent_pos):
        return 0, 0  # return tuple for coordinates

    @abstractmethod
    def do_shoot(self, list_mines, list_bullets, list_health, my_pos, opponent_pos):
        return True  # return whether to shoot or not

    @abstractmethod
    def do_place_mine(self, list_mines, list_bullets, list_health, my_pos, opponent_pos):
        return True