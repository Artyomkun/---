import time
import random
import threading
from copy import deepcopy

print_lock = threading.Lock()
results_lock = threading.Lock()
results = {}

def print_board(board, show_indices=False):
    def cell_repr(i):
        return str(i) if show_indices and board[i] == ' ' else board[i]

    rows = []
    for i in range(3):
        row = [cell_repr(i * 3 + j) for j in range(3)]
        rows.append(" " + " | ".join(row))
    return "\n---+---+---\n".join(rows)

def check_winner(board):
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for i, j, k in wins:
        if board[i] == board[j] == board[k] and board[i] != ' ':
            return board[i]
    if ' ' not in board:
        return 'Draw'
    return None

def get_empty_cells(board):
    return [i for i, cell in enumerate(board) if cell == ' ']

def minimax(board, depth, alpha, beta, is_max, ai, human):
    winner = check_winner(board)
    if winner == ai:
        return 10 - depth
    if winner == human:
        return depth - 10
    if winner == 'Draw':
        return 0

    if is_max:
        max_eval = -float('inf')
        for cell in get_empty_cells(board):
            board[cell] = ai
            eval = minimax(board, depth + 1, alpha, beta, False, ai, human)
            board[cell] = ' '
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for cell in get_empty_cells(board):
            board[cell] = human
            eval = minimax(board, depth + 1, alpha, beta, True, ai, human)
            board[cell] = ' '
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def ai_move(board, symbol, difficulty, human_symbol):
    empty = get_empty_cells(board)
    if not empty:
        return None
    if difficulty == "easy":
        return random.choice(empty)
    if difficulty == "medium" and random.random() < 0.5:
        return random.choice(empty)

    best_score = -float('inf')
    best_move = None
    for cell in empty:
        board[cell] = symbol
        score = minimax(board, 0, -float('inf'), float('inf'), False, symbol, human_symbol)
        board[cell] = ' '
        if score > best_score:
            best_score = score
            best_move = cell
    return best_move

def human_move(board, symbol, game_id):
    while True:
        try:
            with print_lock:
                print(f"[Игра #{game_id}] Текущая доска:")
                print(print_board(board, show_indices=True))
                print(f"[Игра #{game_id}] Игрок {symbol}, введите ход (0-8): ")
            move = int(input().strip())
            if 0 <= move <= 8 and board[move] == ' ':
                return move
            else:
                with print_lock:
                    print(f"[Игра #{game_id}] Неверный ход. Клетка занята или номер вне диапазона.")
        except ValueError:
            with print_lock:
                print(f"[Игра #{game_id}] Введите число от 0 до 8.")

def play_game(game_id, mode, delay, difficulty, human_symbol):
    try:
        board = [' '] * 9
        current = 'X'
        move_count = 0
        ai_symbol = 'O' if human_symbol == 'X' else 'X'

        with print_lock:
            print(f"\n[Игра #{game_id} началась | Режим: {mode} | Сложность: {difficulty}]")

        while True:
            if mode == "human_vs_human":
                move = human_move(board, current, game_id)
            elif mode == "human_vs_ai" and current == human_symbol:
                move = human_move(board, current, game_id)
            else:
                move = ai_move(board, current, difficulty, human_symbol if mode != 'ai_vs_ai' else ('O' if current == 'X' else 'X'))
            with print_lock:
                    print(f"[Игра #{game_id}] ИИ ({current}) ходит на {move}")
            if move is None:
                with print_lock:
                    print(f"[Игра #{game_id}] Нет доступных ходов.")
                break

            board[move] = current
            move_count += 1

            with print_lock:
                print(f"[Игра #{game_id}] Ход #{move_count}: {current} на {move}")
                print(print_board(board))

            winner = check_winner(board)
            if winner:
                with print_lock:
                    result_text = "Ничья" if winner == 'Draw' else f"{winner} победил"
                    print(f"[Игра #{game_id}] Игра окончена: {result_text}")
                    print(f"[Игра #{game_id}] Финальная доска:\n{print_board(board)}")
                with results_lock:
                    results[game_id] = result_text
                break

            current = 'O' if current == 'X' else 'X'
            time.sleep(delay)
    except Exception as e:
        with print_lock:
            print(f"[Игра #{game_id}] Ошибка: {e}")
        with results_lock:
            results[game_id] = f"Ошибка: {e}"

def start_games(mode, num_games, delay, difficulty, human_symbol):
    threads = []
    for i in range(num_games):
        thread = threading.Thread(
            target=play_game,
            args=(i + 1, mode, delay, difficulty, human_symbol)
        )
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

    with print_lock:
        print("\n=== Результаты игр ===")
        for game_id in sorted(results):
            print(f"Игра #{game_id}: {results[game_id]}")
        print("====================")

def main():
    try:
        while True:
            print("Выберите режим игры:")
            print("1. Человек против человека")
            print("2. Человек против ИИ")
            print("3. ИИ против ИИ")
            while True:
                mode_input = input("Введите номер режима (1-3): ").strip()
                mode_map = {
                    "1": "human_vs_human",
                    "2": "human_vs_ai",
                    "3": "ai_vs_ai"
                }
                if mode_input in mode_map:
                    mode = mode_map[mode_input]
                    break
                print("Ошибка: Введите число от 1 до 3.")

            print("Выберите уровень сложности:")
            print("1. Легкий")
            print("2. Средний")
            print("3. Сложный")
            while True:
                difficulty_input = input("Введите номер сложности (1-3): ").strip()
                difficulty_map = {
                    "1": "easy",
                    "2": "medium",
                    "3": "hard"
                }
                if difficulty_input in difficulty_map:
                    difficulty = difficulty_map[difficulty_input]
                    break
                print("Ошибка: Введите число от 1 до 3.")

            while True:
                num_games = input("Сколько игр запустить параллельно: ").strip()
                if num_games.isdigit() and int(num_games) > 0:
                    num_games = int(num_games)
                    break
                print("Ошибка: Введите положительное число.")

            while True:
                delay = input("Задержка между ходами (в секундах): ").strip()
                try:
                    delay = float(delay)
                    if delay >= 0:
                        break
                    print("Ошибка: Задержка не может быть отрицательной.")
                except ValueError:
                    print("Ошибка: Введите корректное число.")

            human_symbol = None
            if mode == "human_vs_ai":
                while True:
                    human_symbol = input("Выберите символ (X или O): ").strip().upper()
                    if human_symbol in ['X', 'O']:
                        break
                    print("Ошибка: Введите X или O.")
            else:
                human_symbol = 'X'

            start_games(mode, num_games, delay, difficulty, human_symbol)

            print("\n=== Все игры завершены ===")
            answer = input("Нажмите Enter чтобы выйти, или введите 'да' чтобы сыграть еще раз, 'нет' чтобы закрыть: ").strip().lower()

            if answer == '':
                print("Выход из программы...")
                break
            elif answer == 'да':
                print("Перезапуск игр...")
                continue
            elif answer == 'нет':
                print("Выход из программы...")
                break
            else:
                print("Неизвестный ответ, повторите ввод.")

    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"Ошибка ввода: {e}. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()
