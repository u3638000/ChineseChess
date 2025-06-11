from cc_gym import ChineseChessEnv

# 创建环境
env = ChineseChessEnv()

# 重置环境
observation, info = env.reset()

for _ in range(1000):
    # 随机选择动作
    action = env.action_space.sample()
    
    # 执行动作
    observation, reward, terminated, truncated, info = env.step(action)
    
    # 渲染环境
    env.render()
    
    # 如果游戏结束，重置环境
    if terminated or truncated:
        observation, info = env.reset()

# 关闭环境
env.close()