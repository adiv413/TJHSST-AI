import sys; args = sys.argv[1:]
idx = int(args[0])-40

myRegexLst = [
    r"/^[x.o]+$/i",
    r"/^[xo]*[.][xo]*$/i",
    r"/^(x+o*)?[.]|[.](o*x+)?$/i", #add .* on both sides of | if not work
    r"/^.(..)*$/",
    r"/^(0|1[01])([01]{2})*$/",
    r"/\w*(a[eiou]|e[aiou]|i[eaou]|o[aeiu]|u[aeio])\w*/",
    r"/^(0+|10+|1+$)*$/",
    r"/^[bc]*a?[bc]*$/",
    r"/^[bc]*((a[bc]*){2})*[bc]*$/",
    r"/^0$|^(2[02]*)?((1[02]*){2})*$/"
    ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])