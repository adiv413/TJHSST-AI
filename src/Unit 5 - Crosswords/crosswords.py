import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import re
import time

def main():
    height = 0
    width = 0
    num_block_squares = 0
    dictionary_file = None
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
            # dictionary_file = open(i, 'r') uncomment in re2
            pass
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

        start_pos = v_offset * width + h_offset
        
        if orientation.lower() == 'h':
            crossword = crossword[:start_pos] + word + crossword[start_pos + len(word):]
        else:
            curr_pos = start_pos

            for i in range(len(word)):
                crossword = crossword[:curr_pos] + word[i] + crossword[curr_pos + 1:]
                curr_pos += width

    if num_block_squares == height * width:
        print(num_block_squares * '#')
    else:
        final_crossword = rotate_180_entire(crossword, height, width)

        if not is_valid(final_crossword, height, width):
            final_crossword = fix_invalid_board(final_crossword, height, width)

        # for i in range(height):
        #     for j in range(width):
        #         print(final_crossword[i * width + j], end=' ')
        #     print()
        # print()

        final_crossword = add_blocking_squares(final_crossword, height, width, num_block_squares)
        
        for i in range(height):
            for j in range(width):
                print(final_crossword[i * width + j], end=' ')
            print()
        print()

        # print('---------------------------------')
        # print(is_valid(final_crossword, height, width))
        # print('---------------------------------')
        # print('\n\n\n\n\n\n\n')

        

        # print(check_small_areas(final_crossword, height, width))

        # print(is_valid(final_crossword, height, width))

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
            # print('sssssssssssssssssssssssss\n\n\n\n\n')
            # print()
            # for i in range(height):
            #     for j in range(width):
            #         print(filled_crossword[i * width + j], end=' ')
            #     print()
            # print()
            # print('sssssssssssssssssssssssss\n\n\n\n\n')


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

            # print('---------------------------------REGIONS------------------------------')

            # for xword in regions_to_fill:
            #     print()
            #     for i in range(height):
            #         for j in range(width):
            #             print(xword[i * width + j], end=' ')
            #         print()
            #     print()

            # print('---------------------------------END REGIONS------------------------------')

            num_squares_to_change_list = {xword.count('*') : xword for xword in regions_to_fill}
            smallest_change = min(num_squares_to_change_list)

            filled_crossword = num_squares_to_change_list[smallest_change].replace('*', '#')

            # print()
            # for i in range(height):
            #     for j in range(width):
            #         print(filled_crossword[i * width + j], end=' ')
            #     print()
            # print()

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

def add_blocking_squares(crossword, height, width, target_num_squares):
    if not is_valid(crossword, height, width):
        return ''

    if crossword.count('#') == target_num_squares:
        return crossword
    elif crossword.count('#') > target_num_squares:
        return ''

    set_of_choices = [i for i in range(len(crossword)) if crossword[i] == '-']
    for choice in set_of_choices:
        new_xword = crossword[:choice] + '#' + crossword[choice + 1:]
        new_pos = rotate_180_pos(choice, height, width)

        if crossword[new_pos] != '-':
            continue

        new_xword = new_xword[:new_pos] + '#' + new_xword[new_pos + 1:]
        ret = add_blocking_squares(new_xword, height, width, target_num_squares)
        if ret:
            return ret

    return ''

    '''
    find a setOfChoices that is collectively exhaustive 
        find a list of the indices
        order them by center -> outside (do this or no??)
        order them by are they adjacent to another blocking square
    for each possibleChoice in the setOfChoices:
        subPzl = pzl with possibleChoiceapplied
        bF = bruteForce(subPzl)
        if bF: return bF
    return ""
    '''

if __name__ == '__main__':
    main()