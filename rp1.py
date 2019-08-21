import sys
import re

###可以将以下格式：
###      <div>EXCIA 雅思 蜂浆粉霜&nbsp; &nbsp;1232<br />
###      <a href="http://item.taobao.com/item.htm?id=566602210609" target="_blank">http://item.taobao.com/item.htm?id=566602210609</a></div>
###替换为：
###      <div data-spm-anchor-id="a2126o.11854294.0.i61.69c44831JC570V">ALBION EXAGE基础28天美白精华&nbsp; 388<a href="http://item.taobao.com/item.htm?id=565312439339" target="_blank">点击链接</a><br />

if len(sys.argv) < 3:
    print("usage: rp1.py [source_file] [target_file]")
    exit(0)

try:
    source = open(sys.argv[1], 'r')
except:
    print("Open file:", sys.argv[0], " failed.")
    exit(0)

try:
    target = open(sys.argv[2], 'w')
except:
    print("Open file:", sys.argv[1], " failed.")
    exit(0)

output = []
temp = []
pre = re.compile(r'^<div[\s\S]*')
addr = re.compile(r'[\s\S]*<a href=\"(http:\/\/item.taobao.com\/item.htm\?id=\d+)\"')
preline = -1
for line in source:
    temp.append(line)
    # r1 = pre.match(line)
    r1 = line.rfind('<')
    r2 = addr.match(line)
    if len(line) > 18 and r1 != -1 and not r2:
        preline = len(temp)-1
    elif r2:
        idr = r2.group(1)
        if preline != -1:
            l = temp[preline]
            lidx = l.rindex('<')
            ll = l[:lidx]
            lr = l[lidx:]
            l = ll + r'<a href="' + idr + r'" target="_blank">点击链接</a>' + lr
            temp[preline] = l
            temp.pop()
        for l in temp:
            output.append(l)
        temp = []
        preline = -1

for line in output:
    target.write(line)

source.close()
target.close()
print('Done!')