from sqlalchemy import Column, Integer, String
from database import Base


class Game(Base):
    """Модель таблицы games в базе данных."""
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    white_player = Column(String, nullable=False, default="Не указано")
    black_player = Column(String, nullable=False, default="Не указано")
    result = Column(String, nullable=False, default="Не указано")
    game_date = Column(String, nullable=True)
    eco_code = Column(String, nullable=True)
    opening_name = Column(String, nullable=True)
    move_count = Column(Integer, nullable=True)
