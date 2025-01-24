import sqlite3
from datetime import datetime

class StudyTrackerDB:
    def __init__(self, db_name='study_hours.db'):
        self.db_name = db_name
        self._create_tables()

    def _create_tables(self):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS study (
                        date DATE PRIMARY KEY,
                        hours REAL,
                        week INTEGER)''')
            c.execute('''CREATE TABLE IF NOT EXISTS settings (
                        key TEXT PRIMARY KEY,
                        value TEXT)''')
            conn.commit()

    def add_hours(self, hours, date=None):
        date_obj = datetime.strptime(date, '%Y-%m-%d') if date else datetime.now()
        date_str = date_obj.strftime('%Y-%m-%d')
        week = date_obj.isocalendar()[1]

        try:
            hours = float(hours)
        except ValueError:
            raise ValueError("Invalid hours value")

        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            try:
                c.execute('INSERT INTO study VALUES (?, ?, ?)', (date_str, hours, week))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def get_week_total(self, week=None):
        week = week or datetime.now().isocalendar()[1]
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('SELECT SUM(hours) FROM study WHERE week = ?', (week,))
            total = c.fetchone()[0]
            return total if total else 0.0

    def get_history(self):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''SELECT week, 
                        strftime('%Y', date) as year,
                        SUM(hours) 
                        FROM study 
                        GROUP BY year, week
                        ORDER BY year DESC, week DESC''')
            return c.fetchall()

    def get_setting(self, key, default=None):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('SELECT value FROM settings WHERE key = ?', (key,))
            result = c.fetchone()
            return result[0] if result else default

    def save_setting(self, key, value):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('INSERT OR REPLACE INTO settings VALUES (?, ?)', (key, value))
            conn.commit()

    def reset_all_data(self):
        """Elimina todos los registros de estudio"""
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM study')
            conn.commit()