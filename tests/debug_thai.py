from py_mini_racer import MiniRacer
import json

ctx = MiniRacer()
with open(r'C:\Users\Wisithbhol S\.gemini\antigravity\scratch\chaecheck\js\inci-cleaner.js','r',encoding='utf-8') as f:
    ctx.eval(f.read())

s = '\u0e2a\u0e48\u0e27\u0e19\u0e1b\u0e23\u0e30\u0e01\u0e2d\u0e1a (Ingredients): Aqua, Cetearyl Alcohol, Dimethicone, Fragrance.\n\u0e44\u0e21\u0e48\u0e21\u0e35 mineral oil'
ctx.eval(f'var s = {json.dumps(s)}')

r = ctx.eval('''
var headerRe = /(?:ingredients?\\s*[:\\)\\}\\]]|\\u0E2A\\u0E48\\u0E27\\u0E19\\u0E1B\\u0E23\\u0E30\\u0E01\\u0E2D\\u0E1A\\s*[:\\)\\}\\]]?)/gi;
var matches = [];
var m;
while ((m = headerRe.exec(s)) !== null) matches.push({idx: m.index, len: m[0].length, after: s.slice(m.index + m[0].length, m.index + m[0].length + 30)});
JSON.stringify(matches);
''')
with open(r'C:\Users\Wisithbhol S\.gemini\antigravity\scratch\chaecheck\tests\debug_out.txt','w',encoding='utf-8') as f:
    f.write(r + '\n')

# Test 2: what happens after header processing
r2 = ctx.eval('''
var headers = [];
headerRe.lastIndex = 0;
while ((m = headerRe.exec(s)) !== null) headers.push(m);
var result;
if (headers.length >= 1) {
    var firstEnd = headers[0].index + headers[0][0].length;
    result = headers.length >= 2 ? s.slice(firstEnd, headers[1].index) : s.slice(firstEnd);
} else {
    result = s;
}
result;
''')
with open(r'C:\Users\Wisithbhol S\.gemini\antigravity\scratch\chaecheck\tests\debug_out.txt','a',encoding='utf-8') as f:
    f.write('After header: ' + repr(r2) + '\n')
