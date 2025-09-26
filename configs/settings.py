"""
Файл с базовыми настройками и прочей важной штукой
"""

host = "",
database = "",
user = "",
password = ""

# токен получается в @BotFather
TOKEN = ''
# id админов
admins = [0]
# фио людей разбито по 7 человек для удобной навигации
yandex_token = ''

# создает базу данных с id телгерамм, фио и кол-вом посещений/пропусков
db_users_224_config = f"CREATE TABLE users_224 (user_id BIGINT NOT NULL, name TINYTEXT, attendance TINYTEXT, pass TINYTEXT);"
db_attendance_config = f"CREATE TABLE attendance (name TINYTEXT NOT NULL, date TINYTEXT, pair TINYINT, attendance TINYINT, redacted TINYINT);"