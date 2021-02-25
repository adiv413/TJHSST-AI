import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import re

def main():
    height = 0
    width = 0
    num_block_squares = 0
    dictionary_file = None
    final_crossword = ""
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
    
    final_crossword = (height * width) * '-'

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
            final_crossword = final_crossword[:start_pos] + word + final_crossword[start_pos + len(word):]
        else:
            curr_pos = start_pos

            for i in range(len(word)):
                final_crossword = final_crossword[:curr_pos] + word[i] + final_crossword[curr_pos + 1:]
                curr_pos += width
        

    if height * width == num_block_squares:
        final_crossword = (height * width) * '#'
    print(check_for_isolated_regions(final_crossword, height, width))
    # print(height, width, num_block_squares)
    # print(seed_strings)
    # print(final_crossword)
    # print()
    for i in range(height):
        for j in range(width):
            print(final_crossword[i * width + j], end=' ')
        print()

    
# returns True if there are no isolated regions (everything is connected), and False if there are isolated regions
def check_for_isolated_regions(crossword, height, width):
    start = crossword.index('-')
    filled_crossword = flood_fill(crossword, start // width, start % width, width, height)

    if '-' in filled_crossword:
        return False
    else:
        return True

def flood_fill(crossword, i, j, width, height):
    # i is the vertical displacement and j is horizontal
    pos = i * width + j
    if i >= height or j >= width or i < 0 or j < 0 or crossword[pos] != '-':
        return crossword

    new_crossword = crossword[:pos] + 'x' + crossword[pos + 1:]

    new_crossword = flood_fill(new_crossword, i + 1, j, width, height)
    new_crossword = flood_fill(new_crossword, i, j + 1, width, height)
    new_crossword = flood_fill(new_crossword, i - 1, j, width, height)
    new_crossword = flood_fill(new_crossword, i, j - 1, width, height)
    
    return new_crossword

if __name__ == '__main__':
    main()