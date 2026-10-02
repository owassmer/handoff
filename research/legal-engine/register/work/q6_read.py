"""Print batch-6 sections by index range: python3 register/work/q6_read.py 0 6 [maxchars]"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q6_lib import BATCH, text
a, b = int(sys.argv[1]), int(sys.argv[2])
m = int(sys.argv[3]) if len(sys.argv) > 3 else 100000
for i in range(a, b):
    s = BATCH[i]
    t = text(s["text_file"])
    body = t.split("\n", 3)[3] if t.startswith("SOURCE") else t
    print(f"\n######## [{i}] {s['section_id']} ({s['chars']}) file={s['text_file']}")
    print(body[:m])
