import sys; args = sys.argv[1:]
idx = int(args[0])-30

myRegexLst = [
    r"/^0$|^10[01]$/",
    r"/^[01]*$/",
    r"/0$/",
    r"/\b\w*?[aeiou]\w*?[aeiou]\w*?\b/i",
    r"/^1[01]*0$|^0$/",
    r"/^[01]*110[01]*$/",
    r"/\w{2,4}/",
    r"/^\d{3}\s*[-]{0,1}\s*\d{2}\s*[-]{0,1}\s*\d{4}$/",
    r"/^.*?\b\w*d\w*/m",
    r"/^((1*100*1{1,})*|(0*011*0{1,})*)*$/"
    ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])