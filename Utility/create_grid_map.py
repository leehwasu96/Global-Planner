import tkinter as tk

class ParkingEnvironment:
    def __init__(self, root, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cell_size = 15  # 각 셀의 크기 설정
        self.parking_map = [[0] * cols for _ in range(rows)]

        self.root = root
        self.canvas = tk.Canvas(root, width=cols * self.cell_size, height=rows * self.cell_size)
        self.canvas.pack()

        self.draw_parking_map()

        # 추가: 이전 클릭 상태 저장 변수
        self.prev_clicked = None
        # 추가: 이동 중에 이미 변경된 셀을 저장하는 집합
        self.changed_cells = set()
        # 추가: 오른쪽 클릭으로 선택된 두 셀의 위치 저장 변수
        self.right_clicked_cells = None

        # 추가: Clear, Load, Save, Exit 버튼 순서대로 배치
        clear_button = tk.Button(root, text="Clear", command=self.clear_parking_map)
        clear_button.pack(side=tk.LEFT)

        load_button = tk.Button(root, text="Load", command=self.load_from_txt)
        load_button.pack(side=tk.LEFT)

        save_button = tk.Button(root, text="Save", command=self.save_to_txt)
        save_button.pack(side=tk.LEFT)

        exit_button = tk.Button(root, text="Exit", command=self.on_window_close)
        exit_button.pack(side=tk.RIGHT)

        # 변경: 마우스 클릭을 뗀 후에도 계속 드래그 가능하도록
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        # 추가: 오른쪽 클릭 이벤트 처리
        self.canvas.bind("<Button-3>", self.on_right_mouse_click)

        self.root.bind("<Escape>", self.on_window_close)

    def draw_parking_map(self):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                color = "white" if self.parking_map[i][j] == 0 else "black"
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = (j + 1) * self.cell_size, (i + 1) * self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

        # Canvas 크기를 업데이트
        self.canvas.config(width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        
    def on_mouse_click(self, event):
        row = event.y // 15
        col = event.x // 15

        if 0 <= row < self.rows and 0 <= col < self.cols:
            # 추가: 이전 클릭 상태와 변경된 셀 초기화
            self.prev_clicked = (row, col)
            self.changed_cells = set()
            # 추가: 클릭한 셀의 값을 변경
            self.parking_map[row][col] = 1 if self.parking_map[row][col] == 0 else 0
            self.draw_parking_map()

    def on_mouse_drag(self, event):
        row = event.y // 15
        col = event.x // 15

        if 0 <= row < self.rows and 0 <= col < self.cols:
            # 추가: 이동 중에 이미 변경된 셀은 건너뛰기
            if (row, col) != self.prev_clicked and (row, col) not in self.changed_cells:
                self.parking_map[row][col] = 1 if self.parking_map[row][col] == 0 else 0
                self.changed_cells.add((row, col))
                self.draw_parking_map()

    def on_mouse_release(self, event):
        # 변경: 마우스 클릭을 뗀 후에도 계속 드래그 가능하도록
        self.prev_clicked = None

    def on_right_mouse_click(self, event):
        row = event.y // 15
        col = event.x // 15

        if 0 <= row < self.rows and 0 <= col < self.cols:
            # 추가: 오른쪽 클릭으로 선택된 두 셀의 위치 저장
            if self.right_clicked_cells is None:
                self.right_clicked_cells = (row, col)
            else:
                # 추가: 선택된 두 셀 간의 모든 셀의 값을 바꾸기
                start_row, start_col = self.right_clicked_cells
                self.draw_line(start_col, start_row, col, row, toggle=True)
                self.right_clicked_cells = None
                self.draw_parking_map()

    def on_window_close(self, event=None):
        self.root.destroy()

    def save_to_txt(self):
        with open("grid_map_2.txt", "w") as file:
            for row in self.parking_map:
                file.write(" ".join(map(str, row)) + "\n")

        print("Grid map saved to grid_map_2.txt")

    def load_from_txt(self):
        try:
            with open("grid_map_2.txt", "r") as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    values = list(map(int, line.strip().split()))
                    if i < self.rows:
                        self.parking_map[i] = values
            self.draw_parking_map()
        except FileNotFoundError:
            print("No previous grid map found.")

    def clear_parking_map(self):
        self.parking_map = [[0] * self.cols for _ in range(self.rows)]
        self.draw_parking_map()

    def draw_line(self, x0, y0, x1, y1, toggle=False):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while x0 != x1 or y0 != y1:
            # toggle 옵션을 이용하여 값을 변경
            if toggle:
                # 0: free space / 1: obstacle
                self.parking_map[y0][x0] = 1 if self.parking_map[y0][x0] == 0 else 0
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

        # 추가: 마지막 셀에서도 값을 변경
        if toggle:
            # 0: free space / 1: obstacle
            self.parking_map[y0][x0] = 1 if self.parking_map[y0][x0] == 0 else 0
def main():
    root = tk.Tk()
    root.title("Grid map")

    # 주차 환경 크기 설정 (예: 5x5)
    rows, cols = 30, 30

    parking_environment = ParkingEnvironment(root, rows, cols)

    root.mainloop()

if __name__ == "__main__":
    main()
