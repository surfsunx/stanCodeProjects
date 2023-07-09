"""
File: boggle.py
Name: Joanne Cho
----------------------------------------
This is a program to solve a 4x4 boggle game
"""

import time

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'
BOGGLE_ROW_COUNT = 4
WORD_LENGTH = BOGGLE_ROW_COUNT
LETTER_LENGTH = BOGGLE_ROW_COUNT + BOGGLE_ROW_COUNT-1
NEIGHBORS = [(-1, -1), (0, -1), (1, -1),
			 (-1,  0),          (1,  0),
			 (-1,  1), (0,  1), (1,  1)]


def main():
	"""
	This is a program to solve a 4x4 boggle game.
	"""
	start = time.time()
	####################
	print('Welcome to stanCode \"Boggle Game\"')
	# 1: construct two basic dictionary data structures first
	(dict_list, char_of_dist_map) = read_dictionary()

	# 2: get user input. put input letters in word_grid
	word_grid = []
	row_counter = 0
	while row_counter < BOGGLE_ROW_COUNT:
		letters = input(f"{row_counter+1} row of letters: ")
		if is_legal_input_letters(letters):
			word_grid.append(letters.replace(" ", "").lower())
			row_counter += 1
		else:
			print("Illegal input")

	# 3: loop every letter, build words
	results = []
	for y in range(len(word_grid)):
		for x in range(len(word_grid[y])):
			build_words(word_grid, word_grid[y][x], "", results, y, x, set([y, x]), dict_list, char_of_dist_map)
	result_set = set(results)

	# 4: show final result
	count = 0
	for w in result_set:
		if w in dict_list:
			count += 1
			print(f"Found \"{w}\"")
	print(f"There are {count} words in total.")
	####################
	end = time.time()
	print('----------------------------------')
	print(f'The speed of your boggle algorithm: {end - start} seconds.')


def build_words(grid, current_letter, current_s, result_list, y, x, used, dict_list, char_of_dist_map):
	"""
	Function: Build words

	:param grid: user input boggle-game matrix
	:param current_letter: current letter in grid
	:param current_s: current string
	:param result_list: result list
	:param y: coordinate of y
	:param x: coordinate of x
	:param used: (y, x) has been visited
	:param dict_list: dict_list is a list contains all vocabularies of file dictionary.txt
	:param char_of_dist_map: char_of_dist_map is a dictionary.
	:return result_list: a list contains result
	"""
	if len(current_s) >= WORD_LENGTH:
		result_list.append(current_s)

	if has_prefix_helper(current_s, dict_list, char_of_dist_map):
		for dx, dy in NEIGHBORS:
			nx, ny = x + dx, y + dy
			if is_in_boundary(grid, ny, nx) and (ny, nx) not in used:
				current_s += grid[ny][nx]					# choose
				used.add((ny, nx))
				build_words(grid, grid[ny][nx], current_s, result_list, ny, nx, used, dict_list, char_of_dist_map)
				used.remove((ny, nx))                       # un-choose
				current_s = current_s[:len(current_s)-1]


def is_in_boundary(board, y, x) -> bool:
	"""
	Function: check whether dy and dx is within boundary

	:param board: user input boggle-game matrix
    :param y: coordinate of y
    :param x: coordinate of x
	:return True: y, x is within boundary
			False: y, x is out of boundary
	"""
	return 0 <= y < len(board) and 0 <= x < len(board[y])


def is_legal_input_letters(tmp:str) -> bool:
	"""
	Function: check string length

	:param: None
	:return True: string length is valid
			False: string length is invalid
	"""
	if len(tmp) == LETTER_LENGTH:
		for i in range(1, len(tmp), 2):
			if tmp[i] == ' ':
				pass
			else:
				return False
		if tmp.replace(" ", "").lower().isalpha():
			return True
	else:
		return False


def read_dictionary():
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list

	Function: construct two basic dictionary data structures
	:param: None
	:return tmp_list: dict_list is a list contains all vocabularies of file dictionary.txt
			tmp_dict: char_of_dist_map is a dictionary.
			- Key is a single character.
			- Value is a pair of tuple, indicates two indexes of start and end vocabularies the key character in dict_list
		   	-  For example: {'a': (0, 7151), 'b': (7152, 14528), 'c': (14529, 26318), 'd': (26319, 34131),...}
	"""
	tmp_list = []
	tmp_dict = {}
	with open(FILE, 'r') as f:  # read words from file
		for line in f:
			if len(line) >= WORD_LENGTH:
				tmp_list.append(line.strip())  # build the first basic dict_list data structure

	start = 0
	current_char = 'a'  # always start form 'a'
	for index in range(len(tmp_list)):  # build the second char_of_dist_map data structure
		if current_char != tmp_list[index][:1]:
			tmp_dict[current_char] = (start, index - 1)
			current_char = tmp_list[index][:1]
			start = index

		if index == len(tmp_list) - 1:
			tmp_dict[current_char] = (start, index)

	return tmp_list, tmp_dict  # return as a pair of tuple(immutable)


def has_prefix_helper(sub_s, dict_list, char_of_dist_map):
    """
    Function: Find if dict_list contains a sub string

    :param sub_s: a sub-string of target
    :param dict_list: a list contains all vocabularies of file dictionary.txt
    :param char_of_dist_map: a dictionary with {character: (start_index, end_index)} value pair
    :return True: the sub-string is in dict_list
            False: the sub-string is Not in dict_list
    """
    if len(sub_s) > 1:
        for word in dict_list[char_of_dist_map[sub_s[0]][0]:char_of_dist_map[sub_s[0]][1]+1]:  # 上限不包含
            if word.startswith(sub_s):
                return True
        return False
    else:
        return True


def has_prefix(sub_s):
	"""
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	# the implementation of it is has_prefix_helper(...)
	pass


if __name__ == '__main__':
	main()
