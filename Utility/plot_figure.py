import matplotlib.pyplot as plt

class Plot_figure:
    def __init__(self, start, goal, grid_map, global_path):
        self.start = start
        self.goal = goal
        self.grid_map = grid_map
        self.global_path = global_path
        self.obstacle = []
        
    def plot_obstacle(self):
        
        for i in range(len(self.grid_map)):
            for j in range(len(self.grid_map)):
                if self.grid_map[j][i] == 1:
                    self.obstacle.append([i, j])

        if self.obstacle != []:
            obstacle_x, obstacle_y = zip(*self.obstacle)
            obstacle_x = [i+1 for i in obstacle_x]
            obstacle_y = [i+1 for i in obstacle_y]
            plt.plot(obstacle_x, obstacle_y, "s", color="gray", markersize=10, label='Obstacle')
            
            boundary_x_down = [i for i in range(0, len(self.grid_map)+2)]
            boundary_y_down = [0 for i in range(0, len(self.grid_map)+2)]
            boundary_x_up = [i for i in range(0, len(self.grid_map)+2)]
            boundary_y_up = [len(self.grid_map)+1 for i in range(0, len(self.grid_map)+2)]
            boundary_x_left = [0 for i in range(0, len(self.grid_map)+2)]
            boundary_y_left = [i for i in range(0, len(self.grid_map)+2)]
            boundary_x_right = [len(self.grid_map)+1 for i in range(0, len(self.grid_map)+2)]
            boundary_y_right = [i for i in range(0, len(self.grid_map)+2)]
            boundary_x = boundary_x_down + boundary_x_up + boundary_x_left + boundary_x_right
            boundary_y = boundary_y_down + boundary_y_up + boundary_y_left + boundary_y_right
            plt.plot(boundary_x, boundary_y, "s", color="gray", markersize=10) #, label='Boundary')
        
    def plot_figure(self):

        plt.figure(figsize=(6, 6))
        
        self.plot_obstacle()
                   
        path_x, path_y = zip(*self.global_path)
        path_x = [i for i in path_x]
        path_y = [i for i in path_y]
            
        plt.plot(self.start[0], self.start[1], "bs", markersize=10, label='Start')
        plt.plot(self.goal[0], self.goal[1], "gs", markersize=10, label='Goal')

        plt.plot(path_x, path_y, "r--", markersize=8, label='Path')

        plt.title("Global Path Planning based A* algorithm")
        plt.legend(loc='upper left', fontsize = 10)
        plt.xlim(0, len(self.grid_map)+1)
        plt.ylim(-1, len(self.grid_map)+1)
        plt.grid(visible=True)
        plt.show()

