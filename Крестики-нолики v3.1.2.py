def print_board(board):
    display = []
    for i, cell in enumerate(board):
        display.append(str(i) if cell == ' ' else cell)
    for i in range(3):
        print(' | '.join(display[i * 3:(i + 1) * 3]))
        if i < 2:
            print('--+---+--')


def check_winner(board):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    if ' ' not in board:
        return 'draw'
    return None


def minimax(board, player):
    winner = check_winner(board)
    if winner == 'X':
        return {'score': 1}
    elif winner == 'O':
        return {'score': -1}
    elif winner == 'draw':
        return {'score': 0}

    best = {'score': -float('inf')} if player == 'X' else {'score': float('inf')}

    for i in range(9):
        if board[i] == ' ':
            board[i] = player
            result = minimax(board, 'O' if player == 'X' else 'X')
            board[i] = ' '
            result['index'] = i

            if player == 'X' and result['score'] > best['score']:
                best = result
            elif player == 'O' and result['score'] < best['score']:
                best = result

    return best


def player_move(board):
    while True:
        move = input("Введите ход (0-8): ")
        if not move.isdigit():
            print("Введите число от 0 до 8.")
            continue
        move = int(move)
        if move < 0 or move > 8:
            print("Введите число от 0 до 8.")
            continue
        if board[move] != ' ':
            print("Клетка занята.")
            continue
        return move


def main():
    while True:
        print("Новая игра!")
        board = [' '] * 9
        print_board(board)  # Показываем поле сразу после запуска

        while True:
            # Ход игрока
            move = player_move(board)
            board[move] = 'X'

            winner = check_winner(board)
            if winner:
                print_board(board)
                print()
                if winner == 'draw':
                    print("Ничья!")
                else:
                    print("Победил {winner}!")
                break

            # Ход ИИ
            print("Ход ИИ...")
            move = minimax(board, 'O')['index']
            board[move] = 'O'

            print_board(board)
            winner = check_winner(board)
            if winner:
                print()
                if winner == 'draw':
                    print("Ничья!")
                else:
                    print(f"Победил {winner}!")
                break

        answer = input("Хотите сыграть еще раз? (Да/Нет): ").strip().lower()
        if answer != 'да':
            print("Спасибо за игру!")
            break


if __name__ == "__main__":
    main()