import os, csv, urllib, sys
fin = urllib.urlopen("http://data.iana.org/TLD/tlds-alpha-by-domain.txt")
domains = set(filter(lambda a: not a.startswith('#'), [line.strip().lower() for line in fin]))
fin.close()
mindomainlen = min(map(len, domains))
maxdomainlen = max(map(len, domains))
words = open("/usr/share/dict/words")
fout = open(sys.argv[1], 'w', newline='')
writer = csv.writer(fout)
null = None
true = True
false = False
for word in words:
    word = word.strip().lower()
    for i in range(mindomainlen, min(len(word), maxdomainlen)):
        if word[-i:] in domains:
            row = []
            row.append(word)
            domain = word[:-i]+'.'+word[-i:]
            row.append(domain)
            exitCode = os.system("host -W 1 "+domain+"")
            if exitCode == 0:
                # If it has a host,
                # the website already exists.
                #row.append("Taken")
                continue
            elif exitCode in (1, 256):
                #row.append("Available")
                pass
            else:
                raise Exception("invalid exit code "+str(exitCode))
            '''url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="+urllib.quote_plus(word)
            print url
            urldoc = urllib.urlopen(url)
            result = eval(urldoc.read())
            urldoc.close()
            row.append(result["responseData"]["cursor"]["estimatedResultCount"])'''
            row.append(len(word))
            row.append(i)
            writer.writerow(row)
fout.close()
words.close()