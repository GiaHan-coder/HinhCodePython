import tkinter as tk
import math
import random
import time

# Thiết lập cửa sổ
WIDTH, HEIGHT = 800, 600
root = tk.Tk()
root.title("Heart Particle Animation with Enhanced Text")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#000000")
canvas.pack()

# Cấu hình hạt
settings = {
    "particles": {
        "length": 1000,
        "duration": 4,
        "velocity": 80,
        "effect": -1.3,
        "size": 8,
    }
}

# Lớp Point
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def clone(self):
        return Point(self.x, self.y)

    def length(self, length=None):
        if length is None:
            return math.sqrt(self.x * self.x + self.y * self.y)
        self.normalize()
        self.x *= length
        self.y *= length
        return self

    def normalize(self):
        length = self.length()
        if length != 0:
            self.x /= length
            self.y /= length
        return self

# Lớp Particle
class Particle:
    def __init__(self):
        self.position = Point()
        self.velocity = Point()
        self.acceleration = Point()
        self.age = 0
        self.id = None

    def initialize(self, x, y, dx, dy):
        self.position.x = x
        self.position.y = y
        self.velocity.x = dx
        self.velocity.y = dy
        self.acceleration.x = dx * settings["particles"]["effect"]
        self.acceleration.y = dy * settings["particles"]["effect"]
        self.age = 0

    def update(self, delta_time):
        self.position.x += self.velocity.x * delta_time
        self.position.y += self.velocity.y * delta_time
        self.velocity.x += self.acceleration.x * delta_time
        self.velocity.y += self.acceleration.y * delta_time
        self.age += delta_time

    def draw(self, canvas):
        if self.id:
            canvas.delete(self.id)
        alpha = 1 - self.age / settings["particles"]["duration"]
        if alpha > 0:
            size = settings["particles"]["size"] * (1 - (self.age / settings["particles"]["duration"]) ** 3)
            color = f"#{int(255):02x}{int(11):02x}{int(2):02x}"
            self.id = canvas.create_oval(
                self.position.x - size / 2,
                self.position.y - size / 2,
                self.position.x + size / 2,
                self.position.y + size / 2,
                fill=color,
                outline=""
            )

# Lớp ParticlePool
class ParticlePool:
    def __init__(self, length):
        self.particles = [Particle() for _ in range(length)]
        self.first_active = 0
        self.first_free = 0
        self.duration = settings["particles"]["duration"]

    def add(self, x, y, dx, dy):
        self.particles[self.first_free].initialize(x, y, dx, dy)
        self.first_free = (self.first_free + 1) % len(self.particles)
        if self.first_active == self.first_free:
            self.first_active = (self.first_active + 1) % len(self.particles)

    def update(self, delta_time):
        if self.first_active < self.first_free:
            for i in range(self.first_active, self.first_free):
                self.particles[i].update(delta_time)
        elif self.first_free < self.first_active:
            for i in range(self.first_active, len(self.particles)):
                self.particles[i].update(delta_time)
            for i in range(self.first_free):
                self.particles[i].update(delta_time)

        while (self.particles[self.first_active].age >= self.duration and
               self.first_active != self.first_free):
            self.first_active = (self.first_active + 1) % len(self.particles)

    def draw(self, canvas):
        if self.first_active < self.first_free:
            for i in range(self.first_active, self.first_free):
                self.particles[i].draw(canvas)
        elif self.first_free < self.first_active:
            for i in range(self.first_active, len(self.particles)):
                self.particles[i].draw(canvas)
            for i in range(self.first_free):
                self.particles[i].draw(canvas)

# Hàm tạo điểm trên trái tim
def point_on_heart(t):
    x = 160 * math.sin(t) ** 3
    y = 130 * math.cos(t) - 50 * math.cos(2 * t) - 20 * math.cos(3 * t) - 10 * math.cos(4 * t) + 25
    return Point(x, y)

# Hàm tạo màu ngẫu nhiên
def random_color():
    r = random.randint(100, 255)
    g = random.randint(50, 200)
    b = random.randint(50, 255)
    return f'#{r:02x}{g:02x}{b:02x}'

# Khởi tạo ParticlePool
particles = ParticlePool(settings["particles"]["length"])
particle_rate = settings["particles"]["length"] / settings["particles"]["duration"]

# Biến thời gian và văn bản
last_time = time.time()
text_id = None
text_x = WIDTH / 2 - 100  # Vị trí x ban đầu
text_y = HEIGHT / 2       # Vị trí y giữa trái tim
text_speed = 100          # Tốc độ di chuyển của văn bản
text_direction = 1        # Hướng di chuyển
text_opacity = 1.0        # Độ trong suốt
opacity_direction = -0.02 # Hướng thay đổi độ trong suốt
shake_intensity = 5       # Mức độ rung

# Hàm cập nhật animation
def update():
    global last_time, text_id, text_x, text_direction, text_opacity, opacity_direction
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    # Xóa màn hình
    canvas.delete("all")
    canvas.configure(bg="#000000")

    # Tạo hạt mới
    amount = int(particle_rate * delta_time)
    for _ in range(amount):
        t = math.pi - 2 * math.pi * random.random()
        pos = point_on_heart(t)
        dir = pos.clone().length(settings["particles"]["velocity"])
        particles.add(WIDTH / 2 + pos.x, HEIGHT / 2 - pos.y, dir.x, -dir.y)

    # Cập nhật và vẽ hạt
    particles.update(delta_time)
    particles.draw(canvas)

    # Cập nhật vị trí văn bản "I Love You"
    text_x += text_speed * text_direction * delta_time
    heart_width = 320
    text_padding = 50
    if text_x > WIDTH / 2 + heart_width / 2 - text_padding:
        text_direction = -1
    elif text_x < WIDTH / 2 - heart_width / 2 + text_padding:
        text_direction = 1

    # Cập nhật độ trong suốt (fade in/out)
    text_opacity += opacity_direction
    if text_opacity <= 0.2 or text_opacity >= 1:
        opacity_direction *= -1

    # Tạo hiệu ứng rung
    shake_x = random.randint(-shake_intensity, shake_intensity)
    shake_y = random.randint(-shake_intensity, shake_intensity)

    # Vẽ văn bản với hiệu ứng
    if text_id:
        canvas.delete(text_id)
    color = random_color()
    text_id = canvas.create_text(
        text_x + shake_x,
        text_y + shake_y,
        text="I Love You",
        fill=color,
        font=("Arial", 24, "bold"),
        tags="text"
    )

    # Lặp lại animation
    root.after(16, update)

# Bắt đầu animation
update()

# Chạy cửa sổ
root.mainloop()