import gymnasium as gym
from chinese_chess import ChineseChess


class ChineseChessEnv(gym.Env):
    def __init__(self):
        super(ChineseChessEnv, self).__init__()
        self.game = ChineseChess()
        self.action_space = None
        self.observation_space = None
        self.reset()
        self.render_mode = "human"

    def reset(self):
        self.game.reset()
        observation = self.game.get_observation()
        info = {}
        return observation, info
    
    def step(self, action):
        if not self.game.is_valid_action(action):
            raise ValueError("Invalid action")
        
        reward = self.game.perform_action(action)
        observation = self.game.get_observation()
        terminated = self.game.is_game_over()
        truncated = False