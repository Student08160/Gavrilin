import chess.pgn
import io


def parse_pgn_file(file_content: str) -> list[dict]:
    """
    Принимает текстовое содержимое PGN-файла.
    Возвращает список словарей с данными о партиях.
    """
    games = []

    # Создаём текстовый поток из содержимого файла
    pgn_io = io.StringIO(file_content)

    while True:
        # Читаем очередную партию
        game = chess.pgn.read_game(pgn_io)

        # Если партий больше нет — выходим из цикла
        if game is None:
            break

        # Извлекаем заголовки партии
        headers = game.headers

        # Подсчитываем количество ходов
        move_count = 0
        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
            move_count += 1

        # Формируем словарь с данными партии
        game_data = {
            "white_player": headers.get("White", "Не указано"),
            "black_player": headers.get("Black", "Не указано"),
            "result": headers.get("Result", "Не указано"),
            "game_date": headers.get("Date", None),
            "eco_code": headers.get("ECO", None),
            "opening_name": headers.get("Opening", None),
            "move_count": move_count if move_count > 0 else None,
        }

        games.append(game_data)

    return games
