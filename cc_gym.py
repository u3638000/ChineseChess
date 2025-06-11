import gymnasium as gym
from gymnasium import spaces
import numpy as np
from chinese_chess import ChineseChess


class ChineseChessEnv(gym.Env):
    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 30,
        "name": "ChineseChessEnv",
        "description": "A custom environment for playing Chinese Chess.",
    }
    def __init__(self, render_mode=None):
        super(ChineseChessEnv, self).__init__()
        self.chess_game = ChineseChess()
        self.render_mode = render_mode
        
        # 动态动作空间 - 会在每次调用reset()和step()后更新
        self.action_space = spaces.Discrete(1)  # 初始化为1，之后动态更新
        
        # 观察空间 - 10x9 棋盘，每个位置有14种可能状态（空、红方7种棋子、黑方7种棋子）
        # 0: 空, 1-7: 红方(帅1,仕2,相3,马4,车5,炮6,兵7), 8-14: 黑方(将8,士9,象10,马11,车12,炮13,卒14)
        self.observation_space = spaces.Box(
            low=0, high=14, shape=(10, 9), dtype=np.uint8
        )
        
        # 棋子映射
        self.piece_to_id = {
            'empty': 0,
            'red_general': 1, 'red_advisor': 2, 'red_elephant': 3, 
            'red_horse': 4, 'red_chariot': 5, 'red_cannon': 6, 'red_soldier': 7,
            'black_general': 8, 'black_advisor': 9, 'black_elephant': 10, 
            'black_horse': 11, 'black_chariot': 12, 'black_cannon': 13, 'black_soldier': 14
        }
        
        self.valid_actions = []
        self.state = None

    def _get_obs(self):
        # 将棋盘状态转换为神经网络可用的张量格式
        board_tensor = np.zeros((10, 9), dtype=np.uint8)
        
        for row in range(10):
            for col in range(9):
                piece = self.chess_game.board[row][col]
                if piece is None:
                    board_tensor[row][col] = self.piece_to_id['empty']
                else:
                    piece_id = f"{piece['color']}_{piece['type']}"
                    board_tensor[row][col] = self.piece_to_id[piece_id]
                    
        return board_tensor
    
    def _get_info(self):
        # 返回额外的状态信息
        return {
            "turn": self.chess_game.turn,
            "in_check": self.chess_game.is_in_check(self.chess_game.turn),
            "game_over": self.chess_game.game_over,
            "winner": self.chess_game.winner,
            "valid_actions": self.valid_actions,
        }

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # 重置棋盘
        self.chess_game.reset()
        
        # 获取有效动作
        self.valid_actions = self.chess_game.get_action_space()
        
        # 更新动态动作空间
        self.action_space = spaces.Discrete(len(self.valid_actions))
        
        # 获取观察
        observation = self._get_obs()
        info = self._get_info()
        
        return observation, info

    def step(self, action):
        # action是valid_actions列表中的索引
        if action >= len(self.valid_actions):
            raise ValueError(f"无效动作索引: {action}, 有效动作数量: {len(self.valid_actions)}")
        
        # 获取动作对应的起始位置和目标位置
        from_pos, to_pos = self.valid_actions[action]
        
        # 执行移动
        move_success = self.chess_game.make_move(from_pos, to_pos)
        
        # 如果移动失败（不应该发生，因为我们使用的是有效动作）
        if not move_success:
            print("警告: 选择了有效动作列表中的动作，但移动失败")
        
        # 判断是否终止
        terminated = self.chess_game.game_over
        
        # 截断标志，在这个环境中与终止相同
        truncated = False

        # 获取新的观察
        observation = self._get_obs()
        
        # 更新有效动作
        self.valid_actions = self.chess_game.get_action_space()
        
        # 更新动态动作空间
        if not terminated:
            assert len(self.valid_actions) > 0, f"{self._get_info()}\n\n{self.chess_game.board_to_string()}"
        self.action_space = spaces.Discrete(len(self.valid_actions)) if not terminated else spaces.Discrete(1)
        
        # 计算奖励
        reward = 0
        if self.chess_game.game_over:
            reward = 1.0 if self.chess_game.winner == 'red' else -1.0
        
        # 额外信息
        info = self._get_info()
        
        return observation, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "human":
            # 使用pygame窗口渲染
            self.chess_game.draw_board()
            self.chess_game.draw_pieces()
            self.chess_game.draw_game_status()
            
            import pygame
            pygame.display.flip()
            return None
        
        elif self.render_mode == "rgb_array":
            raise NotImplementedError("RGB array rendering is not implemented yet.")

    def close(self):
        import pygame
        pygame.quit()


def simple_test():
    env = ChineseChessEnv(render_mode="human")
    observation, info = env.reset()
    for _ in range(5000):
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        env.render()
        if terminated:
            observation, info = env.reset()
    env.close()

if __name__ == "__main__":
    for _ in range(10):
        simple_test()