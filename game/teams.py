import random
import sqlite3

from typing import List, Tuple


class Teams:
    def __init__(self):
        self.names_list = [
            'Тигры',
            'Монстры',
            'Победители',
            'Зловещие',
            'Убийцы кроликов',
            'Мы - машина',
            'Непоколебимые',
            'Голодные звери',
            'Жаждущие крови',
            'Черная банда',
            'Безумные волки',
            'Дикие львы',
            'Недобрые дела',
            'Монстры с клыками',
            'Древние зомби',
            'Машины - убийцы',
            'Пулемет',
            'Миномет',
            'Сверхточная ракета',
            'Мамонты',
            'Буйволы',
            'Беглые преступники',
            'Сверхзвуковые ракеты',
            'Трансформеры',
            'Каменьщики',
            'Бездушные',
            'Фантастическая двойка',
            'Опять двойка',
            'Черепашки Ниндзя',
            'Халк и его команда',
            'Дубовые',
            'Гном-Гномычи',
            'Гиганты',
            'Гуливеры',
            'Беспощадные',
            'Большие и страшные',
            'Безумный Макс',
            'Мистер Монстр',
            'Бандиты',
            'Крестный отец',
            'Без компромиссов',
            'Кладовщики',
            'Гробовщики',
            'Топчик',
            'Летающая тарелка',
            'Воздушный маршал',
            'Глубоководный горизонт',
            'Синяя молния',
            'Градовая туча',
            'Летающие воины',
            'Вражеский корабль',
            'Витязи',
            'Киборги',
            'Команда Кусто',
            'Пираты',
            'Беспредельщики',
            'Злые',
            'Безумные змеи',
            'Серые львы',
            'Стрелочники',
            'Оружейная банда',
            'Танкисты',
            'Громкие',
            'Молниеносцы',
            'Железный диск',
            'Не робкие',
            'Машина',
            'Камаз',
            'Подводники',
            'Летающий смерч',
            'Горилаз',
        ]
        self.connection = sqlite3.connect("leaderboard.db")
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS used_names(
                name TEXT
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS team(
                players TEXT,
                nameid INTEGER,
                FOREIGN KEY(nameid) REFERENCES used_names(rowid)
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS score(
                score INTEGER,
                teamid INTEGER,
                FOREIGN KEY(teamid) REFERENCES team(rowid)
            );
        ''')
        self.connection.commit()

    def get_name(self) -> Tuple[int, str]:
        name = random.choice(self.names_list)
        res = self.cursor.execute(f'SELECT COUNT(*) FROM used_names WHERE name = "{name}";')
        val = res.fetchone()
        if not val[0]:
            self.cursor.execute(f'INSERT INTO used_names VALUES ("{name}")')
            self.connection.commit()
            team = self.cursor.execute(f'SELECT rowid FROM used_names WHERE name = "{name}";')
            nid = team.fetchone()
            return nid[0], name
        return self.get_name()

    def append_team(self, players: set) -> str:
        nid, name = self.get_name()
        players_str = ':'.join(players)
        self.cursor.execute(f'INSERT INTO team VALUES ("{players_str}", {nid});')
        self.connection.commit()
        return name

    def save_score(self, names: Tuple[str], score: List[int]):
        for i, name in enumerate(names):
            name_score = score[i]
            res = self.cursor.execute(f'''
                SELECT 
                    team.rowid
                FROM 
                    team
                INNER JOIN used_names 
                    ON used_names.rowid = team.nameid
                WHERE
                    used_names.name = "{name}";
            ''')
            rowid = res.fetchone()
            self.cursor.execute(f'INSERT INTO score VALUES ({name_score}, {rowid[0]});')
        self.connection.commit()

    def get_top_teams(self):
        res = self.cursor.execute(f'''
            SELECT
                score.score,
                used_names.name
            FROM 
                used_names
            INNER JOIN team 
                ON used_names.rowid = team.nameid
            INNER JOIN score 
                ON team.rowid = score.teamid
            ORDER BY
                score.score DESC
            LIMIT 0, 4;
        ''')

        return res.fetchall()

    def get_top_accounts(self):
        res = self.cursor.execute(f'''
            SELECT
                score.score,
                used_names.name,
                team.players
            FROM 
                used_names
            INNER JOIN team 
                ON used_names.rowid = team.nameid
            INNER JOIN score 
                ON team.rowid = score.teamid
            ORDER BY
                score.score DESC;
        ''')

        return res.fetchall()
