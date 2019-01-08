from AI import AI
import random


class AkhiAI(AI):
    def get_velocity(self, list_mines, list_bullets, list_health, my_pos, opponent_pos):
        return random.randint(-1, 1), random.randint(-1, 1)

    def do_shoot(self, list_mines, list_bullets, list_health, my_pos, opponent_pos):
        return True  # return whether to shoot or not

    def do_place_mine(self, list_mines, list_bullets, list_health, my_pos, opponent_pos):
        return True if random.randint(1, 100) == 50 else False
