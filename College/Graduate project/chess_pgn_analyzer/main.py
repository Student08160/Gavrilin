from fastapi import FastAPI, File, UploadFile, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import database
import models
from pgn_parser import parse_pgn_file
from stats_service import (
    get_results_distribution,
    get_top_openings,
    get_all_games,
    get_total_count,
)

# Создаём приложение
app = FastAPI()

# Подключаем папку со статическими файлами (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем папку с HTML-шаблонами
templates = Jinja2Templates(directory="templates")

# Создаём таблицы в базе данных при запуске
models.Base.metadata.create_all(bind=database.engine)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(database.get_db)):
    """Главная страница — показывает статистику."""

    total = get_total_count(db)

    if total > 0:
        distribution = get_results_distribution(db)
        top_openings = get_top_openings(db)
        all_games = get_all_games(db)
    else:
        distribution = {"white_wins": 0, "black_wins": 0, "draws": 0}
        top_openings = []
        all_games = []

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "total": total,
            "distribution": distribution,
            "top_openings": top_openings,
            "all_games": all_games,
            "message": None,
            "error": None,
        }
    )


@app.post("/upload", response_class=HTMLResponse)
async def upload_pgn(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
):
    """Обработка загрузки PGN-файла."""

    error = None
    message = None

    # Проверка расширения файла
    if not file.filename.endswith(".pgn"):
        error = "Ошибка: файл должен иметь расширение .pgn"
    else:
        # Читаем содержимое файла
        content_bytes = await file.read()

        # Проверка на пустой файл
        if len(content_bytes) == 0:
            error = "Ошибка: файл пустой"
        else:
            try:
                # Декодируем содержимое
                content_str = content_bytes.decode("utf-8")

                # Парсим партии
                games_data = parse_pgn_file(content_str)

                if len(games_data) == 0:
                    error = "Ошибка: файл не содержит шахматных партий"
                else:
                    # Очищаем старые данные перед новой загрузкой
                    db.query(models.Game).delete()
                    db.commit()

                    # Сохраняем новые партии в базу
                    for game_data in games_data:
                        game = models.Game(**game_data)
                        db.add(game)
                    db.commit()

                    message = f"Успешно загружено {len(games_data)} партий!"

            except Exception as e:
                error = f"Ошибка при обработке файла: {str(e)}"

    # Получаем статистику для отображения
    total = get_total_count(db)

    if total > 0:
        distribution = get_results_distribution(db)
        top_openings = get_top_openings(db)
        all_games = get_all_games(db)
    else:
        distribution = {"white_wins": 0, "black_wins": 0, "draws": 0}
        top_openings = []
        all_games = []

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "total": total,
            "distribution": distribution,
            "top_openings": top_openings,
            "all_games": all_games,
            "message": message,
            "error": error,
        }
    )


@app.post("/clear", response_class=HTMLResponse)
async def clear_data(
    request: Request,
    db: Session = Depends(database.get_db),
):
    """Очистка всех данных из базы."""

    db.query(models.Game).delete()
    db.commit()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "total": 0,
            "distribution": {"white_wins": 0, "black_wins": 0, "draws": 0},
            "top_openings": [],
            "all_games": [],
            "message": "Данные успешно очищены.",
            "error": None,
        }
    )
