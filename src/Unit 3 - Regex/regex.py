import sys; args = sys.argv[1:]
idx = int(args[0])-30

myRegexLst = [
    r"/^0$|^10[01]$/",
    r"/^[01]+$/",
    r"/0$/",
    r"/\b\w{0,}?[aeiou]\w{0,}?[aeiou]\w{0,}?\b/i",
    r"",
    r"/.{2,4}/",
    r"/^\d{3}\s{0,}[-–]{0,1}\s{0,}\d{2}\s{0,}[-–]{0,1}\s{0,}\d{4}$/",
    ... ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])