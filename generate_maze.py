import random
import numpy as np
import matplotlib.pyplot as plt
import cv2
from moviepy.editor import ImageSequenceClip


class Maze():
    """ 迷路を作るクラス"""
    PATH = 1
    WALL = 0
    def __init__(self, width, height):
        self.maze = []
        self.width = width
        self.height = height
        # 迷路は、幅高さ5以上の奇数で生成する。
        if(self.height < 5 or self.width < 5):
            print('at least 5')
            exit()
        if (self.width % 2) == 0:
            self.width += 1
        if (self.height % 2) == 0:
            self.height += 1
    def set_out_wall(self):
        """ 迷路全体を構成する2次元配列、迷路の外周を壁とし、それ以外を通路とする。"""
        for _x in range(0, self.width):
            row = []
            for _y in range(0, self.height):
                if (_x == 0 or _y == 0 or _x == self.width-1 or _y == self.height -1):
                    cell = self.WALL
                else:
                    cell = self.PATH
                row.append(cell)
            self.maze.append(row)
        return self.maze
    def set_inner_wall_boutaosi(self, save=True):
        """迷路の中に棒を立ててランダムな方向に倒す。
        外周の内側に基準となる棒を1セルおき、(x, y ともに偶数の座標)に配置する。"""
        gif = []
        for _x in range(2, self.width-1, 2):
            for _y in range(2, self.height-1, 2):
                self.maze[_x][_y] = self.WALL
                # 棒をランダムな方向に倒して壁とする。
                # (ただし以下に当てはまる方向以外に倒す。)
                # 1行目の内側の壁以外では上方向に倒してはいけない。
                # すでに棒が倒され壁になっている場合、その方向には倒してはいけない。
                while True:
                    if _y == 2:
                        direction = random.randrange(0, 4)
                    else:
                        direction = random.randrange(0, 3)
                    # 棒を倒して壁にする方向を決める。
                    wall_x = _x
                    wall_y = _y
                    # 右
                    if direction == 0:
                        wall_x += 1
                    # 下
                    elif direction == 1:
                        wall_y += 1
                    # 左
                    elif direction == 2:
                        wall_x -= 1
                    # 上
                    else:
                        wall_y -= 1
                    # 壁にする方向が壁でない場合は壁にする。
                    if self.maze[wall_x][wall_y] != self.WALL:
                        self.maze[wall_x][wall_y] = self.WALL
                        if save:
                            map = np.repeat(np.array(self.maze)[:, :, None].astype(np.uint8) * 255, 3, axis=2)
                            gif.append(cv2.resize(map, (map.shape[1]*20, map.shape[0]*20), interpolation=cv2.INTER_NEAREST))
                        break
        if save:
            map = np.repeat(np.array(self.maze)[:, :, None].astype(np.uint8) * 255, 3, axis=2)
            map = cv2.resize(map, (map.shape[1]*20, map.shape[0]*20), interpolation=cv2.INTER_NEAREST)
            gif.append(map)
            gif.append(map)
            gif.append(map)
            clip = ImageSequenceClip(gif, fps=3)
            clip.write_gif('create.gif')
        return self.maze
    def set_start_goal(self, sx=None, sy=None, ex=None, ey=None):
        """ スタートとゴールを迷路にいれる。"""
        # 迷路内に含まれているか判断
        flag = False
        if sx is not None or sy is not None or ex is not None or ey is not None:
            if 0 < sx and 0 < sy and 0 < ex and 0 < ey and sx < self.width-1 \
                and sy < self.height-1 and ex < self.width-1 and ey < self.height-1:  # 座標がマップ内に存在しているか
                if self.maze[sy][sx] == str(self.PATH) and self.maze[ey][ex] == str(self.PATH):  # 座標位置が通路かどうか
                    flag = True
        if sx and sy and flag:
            self.maze[sy][sx] = 'S'
        else:
            self.maze[1][1] = 'S'
        if ex and ey and flag:
            self.maze[ex][ey] = 'G'
        else:
            self.maze[self.width-2][self.height-2] = 'G'
        return self.maze
    def print_maze(self):
        """ 迷路を出力する。"""
        for row in self.maze:
            for cell in row:
                if cell == self.PATH:
                    print('   ', end='')
                elif cell == self.WALL:
                    print('###', end='')
                elif cell == 'S':
                    print('STR', end='')
                elif cell == 'G':
                    print('GOL', end='')
            print()

    def visualize_maze(self):
        """ OpenCVを使って可視化 """
        maze_viz = np.array(self.maze)
        # Start, Endの保存，ついでに消去
        sy, sx = np.where(maze_viz == 'S')
        sy, sx = sy[0], sx[0]
        maze_viz[maze_viz == 'S'] = str(self.PATH)
        ey, ex = np.where(maze_viz == 'G')
        ey, ex = ey[0], ex[0]
        maze_viz[maze_viz == 'G'] = str(self.PATH)
        maze_viz = np.repeat(maze_viz[:, :, None].astype(np.uint8), 3, axis=2)
        # スタートとゴールに色塗り (Start: シアン Goal: イエロー)
        maze_viz[sy, sx] = [1, 1, 0]
        maze_viz[ey, ex] = [0, 1, 1]

        self.map_visualize(maze_viz)
        return maze_viz

    def map_visualize(self, map, save=True):
        map = map * 255
        if save:
            cv2.imwrite('maze_viz.png', cv2.resize(map, (self.width*10, self.height*10), interpolation=cv2.INTER_NEAREST))
        map = cv2.cvtColor(map, cv2.COLOR_BGR2RGB)
        plt.imshow(map)
        plt.show()


maze = Maze(20, 20)
maze.set_out_wall()
maze_map = np.array(maze.set_inner_wall_boutaosi()).astype(np.uint8)
maze.set_start_goal()
# maze.print_maze()
maze.visualize_maze()

print(np.array(maze_map))