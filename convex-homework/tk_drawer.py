from tkinter import *
import math

# Размер окна
SIZE = 1080
# Коэффициент гомотетии
SCALE = 50


def x(p):
    """преобразование x-координаты"""
    return SIZE / 2 + SCALE * p.x


def y(p):
    """преобразование y-координаты"""
    return SIZE / 2 - SCALE * p.y


class TkDrawer:
    """Графический интерфейс для выпуклой оболочки"""

    # Конструктор
    def __init__(self):
        self.root = Tk()
        self.root.title("Выпуклая оболочка")
        self.root.geometry(f"{SIZE+5}x{SIZE+5}")
        self.root.resizable(False, False)
        self.root.bind("<Control-c>", quit)
        self.canvas = Canvas(self.root, width=SIZE, height=SIZE)
        self.canvas.pack(padx=5, pady=5)

    # Завершение работы
    def close(self):
        self.root.quit()

    # Стирание существующей картинки и рисование осей координат
    def clean(self):
        self.canvas.create_rectangle(0, 0, SIZE, SIZE, fill="white")
        self.canvas.create_line(0, SIZE / 2, SIZE, SIZE / 2, fill="blue")
        self.canvas.create_line(SIZE / 2, 0, SIZE / 2, SIZE, fill="blue")
        self.root.update()

    # Рисование точки
    def draw_point(self, p):
        self.canvas.create_oval(
            x(p) + 1, y(p) + 1, x(p) - 1, y(p) - 1, fill="black"
        )
        self.root.update()

    # Рисование линии
    def draw_line(self, p, q, color="black"):
        self.canvas.create_line(x(p), y(p), x(q), y(q), fill=color, width=2)
        self.root.update()

    def draw_neighbourhood(self, p, q, r, color="black"):
        dy1 = y(q) - y(p)
        dx1 = x(q) - x(p)

        dy2 = y(r) - y(q)
        dx2 = x(r) - x(q)

        dist = math.sqrt((dy1) ** 2 + (dx1) ** 2)
        x_p1 = x(p) + (-(dy1)) / dist * SCALE
        y_p1 = y(p) + (dx1) / dist * SCALE
        x_q1 = x(q) + (-(dy1)) / dist * SCALE
        y_q1 = y(q) + (dx1) / dist * SCALE

        start_angle = math.degrees(math.atan2(-dx1, -dy1))
        end_angle = math.degrees(math.atan2(-dx2, -dy2))
        extent = end_angle - start_angle

        while extent <= -180:
            extent += 360
        while extent > 180:
            extent -= 360

        self.canvas.create_arc(
            x(q) - SCALE,
            y(q) - SCALE,
            x(q) + SCALE,
            y(q) + SCALE,
            style="arc",
            start=start_angle,
            extent=extent,
            outline=color,
            width=2,
        )
        self.canvas.create_line(x_p1, y_p1, x_q1, y_q1, fill=color, width=2)
        self.root.update()

    def draw_distance(self, p, q, h, color="black"):
        dy1 = y(q) - y(p)
        dx1 = x(q) - x(p)

        dy2 = y(h) - y(q)
        dx2 = x(h) - x(q)

        dist = math.sqrt((dy1) ** 2 + (dx1) ** 2)
        x_p1 = x(p) + (-(dy1)) / dist * SCALE
        y_p1 = y(p) + (dx1) / dist * SCALE
        x_q1 = x(q) + (-(dy1)) / dist * SCALE
        y_q1 = y(q) + (dx1) / dist * SCALE

        scalar_mul = (x_q1 - x_p1) * (x(h) - x_p1) + (y_q1 - y_p1) * (
            y(h) - y_p1
        )
        dist1 = (x_q1 - x_p1) ** 2 + (y_q1 - y_p1) ** 2  # длина вектора PQ

        x_h1 = x_p1 + scalar_mul / dist1 * (x_q1 - x_p1)
        y_h1 = y_p1 + scalar_mul / dist1 * (y_q1 - y_p1)
        self.canvas.create_line(x(h), y(h), x_h1, y_h1, fill=color, width=1)
        self.root.update()


if __name__ == "__main__":

    import time
    from r2point import R2Point

    tk = TkDrawer()
    tk.clean()
    tk.draw_point(R2Point(2.0, 2.0))
    tk.draw_line(R2Point(0.0, 0.0), R2Point(1.0, 1.0))
    tk.draw_line(R2Point(0.0, 0.0), R2Point(1.0, 0.0))
    time.sleep(5)
