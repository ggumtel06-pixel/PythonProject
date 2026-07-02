import tkinter as tk
from tkinter import messagebox, simpledialog


class PomodoroRankingTimer:
    def __init__(self, root, user_name):
        self.root = root
        self.user_name = user_name.strip().upper()
        self.root.title(f"{self.user_name}'s POMODORO LEAGUE")
        self.root.geometry("700x400")  # 랭킹 보드를 위해 가로 창을 넓혔습니다.

        # 상태 관리 변수
        self.current_mode = "work"
        self.is_running = False
        self.remaining_time = 25 * 60  # 테스트용으로 빠르게 보려면 5 등으로 줄여보세요!
        self.my_tomato = 0

        # 힙한 랭킹용 가상 데이터 (경쟁자들)
        self.leaderboard_data = {
            "CODE_KING": 5,
            "COFFEE_LOVER": 3,
            self.user_name: 0,
            "PYTHON_ZEALOT": 2,
            "SLEEPY_CAT": 1
        }

        # 테마 색상
        self.bg_focus = "#1e1e2e"  # 베이스 다크
        self.bg_sidebar = "#252538"  # 랭킹 보드 배경
        self.accent_color = "#ff79c6"

        self.root.configure(bg=self.bg_focus)

        # --- 레이아웃 분할 (왼쪽: 타이머, 오른쪽: 랭킹 보드) ---
        self.left_frame = tk.Frame(root, bg=self.bg_focus, width=400, height=400)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)

        self.right_frame = tk.Frame(root, bg=self.bg_sidebar, width=280, height=400)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

        # --- 왼쪽: 타이머 컴포넌트 ---
        self.status_label = tk.Label(
            self.left_frame, text="🔥 FOCUS TIME 🔥",
            font=("Helvetica", 18, "bold"), fg=self.accent_color, bg=self.bg_focus
        )
        self.status_label.pack(pady=25)

        self.time_label = tk.Label(
            self.left_frame, text="25:00",
            font=("Helvetica", 54, "bold"), fg="#f5e0dc", bg=self.bg_focus
        )
        self.time_label.pack(pady=10)

        # 버튼 영역
        self.btn_frame = tk.Frame(self.left_frame, bg=self.bg_focus)
        self.btn_frame.pack(pady=25)

        self.start_btn = tk.Button(self.btn_frame, text="START", font=("Helvetica", 10, "bold"), bg="#a6e3a1",
                                   fg="#11111b", width=8, command=self.start_timer)
        self.start_btn.pack(side=tk.LEFT, padx=8)

        self.pause_btn = tk.Button(self.btn_frame, text="PAUSE", font=("Helvetica", 10, "bold"), bg="#f9e2af",
                                   fg="#11111b", width=8, command=self.pause_timer)
        self.pause_btn.pack(side=tk.LEFT, padx=8)

        self.skip_btn = tk.Button(self.btn_frame, text="SKIP", font=("Helvetica", 10, "bold"), bg="#89b4fa",
                                  fg="#11111b", width=8, command=self.skip_session)
        self.skip_btn.pack(side=tk.LEFT, padx=8)

        # --- 오른쪽: 실시간 랭킹 보드 컴포넌트 ---
        self.rank_title = tk.Label(
            self.right_frame, text="🏆 REAL-TIME RANKING",
            font=("Helvetica", 12, "bold"), fg="#f9e2af", bg=self.sidebar_bg_color()
        )
        self.rank_title.pack(pady=15)

        # 랭킹 명단이 들어갈 레이블 리스트 생성
        self.rank_labels = []
        for i in range(5):
            lbl = tk.Label(
                self.right_frame, text="",
                font=("Helvetica", 11), fg="#cdd6f4", bg=self.sidebar_bg_color(), anchor="w"
            )
            lbl.pack(fill=tk.X, padx=20, pady=6)
            self.rank_labels.append(lbl)

        # 첫 랭킹 화면 그리기
        self.update_leaderboard()

    def sidebar_bg_color(self):
        return self.bg_sidebar

    def update_leaderboard(self):
        """데이터를 정렬하여 랭킹 보드를 실시간으로 새로고침"""
        # 토마토 개수 기준 내림차순 정렬
        sorted_ranks = sorted(self.leaderboard_data.items(), key=lambda x: x[1], reverse=True)

        for i, (name, score) in enumerate(sorted_ranks):
            if i >= len(self.rank_labels): break

            # 메달 및 순위 표기
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f" {i + 1} "

            # 내 이름은 강조 표시
            if name == self.user_name:
                text_format = f"{medal} {name} (YOU) - 🍅x{score}"
                self.rank_labels[i].config(text=text_format, fg="#ff79c6", font=("Helvetica", 11, "bold"))
            else:
                text_format = f"{medal} {name} - 🍅x{score}"
                self.rank_labels[i].config(text=text_format, fg="#cdd6f4", font=("Helvetica", 11, "normal"))

    def update_ui_theme(self):
        """모드 변경 시 메인 타이머 테마 색상 변경"""
        if self.current_mode == "work":
            self.accent_color = "#ff79c6"
            status_text = "🔥 FOCUS TIME 🔥"
            bg_color = "#1e1e2e"
        else:
            self.accent_color = "#50fa7b"
            status_text = "🌿 BREAK TIME 🌿"
            bg_color = "#182420"

        self.root.configure(bg=bg_color)
        self.left_frame.configure(bg=bg_color)
        self.status_label.config(text=status_text, fg=self.accent_color, bg=bg_color)
        self.time_label.config(bg=bg_color)
        self.btn_frame.config(bg=bg_color)

    def countdown(self):
        if self.is_running and self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            self.time_label.config(text=f"{mins:02d}:{secs:02d}")
            self.remaining_time -= 1
            self.root.after(1000, self.countdown)
        elif self.remaining_time == 0 and self.is_running:
            self.is_running = False
            self.root.bell()
            self.switch_mode()

    def switch_mode(self):
        if self.current_mode == "work":
            self.my_tomato += 1
            self.leaderboard_data[self.user_name] = self.my_tomato  # 데이터 갱신
            self.update_leaderboard()  # 랭킹 보드 업데이트

            messagebox.showinfo("Good Job!",
                                f"🎉 {self.user_name}님 집중 성공! 🍅 1개 획득 완료.\n현재 총 {self.my_tomato}개로 랭킹이 업데이트되었습니다!")

            self.current_mode = "break"
            self.remaining_time = 5 * 60
        else:
            messagebox.showinfo("Ready?", f"🌿 휴식이 끝났습니다. 다시 집중해 볼까요?")
            self.current_mode = "work"
            self.remaining_time = 25 * 60

        self.update_ui_theme()
        mins, secs = divmod(self.remaining_time, 60)
        self.time_label.config(text=f"{mins:02d}:{secs:02d}")

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.countdown()

    def pause_timer(self):
        self.is_running = False

    def skip_session(self):
        self.is_running = False
        self.switch_mode()


if __name__ == "__main__":
    window = tk.Tk()
    window.withdraw()

    user_input = simpledialog.askstring("POMODORO LEAGUE", "리그에 참여할 닉네임을 입력하세요:")

    if not user_input or user_input.strip() == "":
        user_input = "PLAYER_1"

    window.deiconify()
    app = PomodoroRankingTimer(window, user_input)
    window.mainloop()