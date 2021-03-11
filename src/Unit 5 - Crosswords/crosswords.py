import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import re
import time

all_words_grouped_by_len = None
word_lookup_table = None
all_words = None

def main():
    global all_words_grouped_by_len, word_lookup_table, all_words
    height = 0
    width = 0
    num_block_squares = 0
    dictionary_filename = None
    crossword = ""
    seed_strings = []

    for i in args:
        if re.match('^\d+x\d+$', i):
            nums = i.split('x')
            height = int(nums[0])
            width = int(nums[1])
        elif re.match('^\d+$', i):
            num_block_squares = int(i)
        elif re.match('^\w+\.txt$', i):
            dictionary_filename = i
        elif re.match('^(h|v)\d+x\d+(\w|#)*$', i, re.IGNORECASE):
            seed_strings.append(i)
            pass
    
    crossword = (height * width) * '-'

    for seed in seed_strings:
        orientation = seed[0]
        loc = re.findall('\d+', seed)
        v_offset = int(loc[0])
        h_offset = int(loc[1])
        
        word = re.split('\d+', seed)[-1]
        
        if not word or len(re.split('\d+', seed)) == 2:
            word = '#'

        word = word.lower()
        start_pos = v_offset * width + h_offset
        
        if orientation.lower() == 'h':
            crossword = crossword[:start_pos] + word + crossword[start_pos + len(word):]
        else:
            curr_pos = start_pos

            for i in range(len(word)):
                crossword = crossword[:curr_pos] + word[i] + crossword[curr_pos + 1:]
                curr_pos += width

    if num_block_squares == height * width:
        # special case
        print(num_block_squares * '#')

    else:
        # normal case

        # enforce 180 degree symmetry on input board
        final_crossword = rotate_180_entire(crossword, height, width)

        # validate the input board
        if not is_valid(final_crossword, height, width):
            final_crossword = fix_invalid_board(final_crossword, height, width)

        # add blocking squares to the input board
        final_crossword = add_blocking_squares(final_crossword, height, width, num_block_squares)
        
        # read words from dictionary and create lookup tables
        # all_words_grouped_by_len - {len_of_word : {set_of_words}}
        # word_lookup_table - { letter : { position_in_word : { len_of_word : {set_of_words} } } }
        all_words_grouped_by_len, word_lookup_table, all_words = read_from_dictionary(dictionary_filename, height, width)

        # pretty-print the final result
        # for i in range(height):
        #     for j in range(width):
        #         print(final_crossword[i * width + j], end=' ')
        #     print()
        # print()

        # s = time.time()
        # for i in range(1000):
        final_crossword = fill_in_words(final_crossword, height, width)
        # print(time.time() - s)

        for i in range(height):
            for j in range(width):
                print(final_crossword[i * width + j], end=' ')
            print()
        print()

def fix_invalid_board(crossword, height, width):
    new_crossword = crossword

    while True:
        new_crossword = check_for_isolated_regions(new_crossword, height, width, fill_isolated_regions=True)
        
        ret = check_small_areas(new_crossword, height, width, return_info_to_fix=True)
        if ret[0]:
            break

        pos = ret[2]

        # fix the invalid board by filling in the small areas
        # find the bounds of where to fill in, and fill it in from there

        if ret[1] == 'H':
            # max of the closest # from the left of pos and the left edge of the board

            left_bound = pos

            while left_bound % width > 0 and new_crossword[left_bound] != '#':
                left_bound -= 1

            right_bound = pos

            while right_bound % width < width - 1 and new_crossword[right_bound] != '#':
                right_bound += 1
            
            for h_pos in range(left_bound, right_bound + 1):
                new_crossword = new_crossword[:h_pos] + '#' + new_crossword[h_pos + 1:]

            new_crossword = rotate_180_entire(new_crossword, height, width)

        else:
            
            # NOTE: LOWER_BOUND IS ALWAYS GREATER THAN UPPER_BOUND

            upper_bound = pos

            while upper_bound // width > 0 and new_crossword[upper_bound] != '#':
                upper_bound -= width

            lower_bound = pos

            while lower_bound // width < height - 1 and new_crossword[lower_bound] != '#':
                lower_bound += width
            
            for v_pos in range(upper_bound, lower_bound + 1, width):
                new_crossword = new_crossword[:v_pos] + '#' + new_crossword[v_pos + 1:]

            new_crossword = rotate_180_entire(new_crossword, height, width)

    return new_crossword
    
