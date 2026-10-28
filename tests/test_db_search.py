"""End-to-end: load real js/inci-cleaner.js + js/db.js + data/*.json in V8,
run DB.search / DB.fuzzyCorrect on OCR-style inputs."""
import json, os, sys
from py_mini_racer import MiniRacer
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Users\Wisithbhol S\.gemini\antigravity\scratch\chaecheck'

ctx = MiniRacer()
data = {f: json.load(open(os.path.join(ROOT, 'data', f), encoding='utf-8'))
        for f in os.listdir(os.path.join(ROOT, 'data')) if f.endswith('.json')}
ctx.eval('var self = this; var document = { getElementById: () => null };'
         'var I18n = { t: (k, f) => f };')
ctx.eval('var __DATA = ' + json.dumps(data, ensure_ascii=False) + ';')
ctx.eval('var fetch = (url) => { const f = url.split("/").pop().split("?")[0];'
         ' return Promise.resolve({ ok: true, json: () => Promise.resolve(__DATA[f]) }); };')
ctx.eval(open(os.path.join(ROOT, 'js', 'inci-cleaner.js'), encoding='utf-8').read())
ctx.eval(open(os.path.join(ROOT, 'js', 'db.js'), encoding='utf-8').read().replace('const DB =', 'var DB ='))
ctx.eval('var __ok = false; DB.load().then(() => { __ok = true; });')
ctx.eval('1')  # flush microtasks
assert ctx.eval('__ok'), 'DB failed to load'
print('loaded', ctx.eval('DB.getCount()'))

def search(text):
    return json.loads(ctx.eval(f'JSON.stringify(DB.search({json.dumps(text)}).map(r => [r.inputName, r.id, r._matchType]))'))

CASES = [
  # (input, expected matched ids in order — None means "must be Unknown")
  ("PHENYLBENZIMIDAZOLE SULFONIC ACID,SodiumHYDROXIDETitaniumDIOXIDES ,sodium HyALuronates", 4),
  ("PEG-100 Stearate, Polysorbate 60, 1,2-Hexanediol, CI 77891", 4),
  ("Aqua (Water), Butyrospermum Parkii (Shea) Butter, Niacinamide (5%)", 3),
  ("Aqua/Water/Eau, Caprylic/Capric Triglyceride. Glycerin.", 3),
  ("PhenoxyEthanol, Iso hexadecane, C12-15 Alkyl Benzoate", 3),
  ("WATERGLYCERINDIMETHICONE", 3),
]
fails = 0
for text, n_expected in CASES:
    res = search(text)
    matched = [r for r in res if r[1]]
    ok = len(matched) == n_expected and len(res) == n_expected
    fails += not ok
    print('PASS' if ok else 'FAIL', '|', text)
    for r in res: print('      ', r)

print('fuzzy:', ctx.eval('DB.fuzzyCorrect("Dimethylicone, Octocryrene, Gliceryll Stearate, DIPROPILEGlycol, 1,2-Hexanediol")'))
print(f'{len(CASES)-fails}/{len(CASES)} passed')
