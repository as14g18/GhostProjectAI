from AI import AI
import random


class AkhiAI(AI):
    def get_velocity(self, my_mines, my_bullets, opponent_mines, opponent_bullets, health_pos, my_pos, opponent_pos):
        return health_pos[0] - my_pos[0], my_pos[1] - health_pos[1]

    def do_shoot(self, my_mines, my_bullets, opponent_mines, opponent_bullets, list_health, my_pos, opponent_pos):
        return True  # return whether to shoot or not

    def do_place_mine(self, my_mines, my_bullets, opponent_mines, opponent_bullets, list_health, my_pos, opponent_pos):
        return True if random.randint(1, 100) == 50 else False