# returns True if there are no isolated regions (everything is connected and valid from that angle), and False if there are isolated regions
def check_for_isolated_regions(crossword, height, width, fill_isolated_regions=False):
    start = crossword.find('-')

    if start == -1:
        for i in range(len(crossword)):
            if crossword[i] != '#':
                start = i
                break
        else:
            # the board is only blocking squares
            return True

    filled_crossword = flood_fill(crossword, start // width, start % width, height, width)

    if fill_isolated_regions and '-' in filled_crossword:

        while True:

            master_filled_crossword = filled_crossword
            last_filled_crossword = filled_crossword
            regions_to_fill = set()
            regions_to_fill.add(last_filled_crossword)
            reset_pos_list = []

            while '-' in master_filled_crossword:
                reset_pos_list += [i for i in range(len(last_filled_crossword)) if last_filled_crossword[i] == '*'] # reset these positions to - before adding last_filled_crossword to regions_to_fill

                start = master_filled_crossword.find('-')
                master_filled_crossword = flood_fill(master_filled_crossword, start // width, start % width, height, width)

                last_filled_crossword = master_filled_crossword

                for i in reset_pos_list:
                    last_filled_crossword = last_filled_crossword[:i] + '-' + last_filled_crossword[i + 1:]
                
                regions_to_fill.add(last_filled_crossword)

            regions_to_fill = {i for i in regions_to_fill if '*' in i}

            num_squares_to_change_list = {xword.count('*') : xword for xword in regions_to_fill}
            smallest_change = min(num_squares_to_change_list)

            filled_crossword = num_squares_to_change_list[smallest_change].replace('*', '#')

            if check_for_isolated_regions(filled_crossword, height, width):
                break
        
        ret_crossword = crossword
        block_squares_list = [i for i in range(len(filled_crossword)) if filled_crossword[i] == '#']

        for i in block_squares_list:
            ret_crossword = ret_crossword[:i] + '#' + ret_crossword[i + 1:]

        return ret_crossword

        # check for the first _ and have start for flood fill be there

    if '-' in filled_crossword:
        return False
    else:
        if fill_isolated_regions:
            return crossword
        return True

def flood_fill(crossword, i, j, height, width):
    # i is the vertical displacement and j is horizontal
    pos = i * width + j
    if i >= height or j >= width or i < 0 or j < 0 or crossword[pos] == '#' or crossword[pos] == '*':
        return crossword

    new_crossword = crossword[:pos] + '*' + crossword[pos + 1:]

    new_crossword = flood_fill(new_crossword, i + 1, j, height, width)
    new_crossword = flood_fill(new_crossword, i, j + 1, height, width)
    new_crossword = flood_fill(new_crossword, i - 1, j, height, width)
    new_crossword = flood_fill(new_crossword, i, j - 1, height, width)
    
    return new_crossword

# returns [if return_info_to_fix: (True, None, None) else True] if the crossword has no small areas and is valid from that angle
# else if return_info_to_fix == True: returns (False, orientation, index) where orientation is 'H' or 'V' and index is the pos which fails the test

def check_small_areas(crossword, height, width, return_info_to_fix=False):
    for i in range(len(crossword)):
        if crossword[i] != '#':
            # check horizontal

            cases = set()

            if i % width < width - 2:
                cases.add(crossword[i] + crossword[i + 1] + crossword[i + 2])
            
            if 0 < i % width < width - 1:
                cases.add(crossword[i - 1] + crossword[i] + crossword[i + 1])

            if i % width > 1:
                cases.add(crossword[i - 2] + crossword[i - 1] + crossword[i])

            for triad in cases:
                if '#' not in triad:
                    break
            else:
                if return_info_to_fix:
                    return False, 'H', i
                return False

            # check vertical

            cases = set()

            if i // width < height - 2:
                cases.add(crossword[i] + crossword[i + width] + crossword[i + 2 * width])
            
            if 0 < i // width < height - 1:
                cases.add(crossword[i - width] + crossword[i] + crossword[i + width])

            if i // width > 1:
                cases.add(crossword[i - 2 * width] + crossword[i - width] + crossword[i])

            for triad in cases:
                if '#' not in triad:
                    break
            else:
                if return_info_to_fix:
                    return False, 'V', i
                return False

    if return_info_to_fix:
        return True, None, None
    return True

# returns the 180 degree rotation transposed onto crossword

def rotate_180_entire(crossword, height, width):
    temp_h = height
    temp_w = width
    temp_board = crossword

    # 180 degree rotation (2 90-degree right rotations)

    for i in range(2):
        raw_clock_90 = [[i * temp_w + j for i in range(temp_h)][::-1] for j in range(temp_w)] 
        clock_90 = []

        for i in raw_clock_90:
            clock_90 += i

        temp_board = ''.join([temp_board[clock_90[i]] for i in range(len(temp_board))])

        temp_h, temp_w = temp_w, temp_h

    final_crossword = crossword

    for i in range(len(temp_board)):
        if temp_board[i] == '#':
            final_crossword = final_crossword[:i] + '#' + final_crossword[i + 1:]


    return final_crossword

# returns the position which is 180 degrees rotated from the original position

def rotate_180_pos(pos, height, width):
    return (height * width - 1) - pos

def is_valid(crossword, height, width):
    return check_small_areas(crossword, height, width) and check_for_isolated_regions(crossword, height, width)

def add_blocking_squares(raw_crossword, height, width, target_num_squares):
    crossword = raw_crossword

    if not is_valid(crossword, height, width):
        if target_num_squares - crossword.count('#') < 30:
            return ''
        else:
            crossword = fix_invalid_board(crossword, height, width)

    if crossword.count('#') == target_num_squares:
        return crossword
    elif crossword.count('#') > target_num_squares:
        return ''

    set_of_choices = {i : set() for i in range(100)}

    for i in range(len(crossword)):
        if crossword[i] == '-':
            total_spaces = 0
            temp = i - 1
            temp_spaces = 0

            # left
            while temp % width < width - 1 and crossword[temp] != '#':
                temp -= 1
                temp_spaces += 1

            if temp_spaces < 3: # protection against adjacent blocking squares
                total_spaces += 15

            total_spaces += temp_spaces
            temp_spaces = 0

            # right
            temp = i + 1
            while temp % width > 0 and crossword[temp] != '#':
                temp += 1
                temp_spaces += 1

            if temp_spaces < 3: # protection against adjacent blocking squares
                total_spaces += 15

            total_spaces += temp_spaces
            temp_spaces = 0

            # up
            temp = i - width
            while temp // width > -1 and crossword[temp] != '#':
                temp -= width
                temp_spaces += 1

            if temp_spaces < 3: # protection against adjacent blocking squares
                total_spaces += 15

            total_spaces += temp_spaces
            temp_spaces = 0

            # down
            temp = i + width
            while temp // width < height and crossword[temp] != '#':
                temp += width
                temp_spaces += 1

            if temp_spaces < 3: # protection against adjacent blocking squares
                total_spaces += 15

            total_spaces += temp_spaces
            temp_spaces = 0

            set_of_choices[total_spaces].add(i)
            
    for choice_set in set_of_choices:
        for choice in set_of_choices[choice_set]:
            new_xword = crossword[:choice] + '#' + crossword[choice + 1:]
            new_pos = rotate_180_pos(choice, height, width)

            if crossword[new_pos] != '-':
                continue

            new_xword = new_xword[:new_pos] + '#' + new_xword[new_pos + 1:]
            ret = add_blocking_squares(new_xword, height, width, target_num_squares)
            if ret:
                return ret

    return ''


def read_from_dictionary(filename, height, width): #if word bigger than max(height, width) dont add
    # for adding words, go through each set in set[letter][position] for all letters and positions and find intersection
    word_list = open(filename, 'r').readlines()
    all_words_grouped_by_len = {} # {len_of_word : {set_of_words}}
    word_lookup_table = {} # { letter : { position_in_word : { len_of_word : {set_of_words} } } }
    all_words = set()
    max_len = max(height, width)

    for word in word_list:
        word = word.strip()

        if 3 <= len(word) <= max_len:
            # add to all_words
            all_words.add(word)
            
            # add to all_words_grouped_by_len
            if len(word) not in all_words_grouped_by_len:
                all_words_grouped_by_len[len(word)] = set()
            
            all_words_grouped_by_len[len(word)].add(word)

            # add to lookup table
            for letter_pos in range(len(word)):
                letter = word[letter_pos]

                if letter not in word_lookup_table:
                    word_lookup_table[letter] = {}
                if letter_pos not in word_lookup_table[letter]:
                    word_lookup_table[letter][letter_pos] = {}
                if len(word) not in word_lookup_table[letter][letter_pos]:
                    word_lookup_table[letter][letter_pos][len(word)] = set()

                word_lookup_table[letter][letter_pos][len(word)].add(word)

    return all_words_grouped_by_len, word_lookup_table, all_words

def is_invalid(crossword, height, width):
    horizontal_words =  {i * width + j + 1 for i in range(height) for j in range(width - 1) \
        if crossword[i * width + j] == '#' and crossword[i * width + j + 1] != '#'} | \
        {i * width for i in range(height) if crossword[i * width] != '#'}
    
    vertical_words = set()

    for i in range(width):
        col = [(crossword[j], j) for j in range(i, height * width, width)]
        if col[0][0] != '#':
            vertical_words.add(col[0][1])

        for j in range(len(col) - 1):
            if col[j][0] == '#' and col[j + 1][0] != '#':
                vertical_words.add(col[j + 1][1])

    for i in horizontal_words:
        end = i + width - i % width
        
        if '#' in crossword[i:end]:
            end = crossword.index('#', i)

        spaces = crossword[i:end].count('-')

        if spaces == 0 and crossword[i:end] not in all_words:
            return True

    for i in vertical_words:
        end = i

        while end // width < width and crossword[end] != '#':
            end += width

        end -= (width - 1)
        col = [crossword[j] for j in range(i, end, width)]
        spaces = col.count('-')

        if spaces == 0 and ''.join(col) not in all_words:
            return True

    return False

def is_solved(crossword):
    return '-' not in crossword

def fill_in_words(raw_crossword, height, width):
    crossword = raw_crossword
    
    # if is_invalid(crossword, height, width):
    #     return ''
    if is_solved(crossword):
        return crossword

    words_in_xword = set()

    # create and order set of choices

    set_of_choices = {i : set() for i in range(1, 50)} # { num_spaces : set("start_pos + end_pos + orientation (H/V)") }

    horizontal_words =  {i * width + j + 1 for i in range(height) for j in range(width - 1) \
        if crossword[i * width + j] == '#' and crossword[i * width + j + 1] != '#'} | \
        {i * width for i in range(height) if crossword[i * width] != '#'}
    
    vertical_words = set()

    for i in range(width):
        col = [(crossword[j], j) for j in range(i, height * width, width)]
        if col[0][0] != '#':
            vertical_words.add(col[0][1])

        for j in range(len(col) - 1):
            if col[j][0] == '#' and col[j + 1][0] != '#':
                vertical_words.add(col[j + 1][1])

    for i in horizontal_words:
        end = i + width - i % width
        
        if '#' in crossword[i:end]:
            end = crossword.index('#', i)

        spaces = crossword[i:end].count('-')

        if spaces > 0:
            set_of_choices[spaces].add(str(i) + ' ' + str(end) + ' H')
        else:
            words_in_xword.add(crossword[i:end])

    for i in vertical_words:
        end = i

        while end // width < height and crossword[end] != '#':
            end += width

        end -= (width - 1)
        col = [crossword[j] for j in range(i, end, width)]
        spaces = col.count('-')

        if spaces > 0:
            set_of_choices[spaces].add(str(i) + ' ' + str(end) + ' V')
        else:
            words_in_xword.add(''.join(col))
    
    # apply choices, recur using that choices

    for num_spaces in set_of_choices:
        if set_of_choices[num_spaces]:
            for chunk in set_of_choices[num_spaces]:
                choice = chunk.split(' ')
                start = int(choice[0])
                end = int(choice[1]) # note: end is always real_end + 1, to make range() and list comp easier
                start2 = 0
                end2 = 0
                orientation = choice[2]
                word = ''

                if orientation == 'H':
                    word = crossword[start:end]

                    # start2 = start
                    # end2 = start

                    # while start2 // width > 0 and crossword[start2 - width] != '#':
                    #     start2 -= width

                    # while end2 // width < height - 1 and crossword[end2 + width] != '#':
                    #     end2 += width

                else:
                    word = ''.join([crossword[i] for i in range(start, end, width)])

                    # start2 = start
                    # end2 = start

                    # while start2 % width > 0 and crossword[start2 - 1] != '#':
                    #     start2 -= 1

                    # while end2 % width < width - 1 and crossword[end2 + 1] != '#':
                    #     end2 += 1

                potential_words = None

                for letter_pos in range(len(word)):
                    letter = word[letter_pos]
                    if letter != '-':
                        if potential_words is None:
                            # print(letter, letter_pos, len(word))
                            try:
                                potential_words = word_lookup_table[letter][letter_pos][len(word)]    
                            except:
                                return ''
                        else:
                            try:
                                potential_words = set.intersection(potential_words, word_lookup_table[letter][letter_pos][len(word)])
                            except:
                                return ''

                if potential_words is None:
                    for word_to_place in all_words_grouped_by_len[len(word)]:
                        new_crossword = None
                        if orientation == 'H':
                            new_crossword = crossword[:start] + word_to_place + crossword[end:]
                        else:
                            count = 0
                            new_crossword = crossword
                            for pos in range(start, end, width):
                                new_crossword = new_crossword[:pos] + word_to_place[count] + new_crossword[pos + 1:]
                                count += 1

                        ret = fill_in_words(new_crossword, height, width)

                        if ret:
                            return ret

                else:
                    for word_to_place in potential_words:
                        if word_to_place not in words_in_xword:

                            # apply choice and recur
                            
                            new_crossword = None
                            if orientation == 'H':
                                new_crossword = crossword[:start] + word_to_place + crossword[end:]
                            else:
                                count = 0
                                new_crossword = crossword
                                for pos in range(start, end, width):
                                    new_crossword = new_crossword[:pos] + word_to_place[count] + new_crossword[pos + 1:]
                                    count += 1

                            # print()

                            # for i in range(height):
                            #     for j in range(width):
                            #         print(crossword[i * width + j], end=' ')
                            #     print()
                            # print()

                            # for i in range(height):
                            #     for j in range(width):
                            #         print(new_crossword[i * width + j], end=' ')
                            #     print()
                            # print()

                            # print()

                            ret = fill_in_words(new_crossword, height, width)
                            if ret:
                                return ret


    return ''

if __name__ == '__main__':
    main()