import turtle

# Tạo màn hình và đặt nền đỏ
screen = turtle.Screen()
screen.bgcolor("red")

# Tạo đối tượng Turtle
star = turtle.Turtle()
star.speed(1)  # Tốc độ vẽ chậm nhất

def drawStar(size):
    star.color("yellow")
    star.begin_fill()
    for i in range(5):
        star.forward(size)
        star.right(144)
        star.forward(size)
        star.left(72)
    star.end_fill()

# Đưa Turtle về vị trí ban đầu để ngôi sao nằm giữa
star.penup()  # Nhấc bút để di chuyển mà không vẽ
star.goto(25, 25)  # Tọa độ đã điều chỉnh để ngôi sao nằm chính giữa
star.pendown()  # Đặt bút xuống để bắt đầu vẽ

# Vẽ ngôi sao với kích thước 100
drawStar(100)

# Kết thúc chương trình
turtle.done()