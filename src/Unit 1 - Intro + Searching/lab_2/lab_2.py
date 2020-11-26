# Aditya Vasantharao, pd. 4
# CodingBat Python all level 2 answers in as few characters as possible per method (before minification)

def string_times(str, n):
  return str * n

def front_times(str, n):
  return str[:3] * n

def string_bits(str):
  return str[::2]

def string_splosion(str):
  return ''.join([str[:i+1] for i in range(len(str))])

def last2(str):
  return len(str) and sum([str[i:i + 2] == str[-2:] for i in range(len(str))]) - 1

def array_count9(nums):
  return nums.count(9)

def array_front9(nums):
  return 9 in nums[:4]

def array123(nums):
  return ' 1, 2, 3,' in ' '+str(nums)[1:-1]+','

def string_match(a, b):
  return sum([(i,j)==(k,l) for i,j,k,l in zip(a,a[1:],b,b[1:])])

def make_bricks(small, big, goal):
  return goal - 5 * min(goal // 5, big) - small < 1

def lone_sum(a, b, c):
  return a*(b!=a!=c)+b*(a!=b!=c)+c*(a!=c!=b) 

def lucky_sum(a, b, c):
  return a*(a!=13)+b*(b!=13!=a)+c*(b!=13!=c!=13!=a!=13) 

def no_teen_sum(a, b, c):
  return sum([i*(i<13 or 14<i<17 or i>19) for i in [a,b,c]])

def round_sum(a, b, c):
  return int(sum([round(i+.1,-1) for i in [a,b,c]]))

def close_far(a, b, c):
  return abs(c-b)>1 and (abs(a-b)<2 and abs(a-c)>1 or abs(a-c)<2 and abs(a-b)>1)

def make_chocolate(small, big, goal):
  return [i*(i<=small)-(i>small) for i in [goal - 5 * min(goal // 5, big)]][0]

def double_char(str):
  return ''.join([i*2 for i in str])

def count_hi(str):
  return str.count('hi')

def cat_dog(str):
  return str.count('cat') == str.count('dog')

def count_code(str):
  return sum([(str[i:i+2],str[i+3])==('co','e') for i in range(len(str)-3)])

def end_other(a, b):
  return a.lower().endswith(b.lower()) or b.lower().endswith(a.lower())

def xyz_there(str):
  return [1 for i in range(len(str)-2) if str[i:i+3] == 'xyz' and str[abs(i-1)]!='.'] != []

def count_evens(nums):
  return sum([i%2==0 for i in nums])

def big_diff(nums):
  return max(nums) - min(nums)

def centered_average(nums):
  return nums.remove(max(nums)) or nums.remove(min(nums)) or sum(nums)//len(nums)

def sum13(nums):
  return sum([v for i,v in enumerate(nums) if nums[max(0,i-1)]!=13!=v])

def sum67(nums): 
  return (b := False) or sum([i*(not (b and i==7))*(not b)*(i!=6)+0*(b := b and i!=7 or i==6) for i in nums])

def has22(nums):
  return ' 2, 2,' in ' '+str(nums)[1:-1]+','
