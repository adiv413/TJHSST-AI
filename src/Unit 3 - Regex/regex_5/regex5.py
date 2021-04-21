import sys; args = sys.argv[1:]
idx = int(args[0])-70

myRegexLst = [  
    r"/^(?=.*a)(?=.*e)(?=.*i)(?=.*o)(?=.*u)[a-z]*$/m",
    r"/^([b-df-hj-np-tv-z]*[aeiou][b-df-hj-np-tv-z]*){5}$/m",
    r"/^[b-df-hj-np-tvxz]w[b-df-hj-np-tvxz]$|^[a-z]*[b-df-hj-np-tvxz]w[b-df-hj-np-tvxz]{2}[a-z]*$/m",
    r"/^(([a-z])(([a-z])(([a-z])[a-z]*\6|[a-z]?)\4|[a-z]?)\2|a)$/m",
    r"/^[ac-su-z]*(bt|tb)[ac-su-z]*$/m",
    r"/^(?=[a-z]*([a-z])\1[a-z]*)[a-z]*$/m",
    r"/^(?=.*([a-z])([a-z]*\1[a-z]*){5})[a-z]*$/m",
    r"/^[a-z]*((\w)\2){3}[a-z]*$/m",
    r"/^([aeiou]*[b-df-hj-np-tv-z]){13}[aeiou]*$/m",
    r"/^(([a-z])(?!.*\2.*\2))*$/m"
    ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])