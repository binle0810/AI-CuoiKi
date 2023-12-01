import tkinter as tk
import numpy as np

class TSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travelling Salesman Problem - Greedy Algorithm")
        self.root.geometry("700x350")  

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="white", width=600, height=300)
        self.canvas.grid(row=0, column=0, columnspan=2, rowspan=4, sticky="nsew")
        self.canvas.bind("<Button-1>", self.add_point)

        # Bảng hiển thị đường đi và tổng quãng đường
        self.table_frame = tk.Frame(self.root)
        self.table_frame.grid(row=4, column=0, columnspan=2, sticky="ew")

        self.path_label = tk.Label(self.table_frame, text="Đường đi: ")
        self.path_label.grid(row=0, column=0, sticky="w")

        self.distance_label = tk.Label(self.table_frame, text="Tổng quãng đường: ")
        self.distance_label.grid(row=1, column=0, sticky="w")

        # Nút Giải bài toán và Nút Xóa điểm
        self.solve_button = tk.Button(self.root, text="Giải bài toán", command=self.solve_tsp)
        self.solve_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.clear_button = tk.Button(self.root, text="Xóa điểm", command=self.clear_points)
        self.clear_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        self.points = []
        self.lines = []

    def add_point(self, event):
        x, y = event.x, event.y
        label = chr(65 + len(self.points))
        self.canvas.create_text(x, y, text=label, fill="red", font=("Helvetica", 10, "bold"))
        self.points.append((x, y))
        self.clear_lines()

    def clear_points(self):
        self.canvas.delete("all")
        self.points = []
        self.lines = []
        self.clear_table()

    def clear_lines(self):
        for line in self.lines:
            self.canvas.delete(line)
        self.lines = []

    def clear_table(self):
        self.path_label.config(text="Đường đi: ")
        self.distance_label.config(text="Tổng quãng đường: ")

    def total_distance(self, tour):
        total = 0
        for i in range(len(tour) - 1):
            x1, y1 = self.points[tour[i]]
            x2, y2 = self.points[tour[i + 1]]
            total += np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return total

    def solve_tsp(self):
        if len(self.points) < 2:
            return

        self.clear_lines()  # Xóa các đường đi cũ trước khi giải bài toán
        self.clear_table()  # Xóa thông tin trên bảng

        # Tính ma trận khoảng cách giữa các điểm
        distance_matrix = np.zeros((len(self.points), len(self.points)))
        for i in range(len(self.points)):
            for j in range(i + 1, len(self.points)):
                distance_matrix[i, j] = distance_matrix[j, i] = np.sqrt(
                    (self.points[i][0] - self.points[j][0]) ** 2 +
                    (self.points[i][1] - self.points[j][1]) ** 2
                )

        # Bắt đầu 
        current_city = 0 
        tour = [current_city]
        unvisited_cities = set(range(len(self.points)))
        unvisited_cities.remove(current_city)

        # Greedy Algorithm
        while unvisited_cities:
            nearest_city = min(unvisited_cities, key=lambda city: distance_matrix[current_city, city])
            tour.append(nearest_city)
            unvisited_cities.remove(nearest_city)
            current_city = nearest_city

        # Thêm bước cuối cùng để quay trở lại điểm xuất phát
        tour.append(tour[0])

        # Vẽ đường đi trên canvas
        for i in range(len(tour) - 1):
            x1, y1 = self.points[tour[i]]
            x2, y2 = self.points[tour[i + 1]]
            line = self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
            self.lines.append(line)

        # Hiển thị đường đi và tổng quãng đường trên bảng
        path_str = " -> ".join([chr(65 + city) for city in tour])
        total_distance = self.total_distance(tour)
        self.path_label.config(text=f"Đường đi: {path_str}")
        self.distance_label.config(text=f"Tổng quãng đường: {total_distance:.2f}")

def main():
    root = tk.Tk()
    app = TSPApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
