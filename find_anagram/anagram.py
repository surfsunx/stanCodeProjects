"""
File: anagram.py
Name: Joanne Cho
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

import time                   # This file allows you to calculate the speed of your algorithm

# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
EXIT = '-1'                   # Controls when to stop the loop


def main():
    """
    This program recursively finds all the anagram(s)
    for the word input by user and terminates when the
    input string matches the EXIT constant defined
    at line 19
    """
    start = time.time()
    ####################
    print('Welcome to stanCode \"Anagram Generator\" (or ' + str(EXIT) + ' to quit)')
    (dict_list, char_of_dist_map) = read_dictionary()       # construct two basic dictionary data structures first.
    while True:
        target = input('Find anagram for: ')
        if target == EXIT:
            return 0
        find_anagrams_finder(target, dict_list, char_of_dist_map)
    ####################
    end = time.time()
    print('----------------------------------')
    print(f'The speed of your anagram algorithm: {end-start} seconds.')


def read_dictionary():
    """
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
    with open(FILE, 'r') as f:                  # read words from file
        for line in f:
            tmp_list.append(line.strip())       # build the first basic dict_list data structure

    start = 0
    current_char = 'a'                          # always start form 'a'
    for index in range(len(tmp_list)):          # build the second char_of_dist_map data structure
        if current_char != tmp_list[index][:1]:
            tmp_dict[current_char] = (start, index-1)
            current_char = tmp_list[index][:1]
            start = index

        if index == len(tmp_list)-1:
            tmp_dict[current_char] = (start, index)

    return tmp_list, tmp_dict                   # return as a pair of tuple(immutable)


def find_anagrams_finder(target, dict_list, char_of_dist_map):
    """
    Function: find anagrams of target string

    :param target: User input target string
    :param dict_list: a list contains all vocabularies of file dictionary.txt
    :param char_of_dist_map: a dictionary with {character: (start_index, end_index)} value pair
    :return: None. Show anagrams strings on console
    """
    result_list = []                            # initial two data structures
    target_word_dict = {}
    for c in target:                            # build target_word_dict ds
        if c not in target_word_dict.keys():
            tmp_list = []
            for i in dict_list[char_of_dist_map[c][0]: char_of_dist_map[c][1]+1]:    # 上限不包含
                if len(i) == len(target):
                    tmp_list.append(i)
            target_word_dict[c] = tmp_list

    # do recursive searching
    find_anagrams_helper(target, [], len(target), dict_list, char_of_dist_map, target_word_dict, result_list)

    # show final result
    if result_list:                             # if result_list contains anagrams
        print(f"{len(result_list)} anagrams:  {result_list}")
        result_list.clear()                     # clear two ds
        target_word_dict.clear()
    else:
        print("No anagrams...")


def find_anagrams_helper(s, current_lst, ans_len, dict_list, char_of_dist_map, target_word_dict, result_list):
    """
    Function: a recursive function of finding anagrams of target string

    :param s: User input target string
    :param current_lst: a list of current string
    :param ans_len: length of user input target string
    :param dict_list: a list contains all vocabularies of file dictionary.txt
    :param char_of_dist_map: a dictionary with {character: (start_index, end_index)} value pair
    :param target_word_dict: a dictionary, key is every and each character of target string, value is all vocabularies
            in dict_list with length of target string.
            Example of 'mar':
                {'m': ['mac', 'mad', 'mae', 'mag', 'man', 'map',...],
                 'a': ['aah', 'aal', 'aas', 'aba', 'abo', 'aby', ...],
                 'r': ['rad', 'rag', 'rah', 'raj', 'ram', 'ran', ...]}
    :param result_list: a result list of all anagrams
    :return: None. Show anagrams strings on console
    """
    if len(current_lst) == ans_len:
        tmp = ''.join(current_lst)
        if tmp in target_word_dict[tmp[0]]:
            if tmp not in result_list:
                print("Searching...")
                print(f"Found:  {tmp}")
                result_list.append(tmp)      # append to result_list
    else:
        for c in s:
            # Choose
            current_lst.append(c)
            # Explore
            if has_prefix_helper(''.join(current_lst), dict_list, char_of_dist_map):
                find_anagrams_helper(s.replace(c, "", 1), current_lst, ans_len,
                                     dict_list, char_of_dist_map, target_word_dict, result_list)
            # Un-Choose
            current_lst.pop()


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


def find_anagrams(s):
    """
    :param s:
    :return:
    """
    # the implementation of it is find_anagrams_helper(...)
    pass


def has_prefix(sub_s):
    """
    :param sub_s:
    :return:
    """
    # the implementation of it is has_prefix_helper(...)
    pass


if __name__ == '__main__':
    main()
