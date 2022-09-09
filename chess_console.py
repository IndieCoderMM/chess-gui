import chess 

def main():
	board = chess.Board()
	

	while not board.is_game_over():
		print('-'*20)
		print(board)
		print('-'*20)

		available_moves = list(board.legal_moves)
		print('Available Moves')
		print('================')
		for i, move in enumerate(available_moves):
			print(f'{i+1}. {board.lan(move)}')
		print()
		turn = 'White' if board.turn == chess.WHITE else 'Black'
		num = input(f'({turn}) Enter move number -> ')
		# Convert to index
		if num.isdigit():
			index = int(num)-1
		# Check for quit
		elif num.lower() == 'q':
			confirm = input('Are you sure you want to quit (y/N)? ')
			if confirm.lower() == 'y':
				print('Quitting the game...')
				return
			else:
				continue
		else:
			print('Invalid Input!')
			continue
		try:
			# Make a Move
			move = available_moves[index]
			board.push(move)
		except IndexError:
			print('Invalid Move! Try another ...')
			continue

	if board.is_checkmate():
		winner = 'WHITE' if board.outcome().winner == chess.WHITE else 'BLACK'
		print('CHECKMATE!!!')
		print('************')
		print(f'{winner} wins by checkmate.')
	else:
		print('DRAW!!!')
		print('********')


if __name__ == '__main__':
	main()