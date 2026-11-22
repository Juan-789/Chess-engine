import chess
import chess.pgn

from collections.abc import Iterator
from dataclasses import dataclass
from chess.pgn import Game


@dataclass(frozen=True, slots=True)
class PositionSample:
    game_id: str
    ply: str
    fen: str
    rating: int
    move_uci: str

def extract_game(game: Game, game_id: str):
    white_elo = int(game.headers["WhiteElo"])
    black_elo = int(game.headers["BlackElo"])

    board:chess.Board = game.board()

    for ply, move in enumerate(game.mainline_moves(), start=1):
        curr_play = board.turn
             
        rating = (white_elo if curr_play == chess.WHITE else black_elo)

        yield PositionSample(game_id, ply, board.fen(), rating, move.uci())

        board.push(move)


with open("data/sample.pgn", encoding="utf-8") as file:
    game: Game | None = chess.pgn.read_game(file)

    if game is None:
        raise ValueError("No games found")

    if game.errors:
        raise ValueError(f"Invalid game: {game.errors}")

    for sample in extract_game(game, "demo-1"):
        print(sample)
