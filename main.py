import tkinter as tk
import random

# ================= 遊戲設定 =================
GAME_WIDTH = 600
GAME_HEIGHT = 600
SPACE_SIZE = 25
INITIAL_SPEED = 120  # 毫秒（越小越快）
BG_COLOR = "#181825"        # 深黑底色
SNAKE_COLOR = "#a6e3a1"     # 霓虹綠蛇身
HEAD_COLOR = "#94e2d5"      # 蛇頭亮色
FOOD_COLOR = "#f38ba8"      # 霓虹紅食物
FONT_FAMILY = "Microsoft JhengHei"
# ============================================

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Snake - 貪食蛇小遊戲")
        self.root.resizable(False, False)

        self.score = 0
        self.high_score = 0
        self.direction = "Right"
        self.running = False
        self.speed = INITIAL_SPEED

        # 頂部計分板
        self.score_frame = tk.Frame(root, bg="#11111b", pady=10)
        self.score_frame.pack(fill="x")

        self.label_score = tk.Label(
            self.score_frame, 
            text="目前分數: 0", 
            font=(FONT_FAMILY, 14, "bold"), 
            fg="#cdd6f4", 
            bg="#11111b"
        )
        self.label_score.pack(side="left", padx=20)

        self.label_high = tk.Label(
            self.score_frame, 
            text="最高紀錄: 0", 
            font=(FONT_FAMILY, 14, "bold"), 
            fg="#f9e2af", 
            bg="#11111b"
        )
        self.label_high.pack(side="right", padx=20)

        # 遊戲主畫布
        self.canvas = tk.Canvas(root, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH, highlightthickness=0)
        self.canvas.pack()

        # 鍵盤綁定 (支援方向鍵與 WASD)
        self.root.bind("<Up>", lambda e: self.change_direction("Up"))
        self.root.bind("<Down>", lambda e: self.change_direction("Down"))
        self.root.bind("<Left>", lambda e: self.change_direction("Left"))
        self.root.bind("<Right>", lambda e: self.change_direction("Right"))
        self.root.bind("<w>", lambda e: self.change_direction("Up"))
        self.root.bind("<s>", lambda e: self.change_direction("Down"))
        self.root.bind("<a>", lambda e: self.change_direction("Left"))
        self.root.bind("<d>", lambda e: self.change_direction("Right"))
        self.root.bind("<space>", lambda e: self.start_game() if not self.running else None)

        self.show_start_screen()

    def show_start_screen(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            GAME_WIDTH / 2, GAME_HEIGHT / 2 - 40,
            text="🐍 NEON SNAKE", font=(FONT_FAMILY, 32, "bold"), fill="#a6e3a1"
        )
        self.canvas.create_text(
            GAME_WIDTH / 2, GAME_HEIGHT / 2 + 20,
            text="使用【方向鍵】或【W A S D】移動", font=(FONT_FAMILY, 14), fill="#cdd6f4"
        )
        self.canvas.create_text(
            GAME_WIDTH / 2, GAME_HEIGHT / 2 + 70,
            text="▶ 按【空白鍵 Space】開始遊戲 ◀", font=(FONT_FAMILY, 16, "bold"), fill="#f9e2af"
        )

    def start_game(self):
        self.canvas.delete("all")
        self.score = 0
        self.speed = INITIAL_SPEED
        self.direction = "Right"
        self.running = True
        self.label_score.config(text="目前分數: 0")

        # 初始化蛇身（預設 3 節）
        self.snake = [
            (SPACE_SIZE * 3, SPACE_SIZE * 5),
            (SPACE_SIZE * 2, SPACE_SIZE * 5),
            (SPACE_SIZE * 1, SPACE_SIZE * 5)
        ]
        self.spawn_food()
        self.next_turn()

    def spawn_food(self):
        while True:
            x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def change_direction(self, new_dir):
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if self.running and new_dir != opposites.get(self.direction):
            self.direction = new_dir

    def next_turn(self):
        if not self.running:
            return

        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            head_y -= SPACE_SIZE
        elif self.direction == "Down":
            head_y += SPACE_SIZE
        elif self.direction == "Left":
            head_x -= SPACE_SIZE
        elif self.direction == "Right":
            head_x += SPACE_SIZE

        new_head = (head_x, head_y)

        # 撞牆判定
        if head_x < 0 or head_x >= GAME_WIDTH or head_y < 0 or head_y >= GAME_HEIGHT:
            self.game_over()
            return

        # 咬到自己判定
        if new_head in self.snake:
            self.game_over()
            return

        # 前進移動
        self.snake.insert(0, new_head)

        # 吃到食物判定
        if new_head == self.food:
            self.score += 10
            self.label_score.config(text=f"目前分數: {self.score}")
            if self.score > self.high_score:
                self.high_score = self.score
                self.label_high.config(text=f"最高紀錄: {self.high_score}")
            
            # 隨分數增加速度微幅提升
            if self.speed > 60:
                self.speed -= 2
            
            self.spawn_food()
        else:
            self.snake.pop()

        self.draw_elements()
        self.root.after(self.speed, self.next_turn)

    def draw_elements(self):
        self.canvas.delete("all")

        # 畫食物 (霓虹發光球感)
        fx, fy = self.food
        self.canvas.create_oval(
            fx + 2, fy + 2, fx + SPACE_SIZE - 2, fy + SPACE_SIZE - 2,
            fill=FOOD_COLOR, outline="#f5c2e7", width=2
        )

        # 畫蛇身
        for i, (sx, sy) in enumerate(self.snake):
            color = HEAD_COLOR if i == 0 else SNAKE_COLOR
            self.canvas.create_rectangle(
                sx + 1, sy + 1, sx + SPACE_SIZE - 1, sy + SPACE_SIZE - 1,
                fill=color, outline=""
            )

    def game_over(self):
        self.running = False
        self.canvas.create_rectangle(
            50, GAME_HEIGHT / 2 - 90, GAME_WIDTH - 50, GAME_HEIGHT / 2 + 90,
            fill="#11111b", outline="#f38ba8", width=2
        )
        self.canvas.create_text(
            GAME_WIDTH / 2, GAME_HEIGHT / 2 - 30,
            text="💥 GAME OVER", font=(FONT_FAMILY, 28, "bold"), fill="#f38ba8"
        )
        self.canvas.create_text(
            GAME_WIDTH / 2, GAME_HEIGHT / 2 + 15,
            text=f"最終得分: {self.score}", font=(FONT_FAMILY, 16), fill="#cdd6f4"
        )
        self.canvas.create_text(
            GAME_WIDTH / 2, GAME_HEIGHT / 2 + 50,
            text="按【空白鍵 Space】重新挑戰", font=(FONT_FAMILY, 13), fill="#a6e3a1"
        )

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
