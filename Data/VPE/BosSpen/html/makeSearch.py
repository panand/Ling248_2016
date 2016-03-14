
f = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]
for i in range(len(f)):
    p = "curl http://www.let.rug.nl/bos/vpe/corpus/wsj.section%s.html > wsj_%s.html" % (f[i], f[i])
    print p
