import sys; args = sys.argv[1:]
idx = int(args[0])-50

myRegexLst = [  
    r"/(\w)\w*\1/i",
    r"/(\w)(\w*\1){3}/i",
    r"/^(0|1)([01]*\1)*$/",
    r"/\b(?=\w*cat)\w{6}\b/i",
    r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",
    r"/\b(?!\w*cat)\w{6}\b/i",
    r"/\b((\w)(?!\w*\2))+\b/i",
    r"//",
    r"//",
    r"//"
    ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])