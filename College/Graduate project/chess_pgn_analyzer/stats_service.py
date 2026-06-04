from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Game


def get_results_distribution(db: Session) -> dict:
    """
    Возвращает количество побед белых, побед чёрных и ничьих.
    """
    white_wins = db.query(Game).filter(Game.result == "1-0").count()
    black_wins = db.query(Game).filter(Game.result == "0-1").count()
    draws = db.query(Game).filter(Game.result == "1/2-1/2").count()

    return {
        "white_wins": white_wins,
        "black_wins": black_wins,
        "draws": draws,
    }


def get_top_openings(db: Session, limit: int = 5) -> list[dict]:
    """
    Возвращает топ-N самых популярных дебютов.
    """
    results = (
        db.query(Game.opening_name, func.count(Game.opening_name).label("count"))
        .filter(Game.opening_name.isnot(None))
        .group_by(Game.opening_name)
        .order_by(func.count(Game.opening_name).desc())
        .limit(limit)
        .all()
    )

    return [{"opening": row.opening_name, "count": row.count} for row in results]


def get_all_games(db: Session) -> list[Game]:
    """
    Возвращает список всех загруженных партий.
    """
    return db.query(Game).all()


def get_total_count(db: Session) -> int:
    """
    Возвращает общее количество партий в базе.
    """
    return db.query(Game).count()
