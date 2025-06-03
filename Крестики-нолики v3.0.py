def print_board(board):
    for i in range(3):
        print(' | '.join(board[i*3:(i+1)*3]))
        if i < 2:
            print('--+---+--')

def check_winner(board):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],  
        [0,3,6], [1,4,7], [2,5,8],  
        [0,4,8], [2,4,6]           
    ]
    for line in wins:
        a,b,c = line
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

    if player == 'X':
        best = {'score': -float('inf')}
    else:
        best = {'score': float('inf')}

    for i in range(9):
        if board[i] == ' ':
            board[i] = player
            result = minimax(board, 'O' if player == 'X' else 'X')
            board[i] = ' '
            result['index'] = i

            if player == 'X':
                if result['score'] > best['score']:
                    best = result
            else:
                if result['score'] < best['score']:
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
    board = [' '] * 9
    current_player = 'X'  # Игрок ходит крестиками

    while True:
        print_board(board)
        if current_player == 'X':
            move = player_move(board)
        else:
            print("Ход ИИ...")
            move = minimax(board, 'O')['index']

        board[move] = current_player
        winner = check_winner(board)

        if winner:
            print_board(board)
            if winner == 'draw':
                print("Ничья!")
            else:
                print(f"Победил {winner}!")
            break

        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    main()