"""Offline safety-screen test: runs prescreen over the 7 request fixtures. No API key needed."""
import os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
ME = "nefarioustrey@agentmail.to"
import tempfile as _t
TRAIL = os.path.join(_t.mkdtemp(), "trail.jsonl")
env = dict(os.environ, CROSSROADS_CONTACTS=os.path.join(H, "contacts_test.json"), CROSSROADS_TRAIL=TRAIL)
def run(name, sender=None):
    f = os.path.join(H, f"req_{name}.txt")
    if sender is None:
        m = re.search(r'"from_inbox":\s*"([^"]+)"', open(f).read()); sender = m.group(1) if m else ""
    if name != "expired":  # keep fixtures fresh: push expiry 2 days ahead in a temp copy
        import tempfile, datetime
        fut = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        txt = re.sub(r'("expires(?:_at)?":\s*")[^"]+(")', lambda m: m.group(1) + fut + m.group(2), open(f).read())
        tf = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False); tf.write(txt); tf.close(); f = tf.name
    p = subprocess.run([sys.executable, os.path.join(R, "scripts", "crossroads.py"), "prescreen",
                        "--inbox", ME, "--body", f, "--sender", sender], capture_output=True, text=True, env=env)
    return p.stdout + p.stderr
passed = failed = 0
def t(label, ok, out=""):
    global passed, failed
    if ok: passed += 1; print("PASS", label)
    else: failed += 1; print("FAIL", label); print(out[:600])
for n in ["ok", "deny"]:
    o = run(n); t(f"{n}: approval card", "APPROVE THIS" in o, o)
for n, s in [("cred", None), ("expired", None), ("spoof", "evil@x.com"), ("unknown", None)]:
    o = run(n, s); t(f"{n}: screened out", "APPROVE THIS" not in o and "SCREENED OUT" in o, o)
o = run("inject"); t("inject: report-and-disengage card", "APPROVE THIS" not in o and re.search(r"disengage|report", o, re.I), o)
lines = open(TRAIL).read().splitlines() if os.path.exists(TRAIL) else []
t("audit trail: one line per screen", len(lines) == 7, str(lines))
print(f"{passed}/{passed+failed} passed"); sys.exit(1 if failed else 0)
