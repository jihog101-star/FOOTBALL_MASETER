
import tkinter as tk
from tkinter import messagebox
import sqlite3
import math

# Matplotlib 그래프 기능
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# ==============================
# 기본 디자인 설정
# ==============================

BG_COLOR = "#0D0F0D"
PANEL_COLOR = "#191D19"
GREEN = "#B7FF00"
WHITE = "#FFFFFF"
GRAY = "#929A92"
RED = "#FF5555"
BLUE = "#55AAFF"


class FootballMaster:

    def __init__(self, window):
        self.window = window
        self.window.title("FOOTBALL MASTER")
        self.window.geometry("1100x700")
        self.window.minsize(900, 600)
        self.window.configure(bg=BG_COLOR)

        self.conn = sqlite3.connect("football.db")
        self.cursor = self.conn.cursor()

        self.create_database()
        self.create_sidebar()
        self.create_main_area()

        self.show_page("DASHBOARD")

        self.window.protocol("WM_DELETE_WINDOW", self.close_program)

    # ==============================
    # 데이터베이스
    # ==============================

    def create_database(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            league TEXT,
            home_team TEXT,
            away_team TEXT,
            home_score INTEGER,
            away_score INTEGER
        )
        """)
        self.conn.commit()

    def get_matches(self):
        self.cursor.execute(
            "SELECT * FROM matches ORDER BY id DESC"
        )
        return self.cursor.fetchall()

    # ==============================
    # 화면 구성
    # ==============================

    def create_sidebar(self):
        self.sidebar = tk.Frame(
            self.window,
            bg=PANEL_COLOR,
            width=220
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="FOOTBALL\nMASTER",
            bg=PANEL_COLOR,
            fg=GREEN,
            font=("Arial", 22, "bold"),
            justify="left"
        ).pack(anchor="w", padx=20, pady=(35, 35))

        menus = [
            "DASHBOARD",
            "MATCH RECORD",
            "TEAM ANALYSIS",
            "TEAM COMPARE",
            "MATCH PREDICTION",
            "STATISTICS",
            "SETTINGS"
        ]

        for menu in menus:
            tk.Button(
                self.sidebar,
                text=menu,
                bg=PANEL_COLOR,
                fg=WHITE,
                activebackground=GREEN,
                activeforeground=BG_COLOR,
                font=("Arial", 10, "bold"),
                relief="flat",
                anchor="w",
                padx=20,
                pady=13,
                command=lambda m=menu: self.show_page(m)
            ).pack(fill="x", padx=8, pady=2)

    def create_main_area(self):
        self.main_area = tk.Frame(
            self.window,
            bg=BG_COLOR
        )
        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def create_page_title(self, title, description=""):
        tk.Label(
            self.main_area,
            text=title,
            bg=BG_COLOR,
            fg=GREEN,
            font=("Arial", 24, "bold")
        ).pack(anchor="w", padx=30, pady=(25, 5))

        if description:
            tk.Label(
                self.main_area,
                text=description,
                bg=BG_COLOR,
                fg=GRAY,
                font=("Arial", 10)
            ).pack(anchor="w", padx=32, pady=(0, 20))

    # ==============================
    # 메뉴 이동
    # ==============================

    def show_page(self, page):
        self.clear_main_area()

        if page == "DASHBOARD":
            self.show_dashboard()

        elif page == "MATCH RECORD":
            self.show_match_record()

        elif page == "TEAM ANALYSIS":
            self.show_team_analysis()

        elif page == "TEAM COMPARE":
            self.show_team_compare()

        elif page == "MATCH PREDICTION":
            self.show_match_prediction()

        elif page == "STATISTICS":
            self.show_statistics()

        elif page == "SETTINGS":
            self.show_placeholder(
                "SETTINGS",
                "설정 기능은 추후 추가할 예정입니다."
            )

    # ==============================
    # 대시보드
    # ==============================

    def show_dashboard(self):
        self.create_page_title(
            "DASHBOARD",
            "Football match statistics overview"
        )

        matches = self.get_matches()

        teams = set()

        for match in matches:
            teams.add(match[3])
            teams.add(match[4])

        stats_frame = tk.Frame(
            self.main_area,
            bg=BG_COLOR
        )
        stats_frame.pack(fill="x", padx=25, pady=15)

        stats = [
            ("TOTAL MATCHES", len(matches)),
            ("REGISTERED TEAMS", len(teams)),
            ("DATABASE CONNECTED", "YES")
        ]

        for title, value in stats:
            card = tk.Frame(
                stats_frame,
                bg=PANEL_COLOR,
                padx=20,
                pady=20
            )
            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=7
            )

            tk.Label(
                card,
                text=title,
                bg=PANEL_COLOR,
                fg=GRAY,
                font=("Arial", 10, "bold")
            ).pack(anchor="w")

            tk.Label(
                card,
                text=str(value),
                bg=PANEL_COLOR,
                fg=GREEN,
                font=("Arial", 23, "bold")
            ).pack(anchor="w", pady=(10, 0))

        tk.Label(
            self.main_area,
            text="RECENT MATCHES",
            bg=BG_COLOR,
            fg=WHITE,
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=32, pady=(25, 10))

        if not matches:
            tk.Label(
                self.main_area,
                text="등록된 경기 기록이 없습니다.",
                bg=BG_COLOR,
                fg=GRAY
            ).pack(anchor="w", padx=35, pady=10)

        else:
            for match in matches[:3]:
                self.create_match_row(self.main_area, match)

    # ==============================
    # 경기 기록 표시
    # ==============================

    def create_match_row(self, parent, match):
        row = tk.Frame(
            parent,
            bg=PANEL_COLOR,
            padx=15,
            pady=12
        )
        row.pack(fill="x", padx=30, pady=5)

        text = (
            f"{match[1]}   |   "
            f"{match[3]}   "
            f"{match[5]} : {match[6]}   "
            f"{match[4]}"
        )

        tk.Label(
            row,
            text=text,
            bg=PANEL_COLOR,
            fg=WHITE,
            font=("Arial", 11, "bold")
        ).pack(anchor="w")

        tk.Label(
            row,
            text=match[2],
            bg=PANEL_COLOR,
            fg=GRAY,
            font=("Arial", 9)
        ).pack(anchor="w", pady=(5, 0))

    # ==============================
    # 경기 기록 입력
    # ==============================

    def show_match_record(self):
        self.create_page_title(
            "MATCH RECORD",
            "Enter and manage football match results"
        )

        form = tk.Frame(
            self.main_area,
            bg=PANEL_COLOR,
            padx=20,
            pady=15
        )
        form.pack(fill="x", padx=30, pady=10)

        self.entries = {}

        fields = [
            ("date", "경기 날짜"),
            ("league", "리그"),
            ("home", "홈팀"),
            ("away", "원정팀"),
            ("home_score", "홈팀 점수"),
            ("away_score", "원정팀 점수")
        ]

        for index, (key, label_text) in enumerate(fields):
            row = index // 2
            col = index % 2

            field_frame = tk.Frame(
                form,
                bg=PANEL_COLOR
            )
            field_frame.grid(
                row=row,
                column=col,
                sticky="ew",
                padx=10,
                pady=8
            )

            tk.Label(
                field_frame,
                text=label_text,
                bg=PANEL_COLOR,
                fg=WHITE,
                font=("Arial", 10)
            ).pack(anchor="w")

            entry = tk.Entry(
                field_frame,
                bg="#262B26",
                fg=WHITE,
                insertbackground=WHITE,
                relief="flat",
                font=("Arial", 11)
            )
            entry.pack(fill="x", ipady=7, pady=5)

            self.entries[key] = entry

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        tk.Button(
            form,
            text="SAVE MATCH",
            bg=GREEN,
            fg=BG_COLOR,
            font=("Arial", 11, "bold"),
            relief="flat",
            command=self.save_match
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=12,
            ipady=8
        )

        tk.Label(
            self.main_area,
            text="SAVED MATCHES",
            bg=BG_COLOR,
            fg=WHITE,
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=32, pady=(15, 5))

        self.match_list = tk.Frame(
            self.main_area,
            bg=BG_COLOR
        )
        self.match_list.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        self.refresh_match_list()

    def save_match(self):
        date = self.entries["date"].get().strip()
        league = self.entries["league"].get().strip()
        home = self.entries["home"].get().strip()
        away = self.entries["away"].get().strip()

        home_score_text = self.entries["home_score"].get().strip()
        away_score_text = self.entries["away_score"].get().strip()

        if not all([
            date, league, home, away,
            home_score_text, away_score_text
        ]):
            messagebox.showwarning(
                "입력 오류",
                "모든 항목을 입력해주세요."
            )
            return

        try:
            home_score = int(home_score_text)
            away_score = int(away_score_text)

            if home_score < 0 or away_score < 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "입력 오류",
                "점수는 0 이상의 숫자로 입력해주세요."
            )
            return

        if home.lower() == away.lower():
            messagebox.showwarning(
                "입력 오류",
                "홈팀과 원정팀은 서로 다른 팀이어야 합니다."
            )
            return

        self.cursor.execute("""
        INSERT INTO matches
        (date, league, home_team, away_team, home_score, away_score)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            date,
            league,
            home,
            away,
            home_score,
            away_score
        ))

        self.conn.commit()

        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.refresh_match_list()

        messagebox.showinfo(
            "저장 완료",
            "경기 기록이 저장되었습니다."
        )

    def refresh_match_list(self):
        for widget in self.match_list.winfo_children():
            widget.destroy()

        matches = self.get_matches()

        if not matches:
            tk.Label(
                self.match_list,
                text="등록된 경기 기록이 없습니다.",
                bg=BG_COLOR,
                fg=GRAY
            ).pack(anchor="w", padx=25, pady=10)
            return

        for match in matches:
            self.create_match_row(self.match_list, match)

    # ==============================
    # 팀 통계 계산 공통 기능
    # ==============================

    def get_team_stats(self, team):
        self.cursor.execute("""
        SELECT * FROM matches
        WHERE home_team = ? COLLATE NOCASE
           OR away_team = ? COLLATE NOCASE
        ORDER BY id DESC
        """, (team, team))

        matches = self.cursor.fetchall()

        if not matches:
            return None

        wins = 0
        draws = 0
        losses = 0
        goals_for = 0
        goals_against = 0
        recent_results = []

        for match in matches:
            home_team = match[3]
            away_team = match[4]
            home_score = match[5]
            away_score = match[6]

            if home_team.lower() == team.lower():
                my_score = home_score
                opponent_score = away_score
                opponent = away_team
            else:
                my_score = away_score
                opponent_score = home_score
                opponent = home_team

            goals_for += my_score
            goals_against += opponent_score

            if my_score > opponent_score:
                wins += 1
                result = "WIN"
                color = GREEN

            elif my_score == opponent_score:
                draws += 1
                result = "DRAW"
                color = BLUE

            else:
                losses += 1
                result = "LOSS"
                color = RED

            if len(recent_results) < 5:
                recent_results.append({
                    "date": match[1],
                    "opponent": opponent,
                    "score": f"{my_score} : {opponent_score}",
                    "result": result,
                    "color": color
                })

        total = len(matches)

        return {
            "total": total,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "win_rate": wins / total * 100,
            "avg_goals": goals_for / total,
            "avg_conceded": goals_against / total,
            "recent": recent_results
        }

    # ==============================
    # 팀 분석
    # ==============================

    def show_team_analysis(self):
        self.create_page_title(
            "TEAM ANALYSIS",
            "Analyze team performance using saved match records"
        )

        search_frame = tk.Frame(
            self.main_area,
            bg=PANEL_COLOR,
            padx=20,
            pady=20
        )
        search_frame.pack(fill="x", padx=30, pady=10)

        tk.Label(
            search_frame,
            text="분석할 팀 이름을 입력하세요.",
            bg=PANEL_COLOR,
            fg=WHITE,
            font=("Arial", 11, "bold")
        ).pack(anchor="w")

        input_frame = tk.Frame(
            search_frame,
            bg=PANEL_COLOR
        )
        input_frame.pack(fill="x", pady=(10, 0))

        self.team_entry = tk.Entry(
            input_frame,
            bg="#262B26",
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 12)
        )
        self.team_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9,
            padx=(0, 10)
        )

        self.team_entry.bind(
            "<Return>",
            lambda event: self.analyze_team()
        )

        tk.Button(
            input_frame,
            text="ANALYZE",
            bg=GREEN,
            fg=BG_COLOR,
            font=("Arial", 10, "bold"),
            relief="flat",
            command=self.analyze_team
        ).pack(side="right", ipadx=15, ipady=7)

        self.analysis_result = tk.Frame(
            self.main_area,
            bg=BG_COLOR
        )
        self.analysis_result.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )

        tk.Label(
            self.analysis_result,
            text="팀 이름을 입력하고 ANALYZE 버튼을 눌러주세요.",
            bg=BG_COLOR,
            fg=GRAY
        ).pack(anchor="w", pady=15)

    def analyze_team(self):
        team = self.team_entry.get().strip()

        if not team:
            messagebox.showwarning(
                "입력 오류",
                "분석할 팀 이름을 입력해주세요."
            )
            return

        stats = self.get_team_stats(team)

        for widget in self.analysis_result.winfo_children():
            widget.destroy()

        if not stats:
            tk.Label(
                self.analysis_result,
                text=f"'{team}' 팀의 경기 기록을 찾을 수 없습니다.",
                bg=BG_COLOR,
                fg=RED,
                font=("Arial", 12, "bold")
            ).pack(anchor="w", pady=15)
            return

        tk.Label(
            self.analysis_result,
            text=f"{team}  TEAM STATISTICS",
            bg=BG_COLOR,
            fg=GREEN,
            font=("Arial", 17, "bold")
        ).pack(anchor="w", pady=(0, 15))

        stats_frame = tk.Frame(
            self.analysis_result,
            bg=BG_COLOR
        )
        stats_frame.pack(fill="x", pady=5)

        items = [
            ("MATCHES", stats["total"], WHITE),
            ("WINS", stats["wins"], GREEN),
            ("DRAWS", stats["draws"], BLUE),
            ("LOSSES", stats["losses"], RED)
        ]

        for title, value, color in items:
            card = tk.Frame(
                stats_frame,
                bg=PANEL_COLOR,
                padx=12,
                pady=15
            )
            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=4
            )

            tk.Label(
                card,
                text=title,
                bg=PANEL_COLOR,
                fg=GRAY
            ).pack()

            tk.Label(
                card,
                text=str(value),
                bg=PANEL_COLOR,
                fg=color,
                font=("Arial", 22, "bold")
            ).pack(pady=(7, 0))

        self.create_detail_stats(
            self.analysis_result,
            stats
        )

        self.create_recent_matches(
            self.analysis_result,
            team,
            stats["recent"]
        )

    # ==============================
    # 팀 비교
    # ==============================

    def show_team_compare(self):
        self.create_page_title(
            "TEAM COMPARE",
            "Compare two football teams using match statistics"
        )

        search_frame = tk.Frame(
            self.main_area,
            bg=PANEL_COLOR,
            padx=20,
            pady=20
        )
        search_frame.pack(fill="x", padx=30, pady=10)

        tk.Label(
            search_frame,
            text="비교할 두 팀의 이름을 입력하세요.",
            bg=PANEL_COLOR,
            fg=WHITE,
            font=("Arial", 11, "bold")
        ).pack(anchor="w")

        input_frame = tk.Frame(
            search_frame,
            bg=PANEL_COLOR
        )
        input_frame.pack(fill="x", pady=12)

        self.compare_team1 = tk.Entry(
            input_frame,
            bg="#262B26",
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 11)
        )
        self.compare_team1.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9,
            padx=(0, 8)
        )

        tk.Label(
            input_frame,
            text="VS",
            bg=PANEL_COLOR,
            fg=GREEN,
            font=("Arial", 12, "bold")
        ).pack(side="left", padx=8)

        self.compare_team2 = tk.Entry(
            input_frame,
            bg="#262B26",
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 11)
        )
        self.compare_team2.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9,
            padx=(8, 0)
        )

        tk.Button(
            search_frame,
            text="COMPARE TEAMS",
            bg=GREEN,
            fg=BG_COLOR,
            font=("Arial", 11, "bold"),
            relief="flat",
            command=self.compare_teams
        ).pack(fill="x", ipady=8)

        self.compare_result = tk.Frame(
            self.main_area,
            bg=BG_COLOR
        )
        self.compare_result.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )

        tk.Label(
            self.compare_result,
            text="두 팀의 이름을 입력하고 비교 버튼을 눌러주세요.",
            bg=BG_COLOR,
            fg=GRAY
        ).pack(anchor="w", pady=10)

    def compare_teams(self):
        team1 = self.compare_team1.get().strip()
        team2 = self.compare_team2.get().strip()

        if not team1 or not team2:
            messagebox.showwarning(
                "입력 오류",
                "두 팀의 이름을 모두 입력해주세요."
            )
            return

        if team1.lower() == team2.lower():
            messagebox.showwarning(
                "입력 오류",
                "서로 다른 두 팀을 입력해주세요."
            )
            return

        stats1 = self.get_team_stats(team1)
        stats2 = self.get_team_stats(team2)

        for widget in self.compare_result.winfo_children():
            widget.destroy()

        if not stats1 or not stats2:
            missing = []

            if not stats1:
                missing.append(team1)

            if not stats2:
                missing.append(team2)

            tk.Label(
                self.compare_result,
                text="경기 기록을 찾을 수 없는 팀: " + ", ".join(missing),
                bg=BG_COLOR,
                fg=RED,
                font=("Arial", 11, "bold")
            ).pack(anchor="w", pady=10)
            return

        tk.Label(
            self.compare_result,
            text="TEAM COMPARISON RESULT",
            bg=BG_COLOR,
            fg=GREEN,
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(0, 12))

        cards_frame = tk.Frame(
            self.compare_result,
            bg=BG_COLOR
        )
        cards_frame.pack(fill="x")

        self.create_team_summary(cards_frame, team1, stats1)

        tk.Label(
            cards_frame,
            text="VS",
            bg=BG_COLOR,
            fg=GREEN,
            font=("Arial", 16, "bold")
        ).pack(side="left", padx=10)

        self.create_team_summary(cards_frame, team2, stats2)

        tk.Label(
            self.compare_result,
            text="DETAILED COMPARISON",
            bg=BG_COLOR,
            fg=WHITE,
            font=("Arial", 13, "bold")
        ).pack(anchor="w", pady=(18, 8))

        comparison_frame = tk.Frame(
            self.compare_result,
            bg=PANEL_COLOR,
            padx=15,
            pady=12
        )
        comparison_frame.pack(fill="x")

        comparisons = [
            ("경기 수", "total", "경기"),
            ("승리", "wins", "회"),
            ("무승부", "draws", "회"),
            ("패배", "losses", "회"),
            ("승률", "win_rate", "%"),
            ("평균 득점", "avg_goals", "골"),
            ("평균 실점", "avg_conceded", "골")
        ]

        for label, key, unit in comparisons:
            row = tk.Frame(
                comparison_frame,
                bg=PANEL_COLOR
            )
            row.pack(fill="x", pady=5)

            value1 = stats1[key]
            value2 = stats2[key]

            if key in ("win_rate", "avg_goals", "avg_conceded"):
                if key == "win_rate":
                    text1 = f"{value1:.1f}{unit}"
                    text2 = f"{value2:.1f}{unit}"
                else:
                    text1 = f"{value1:.2f}{unit}"
                    text2 = f"{value2:.2f}{unit}"
            else:
                text1 = f"{value1}{unit}"
                text2 = f"{value2}{unit}"

            if key in ("losses", "avg_conceded"):
                color1 = GREEN if value1 < value2 else (
                    WHITE if value1 == value2 else RED
                )
                color2 = GREEN if value2 < value1 else (
                    WHITE if value1 == value2 else RED
                )
            else:
                color1 = GREEN if value1 > value2 else (
                    WHITE if value1 == value2 else RED
                )
                color2 = GREEN if value2 > value1 else (
                    WHITE if value1 == value2 else RED
                )

            tk.Label(
                row,
                text=text1,
                bg=PANEL_COLOR,
                fg=color1,
                width=12,
                font=("Arial", 10, "bold")
            ).pack(side="left")

            tk.Label(
                row,
                text=label,
                bg=PANEL_COLOR,
                fg=GRAY,
                font=("Arial", 10)
            ).pack(side="left", expand=True)

            tk.Label(
                row,
                text=text2,
                bg=PANEL_COLOR,
                fg=color2,
                width=12,
                font=("Arial", 10, "bold")
            ).pack(side="right")

        recent_frame = tk.Frame(
            self.compare_result,
            bg=BG_COLOR
        )
        recent_frame.pack(fill="x", pady=12)

        tk.Label(
            recent_frame,
            text=f"{team1} 최근 5경기: " +
                 " / ".join(r["result"] for r in stats1["recent"]),
            bg=BG_COLOR,
            fg=GREEN,
            font=("Arial", 9, "bold")
        ).pack(anchor="w", pady=3)

        tk.Label(
            recent_frame,
            text=f"{team2} 최근 5경기: " +
                 " / ".join(r["result"] for r in stats2["recent"]),
            bg=BG_COLOR,
            fg=GREEN,
            font=("Arial", 9, "bold")
        ).pack(anchor="w", pady=3)

        if stats1["win_rate"] > stats2["win_rate"]:
            winner_text = f"{team1}의 승률이 더 높습니다."
        elif stats2["win_rate"] > stats1["win_rate"]:
            winner_text = f"{team2}의 승률이 더 높습니다."
        else:
            winner_text = "두 팀의 승률이 같습니다."

        tk.Label(
            self.compare_result,
            text="RESULT: " + winner_text,
            bg=PANEL_COLOR,
            fg=GREEN,
            font=("Arial", 12, "bold"),
            padx=15,
            pady=12
        ).pack(fill="x", pady=5)

    def create_team_summary(self, parent, team, stats):
        card = tk.Frame(
            parent,
            bg=PANEL_COLOR,
            padx=15,
            pady=12
        )
        card.pack(
            side="left",
            fill="both",
            expand=True
        )

        tk.Label(
            card,
            text=team,
            bg=PANEL_COLOR,
            fg=GREEN,
            font=("Arial", 14, "bold")
        ).pack(anchor="w")

        tk.Label(
            card,
            text=f"승률  {stats['win_rate']:.1f}%",
            bg=PANEL_COLOR,
            fg=WHITE,
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(8, 3))

        tk.Label(
            card,
            text=f"전적  {stats['wins']}승 {stats['draws']}무 {stats['losses']}패",
            bg=PANEL_COLOR,
            fg=GRAY,
            font=("Arial", 9)
        ).pack(anchor="w")

    # ==============================
    # 팀 분석 상세 통계
    # ==============================

    def create_detail_stats(self, parent, stats):
        detail_frame = tk.Frame(
            parent,
            bg=PANEL_COLOR,
            padx=20,
            pady=15
        )
        detail_frame.pack(fill="x", pady=12)

        details = [
            ("WIN RATE", f"{stats['win_rate']:.1f}%"),
            ("AVG. GOALS", f"{stats['avg_goals']:.2f}"),
            ("AVG. CONCEDED", f"{stats['avg_conceded']:.2f}")
        ]

        for title, value in details:
            item = tk.Frame(
                detail_frame,
                bg=PANEL_COLOR
            )
            item.pack(
                side="left",
                fill="both",
                expand=True
            )

            tk.Label(
                item,
                text=title,
                bg=PANEL_COLOR,
                fg=GRAY,
                font=("Arial", 9, "bold")
            ).pack(anchor="w")

            tk.Label(
                item,
                text=value,
                bg=PANEL_COLOR,
                fg=GREEN,
                font=("Arial", 18, "bold")
            ).pack(anchor="w", pady=(5, 0))

    def create_recent_matches(self, parent, team, recent):
        tk.Label(
            parent,
            text="RECENT 5 MATCHES",
            bg=BG_COLOR,
            fg=WHITE,
            font=("Arial", 13, "bold")
        ).pack(anchor="w", pady=(10, 8))

        for match in recent:
            row = tk.Frame(
                parent,
                bg=PANEL_COLOR,
                padx=12,
                pady=9
            )
            row.pack(fill="x", pady=3)

            tk.Label(
                row,
                text=match["date"],
                bg=PANEL_COLOR,
                fg=GRAY,
                font=("Arial", 9)
            ).pack(side="left", padx=(0, 12))

            tk.Label(
                row,
                text=f"{team} {match['score']} {match['opponent']}",
                bg=PANEL_COLOR,
                fg=WHITE,
                font=("Arial", 10, "bold")
            ).pack(side="left")

            tk.Label(
                row,
                text=match["result"],
                bg=PANEL_COLOR,
                fg=match["color"],
                font=("Arial", 9, "bold")
            ).pack(side="right")

    # ==============================
    # 경기 예측
    # ==============================

    def show_match_prediction(self):
        self.create_page_title(
            "MATCH PREDICTION",
            "Estimate match results using saved team statistics"
        )

        input_frame = tk.Frame(
            self.main_area,
            bg=PANEL_COLOR,
            padx=20,
            pady=20
        )
        input_frame.pack(fill="x", padx=30, pady=10)

        tk.Label(
            input_frame,
            text="예측할 두 팀을 입력하세요.",
            bg=PANEL_COLOR,
            fg=WHITE,
            font=("Arial", 11, "bold")
        ).pack(anchor="w")

        teams_frame = tk.Frame(
            input_frame,
            bg=PANEL_COLOR
        )
        teams_frame.pack(fill="x", pady=12)

        self.predict_home = tk.Entry(
            teams_frame,
            bg="#262B26",
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 12)
        )
        self.predict_home.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9,
            padx=(0, 8)
        )

        tk.Label(
            teams_frame,
            text="VS",
            bg=PANEL_COLOR,
            fg=GREEN,
            font=("Arial", 13, "bold")
        ).pack(side="left", padx=8)

        self.predict_away = tk.Entry(
            teams_frame,
            bg="#262B26",
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 12)
        )
        self.predict_away.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9,
            padx=(8, 0)
        )

        tk.Button(
            input_frame,
            text="PREDICT MATCH",
            bg=GREEN,
            fg=BG_COLOR,
            font=("Arial", 11, "bold"),
            relief="flat",
            command=self.predict_match
        ).pack(fill="x", ipady=9)

        self.prediction_result = tk.Frame(
            self.main_area,
            bg=BG_COLOR
        )
        self.prediction_result.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )

        tk.Label(
            self.prediction_result,
            text="두 팀의 이름을 입력하고 예측 버튼을 눌러주세요.",
            bg=BG_COLOR,
            fg=GRAY
        ).pack(anchor="w", pady=10)

    def poisson_probability(self, goals, expected_goals):
        return (
            math.exp(-expected_goals)
            * expected_goals ** goals
            / math.factorial(goals)
        )

    def predict_match(self):
        home = self.predict_home.get().strip()
        away = self.predict_away.get().strip()

        if not home or not away:
            messagebox.showwarning(
                "입력 오류",
                "홈팀과 원정팀을 모두 입력해주세요."
            )
            return

        if home.lower() == away.lower():
            messagebox.showwarning(
                "입력 오류",
                "서로 다른 두 팀을 입력해주세요."
            )
            return

        home_stats = self.get_team_stats(home)
        away_stats = self.get_team_stats(away)

        for widget in self.prediction_result.winfo_children():
            widget.destroy()

        if not home_stats or not away_stats:
            missing = []

            if not home_stats:
                missing.append(home)

            if not away_stats:
                missing.append(away)

            tk.Label(
                self.prediction_result,
                text="경기 기록이 부족한 팀: " + ", ".join(missing),
                bg=BG_COLOR,
                fg=RED,
                font=("Arial", 11, "bold")
            ).pack(anchor="w", pady=10)
            return

        home_expected = (
            home_stats["avg_goals"]
            + away_stats["avg_conceded"]
        ) / 2

        away_expected = (
            away_stats["avg_goals"]
            + home_stats["avg_conceded"]
        ) / 2

        home_expected = max(0.15, min(home_expected, 4.5))
        away_expected = max(0.15, min(away_expected, 4.5))

        home_win = 0
        draw = 0
        away_win = 0
        score_results = []

        for home_goals in range(9):
            for away_goals in range(9):
                probability = (
                    self.poisson_probability(
                        home_goals,
                        home_expected
                    )
                    * self.poisson_probability(
                        away_goals,
                        away_expected
                    )
                )

                score_results.append((
                    home_goals,
                    away_goals,
                    probability
                ))

                if home_goals > away_goals:
                    home_win += probability
                elif home_goals == away_goals:
                    draw += probability
                else:
                    away_win += probability

        total_probability = home_win + draw + away_win

        home_win = home_win / total_probability * 100
        draw = draw / total_probability * 100
        away_win = away_win / total_probability * 100

        best_score = max(
            score_results,
            key=lambda item: item[2]
        )

        predicted_home = best_score[0]
        predicted_away = best_score[1]

        tk.Label(
            self.prediction_result,
            text="PREDICTION RESULT",
            bg=BG_COLOR,
            fg=GREEN,
            font=("Arial", 17, "bold")
        ).pack(anchor="w", pady=(0, 12))

        score_frame = tk.Frame(
            self.prediction_result,
            bg=PANEL_COLOR,
            padx=20,
            pady=18
        )
        score_frame.pack(fill="x", pady=5)

        tk.Label(
            score_frame,
            text="EXPECTED SCORE",
            bg=PANEL_COLOR,
            fg=GRAY,
            font=("Arial", 10, "bold")
        ).pack()

        tk.Label(
            score_frame,
            text=f"{home}   {predicted_home} : {predicted_away}   {away}",
            bg=PANEL_COLOR,
            fg=GREEN,
            font=("Arial", 20, "bold")
        ).pack(pady=12)

        tk.Label(
            score_frame,
            text=(
                f"예상 득점: {home} {home_expected:.2f}골 / "
                f"{away} {away_expected:.2f}골"
            ),
            bg=PANEL_COLOR,
            fg=WHITE,
            font=("Arial", 10)
        ).pack()

        tk.Label(
            self.prediction_result,
            text="WIN / DRAW / LOSS PROBABILITY",
            bg=BG_COLOR,
            fg=WHITE,
            font=("Arial", 13, "bold")
        ).pack(anchor="w", pady=(18, 8))

        probabilities = [
            (home + " WIN", home_win, GREEN),
            ("DRAW", draw, BLUE),
            (away + " WIN", away_win, RED)
        ]

        for title, value, color in probabilities:
            row = tk.Frame(
                self.prediction_result,
                bg=PANEL_COLOR,
                padx=12,
                pady=10
            )
            row.pack(fill="x", pady=4)

            tk.Label(
                row,
                text=title,
                bg=PANEL_COLOR,
                fg=WHITE,
                font=("Arial", 10, "bold"),
                width=18,
                anchor="w"
            ).pack(side="left")

            bar_background = tk.Frame(
                row,
                bg="#303630",
                height=12
            )
            bar_background.pack(
                side="left",
                fill="x",
                expand=True,
                padx=10
            )
            bar_background.pack_propagate(False)

            bar_width = max(1, int(value * 2.2))

            tk.Frame(
                bar_background,
                bg=color,
                width=bar_width,
                height=12
            ).pack(side="left")

            tk.Label(
                row,
                text=f"{value:.1f}%",
                bg=PANEL_COLOR,
                fg=color,
                font=("Arial", 11, "bold"),
                width=8
            ).pack(side="right")

        tk.Label(
            self.prediction_result,
            text=(
                f"분석 데이터: {home_stats['total']}경기 / "
                f"{away_stats['total']}경기"
            ),
            bg=BG_COLOR,
            fg=GRAY,
            font=("Arial", 9)
        ).pack(anchor="w", pady=(12, 3))

        tk.Label(
            self.prediction_result,
            text="※ 과거 경기 기록을 바탕으로 계산한 통계적 추정치입니다.",
            bg=BG_COLOR,
            fg=GRAY,
            font=("Arial", 9)
        ).pack(anchor="w")

    # ==============================
    # 통계 그래프
    # ==============================

    def show_statistics(self):
        self.create_page_title(
            "STATISTICS",
            "Visualize team performance with charts"
        )

        if not MATPLOTLIB_AVAILABLE:
            tk.Label(
                self.main_area,
                text="Matplotlib이 설치되어 있지 않습니다.",
                bg=BG_COLOR,
                fg=RED,
                font=("Arial", 13, "bold")
            ).pack(pady=30)

            tk.Label(
                self.main_area,
                text="터미널에서 아래 명령어를 실행해주세요.",
                bg=BG_COLOR,
                fg=GRAY
            ).pack()

            tk.Label(
                self.main_area,
                text="python -m pip install matplotlib",
                bg=PANEL_COLOR,
                fg=GREEN,
                font=("Consolas", 12, "bold"),
                padx=20,
                pady=15
            ).pack(pady=15)

            return

        matches = self.get_matches()

        teams = set()

        for match in matches:
            teams.add(match[3])
            teams.add(match[4])

        if not teams:
            tk.Label(
                self.main_area,
                text="그래프를 표시할 경기 기록이 없습니다.",
                bg=BG_COLOR,
                fg=GRAY,
                font=("Arial", 12)
            ).pack(pady=50)

            tk.Label(
                self.main_area,
                text="MATCH RECORD에서 경기 결과를 먼저 입력해주세요.",
                bg=BG_COLOR,
                fg=GRAY
            ).pack()

            return

        # 팀별 통계 계산
        team_data = []

        for team in teams:
            stats = self.get_team_stats(team)

            if stats:
                team_data.append((team, stats))

        # 경기 수가 많은 상위 8개 팀 표시
        team_data.sort(
            key=lambda item: item[1]["total"],
            reverse=True
        )
        team_data = team_data[:8]

        team_names = [item[0] for item in team_data]
        win_rates = [
            item[1]["win_rate"] for item in team_data
        ]
        avg_goals = [
            item[1]["avg_goals"] for item in team_data
        ]
        avg_conceded = [
            item[1]["avg_conceded"] for item in team_data
        ]

        # 그래프 생성
        figure = Figure(
            figsize=(9, 5.2),
            dpi=100,
            facecolor=BG_COLOR
        )

        # 승률 그래프
        ax1 = figure.add_subplot(121)
        ax1.set_facecolor(PANEL_COLOR)

        ax1.bar(
            team_names,
            win_rates,
            color=GREEN,
            width=0.6
        )

        ax1.set_title(
            "TEAM WIN RATE",
            color=GREEN,
            fontsize=12,
            fontweight="bold",
            pad=15
        )

        ax1.set_ylabel(
            "Win Rate (%)",
            color=WHITE
        )

        ax1.set_ylim(0, 100)
        ax1.tick_params(
            axis="x",
            colors=WHITE,
            rotation=35,
            labelsize=8
        )
        ax1.tick_params(
            axis="y",
            colors=WHITE,
            labelsize=8
        )

        ax1.grid(
            axis="y",
            alpha=0.2
        )

        for spine in ax1.spines.values():
            spine.set_color(GRAY)

        # 득점과 실점 그래프
        ax2 = figure.add_subplot(122)
        ax2.set_facecolor(PANEL_COLOR)

        x = list(range(len(team_names)))
        width = 0.35

        ax2.bar(
            [i - width / 2 for i in x],
            avg_goals,
            width,
            label="Goals",
            color=GREEN
        )

        ax2.bar(
            [i + width / 2 for i in x],
            avg_conceded,
            width,
            label="Conceded",
            color=RED
        )

        ax2.set_title(
            "AVERAGE GOALS",
            color=GREEN,
            fontsize=12,
            fontweight="bold",
            pad=15
        )

        ax2.set_ylabel(
            "Goals per Match",
            color=WHITE
        )

        ax2.set_xticks(x)
        ax2.set_xticklabels(
            team_names,
            rotation=35,
            ha="right",
            color=WHITE,
            fontsize=8
        )

        ax2.tick_params(
            axis="y",
            colors=WHITE,
            labelsize=8
        )

        ax2.legend(
            facecolor=PANEL_COLOR,
            labelcolor=WHITE,
            fontsize=8
        )

        ax2.grid(
            axis="y",
            alpha=0.2
        )

        for spine in ax2.spines.values():
            spine.set_color(GRAY)

        figure.tight_layout(pad=2)

        # Tkinter 화면에 그래프 표시
        chart_frame = tk.Frame(
            self.main_area,
            bg=BG_COLOR
        )
        chart_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=5
        )

        canvas = FigureCanvasTkAgg(
            figure,
            master=chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        # 그래프 아래 팀 통계 요약
        summary = tk.Frame(
            self.main_area,
            bg=PANEL_COLOR,
            padx=15,
            pady=10
        )
        summary.pack(fill="x", padx=30, pady=(0, 15))

        tk.Label(
            summary,
            text=f"분석 팀 수: {len(team_data)}개",
            bg=PANEL_COLOR,
            fg=GREEN,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        tk.Label(
            summary,
            text="경기 수가 많은 상위 8개 팀을 기준으로 표시합니다.",
            bg=PANEL_COLOR,
            fg=GRAY,
            font=("Arial", 9)
        ).pack(anchor="w", pady=(4, 0))

    # ==============================
    # 준비 중인 메뉴
    # ==============================

    def show_placeholder(self, title, description):
        self.create_page_title(title, description)

        tk.Label(
            self.main_area,
            text="COMING SOON",
            bg=BG_COLOR,
            fg=GREEN,
            font=("Arial", 25, "bold")
        ).pack(pady=100)

    # ==============================
    # 프로그램 종료
    # ==============================

    def close_program(self):
        self.conn.close()
        self.window.destroy()


# ==============================
# 프로그램 실행
# ==============================

if __name__ == "__main__":
    window = tk.Tk()
    app = FootballMaster(window)
    window.mainloop()
