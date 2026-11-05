# Ödev 4 kontrolü: odev4.py'yi çalıştırır, her görevin çıktısını beklenen çıktıyla karşılaştırır.
# PyCharm'da bu dosyayı açıp Run deyin. odev4.py ile aynı klasörde olmalı. Not vermez, yol gösterir.
import builtins
import os
import pathlib
import re
import runpy
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ODEV = HERE / "odev4.py"
TIMEOUT = 10

# 4. görevdeki input() satırlarına, odev4.py'nin söylediği gibi sırayla bunlar yazılır.
INPUTS = ["üç", "25", "3"]

EXPECTED = {
    "1. Puan": ["Mühendislik: 13", "Tıp: 9", "Hukuk: 5"],
    "2. Maçın sonucu": ["Mühendislik 2-1 Tıp: ev sahibi kazandı", "Hukuk 0-0 Eczacılık: berabere",
                        "Tıp 1-3 Hukuk: deplasman kazandı"],
    "3. Bozuk iki function": ["Gol farkı: 5", "Toplam gol: 5"],
    "4. Skoru sormak": ["Mühendislik kaç gol attı? üç", "Tam sayı girin.", "Mühendislik kaç gol attı? 25",
                        "0 ile 20 arasında bir sayı girin.", "Mühendislik kaç gol attı? 3",
                        "Mühendislik 3 gol attı."],
    "5. Oyuncu": ["Arda (10): 2 gol", "Kerem (7): 1 gol"],
}

# Görevdeki bir call değiştirilip dosya bir kez daha çalıştırılır. Sonuç function'ın içinde hesaplanıyorsa
# çıktı da değişir; elle yazılmışsa aynı kalır.
# (görev, aranan satır, yerine yazılan satır, beklenen çıktı, yalnızca ilk satırlara mı bakılır)
VARIANTS = [
    ("1. Puan", r'^print\("Mühendislik:", points\(4, 1\)\)[ \t]*$', 'print("Mühendislik:", points(5, 0))',
     ["Mühendislik: 15"], True),
    ("2. Maçın sonucu", r'^print\("Mühendislik 2-1 Tıp:", result\(2, 1\)\)[ \t]*$',
     'print("Mühendislik 2-1 Tıp:", result(1, 2))', ["Mühendislik 2-1 Tıp: deplasman kazandı"], True),
    ("4. Skoru sormak", r'^goals\s*=\s*ask_score\("Mühendislik kaç gol attı\? ", 0, 20\)[ \t]*$',
     'goals = ask_score("Mühendislik kaç gol attı? ", 0, 5)',
     ["Mühendislik kaç gol attı? üç", "Tam sayı girin.", "Mühendislik kaç gol attı? 25",
      "0 ile 5 arasında bir sayı girin.", "Mühendislik kaç gol attı? 3", "Mühendislik 3 gol attı."], False),
    ("5. Oyuncu", r'^kerem\.score_goal\(\)[ \t]*$', "kerem.score_goal()\nkerem.score_goal()",
     ["Arda (10): 2 gol", "Kerem (7): 2 gol"], False),
]


def run_with_inputs(path):
    """kontrol.py'nin kendisi bu modda çalışır: input()'a INPUTS'u yazar, sonra odev4.py'yi çalıştırır."""
    answers = iter(INPUTS)

    def typed_input(prompt=""):
        print(prompt, end="")
        try:
            value = next(answers)
        except StopIteration:
            raise EOFError("EOF when reading a line") from None
        print(value)
        return value

    builtins.input = typed_input
    sys.argv = [path]
    runpy.run_path(path, run_name="__main__")


def last_title(text):
    titles = [m.group(1) for ln in text.splitlines() if (m := re.fullmatch(r"=== (.+) ===", ln.strip()))]
    return titles[-1] if titles else None


def run(path):
    """Dosyayı çalıştırır. Hata yoksa (çıktı, None), varsa (None, açıklama satırları) döndürür."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
    try:
        done = subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve()), "--calistir", str(path)],
                              capture_output=True, stdin=subprocess.DEVNULL, env=env, timeout=TIMEOUT)
    except subprocess.TimeoutExpired as e:
        partial = (e.stdout or b"").decode("utf-8", errors="replace")
        lines = [f"{TIMEOUT} saniyede bitmedi. Bir while loop'u hiç bitmiyor olabilir (infinite loop):",
                 "loop'tan çıkan return ya da break'e gerçekten ulaşılıyor mu, bakın."]
        title = last_title(partial)
        if title:
            lines.append(f"Çıktıdaki son görev başlığı: {title}")
        return None, lines
    out = done.stdout.decode("utf-8", errors="replace")
    if done.returncode != 0:
        err = [ln for ln in done.stderr.decode("utf-8", errors="replace").splitlines() if ln.strip()]
        lines = ["çalışırken hata verdi. Error message'ın son satırı:", "    " + (err[-1] if err else "(boş)")]
        title = last_title(out)
        if title:
            lines.append(f"Çıktıdaki son görev başlığı: {title}")
        return None, lines
    return out, None


def sections(text):
    """'=== başlık ===' satırlarına göre çıktıyı böler."""
    out, cur = {}, None
    for line in text.splitlines():
        m = re.fullmatch(r"=== (.+) ===", line.strip())
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur is not None:
            out[cur].append(line.rstrip())
    return out


def block(src, start, end):
    """odev4.py'de iki görev başlığı arasındaki kod (comment satırları hariç)."""
    a = src.find(start)
    b = src.find(end, a + 1) if end else len(src)
    lines = src[a:b if b != -1 else len(src)].splitlines()[1:]
    return [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]


def body(code, head):
    """Bir def'in (ya da class içindeki bir method'un) gövdesi: başlığından sonraki daha içeride duran satırlar."""
    lines = code.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip().startswith(head):
            indent = len(ln) - len(ln.lstrip())
            out = []
            for nxt in lines[i + 1:]:
                if len(nxt) - len(nxt.lstrip()) <= indent:
                    break
                out.append(nxt.strip())
            return out
    return None


def first_difference(want, have):
    for i, w in enumerate(want):
        h = have[i] if i < len(have) else "(satır yok)"
        if h != w:
            return f"{i + 1}. satır beklenen: {w!r}, sizinki: {h!r}"
    return f"beklenenden fazla satır var: {have[len(want)]!r}"


def source_notes(title, src):
    """Görevin odev4.py'de yazan kurallarına uyulmuş mu."""
    titles = list(EXPECTED) + ["Meraklısına"]
    i = titles.index(title)
    start = f'print("=== {title.split(".")[0]}.'
    end = f'print("=== {titles[i + 1].split(".")[0]}' if i + 1 < len(titles) - 1 else 'print("=== Meraklısına'
    code = "\n".join(block(src, start, end))
    raw = src[src.find(start):src.find(end, src.find(start) + 1)]
    notes = []
    if title.startswith("1."):
        b = body(code, "def points(") or []
        if not any(x.startswith("return") for x in b):
            notes.append("points() puanı return etsin")
        if any(x.startswith("print(") for x in b):
            notes.append("points()'in içinde print olmasın; yazmayı alttaki print satırları yapıyor")
    if title.startswith("2."):
        b = body(code, "def result(") or []
        if not any(x.startswith("elif") for x in b) or not any(x.startswith("else") for x in b):
            notes.append("if, elif ve else kullanın")
        if sum(1 for x in b if x.startswith("return")) < 3:
            notes.append("her dalda bir return olsun")
    if title.startswith("3."):
        b1 = body(code, "def goal_difference(") or []
        b2 = body(code, "def add_goals(") or []
        if not any(x.startswith("return") for x in b1) or any(x.startswith("print(") for x in b1):
            notes.append("goal_difference() farkı print etmesin, return etsin")
        if not any(x.startswith("return") for x in b2):
            notes.append("add_goals() yeni toplamı return etsin; call satırlarında dönen değeri total'a atayın")
        reasons = [m.group(1).strip() for m in re.finditer(r"^#\s*Neden:(.*)$", raw, re.M)]
        if len(reasons) < 2 or not all(len(r.split()) >= 3 for r in reasons[:2]):
            notes.append("iki \"# Neden:\" satırına da nedenini tek cümleyle yazın")
    if title.startswith("4."):
        b = body(code, "def ask_score(") or []
        joined = "\n".join(b)
        if not re.search(r"\bwhile\s+True\b", joined):
            notes.append("while True ile sayı gelene kadar sorun")
        if "try:" not in joined or not re.search(r"\bexcept\s+ValueError\b", joined):
            notes.append("int()'in hatasını try ve except ValueError ile yakalayın")
        if not any(x.startswith("return") for x in b):
            notes.append("doğru sayıyı return edin")
        if re.search(r"\b20\b", joined):
            notes.append("20'yi elle yazmayın; sınırlar low ve high parameter'larından gelsin")
    if title.startswith("5."):
        b0 = body(code, "def __init__(") or []
        b1 = body(code, "def score_goal(") or []
        b2 = body(code, "def summary(") or []
        if not any(re.match(r"self\.goals\s*=\s*0$", x) for x in b0):
            notes.append("__init__'te goals 0'dan başlasın: self.goals = 0")
        if not any(re.match(r"self\.goals\s*(\+=\s*1|=\s*self\.goals\s*\+\s*1)$", x) for x in b1):
            notes.append("score_goal() self.goals'u bir artırsın")
        if not any(x.startswith("return") for x in b2) or any(x.startswith("print(") for x in b2):
            notes.append("summary() str'yi print etmesin, return etsin")
    return notes


def variant_note(title, src):
    """Görevdeki bir call'u değiştirip dosyayı yeniden çalıştırır."""
    for name, pattern, new_line, want, head_only in VARIANTS:
        if name != title:
            continue
        changed, count = re.subn(pattern, lambda m: new_line, src, count=1, flags=re.M)
        if count == 0:
            return []
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "odev4.py"
            path.write_text(changed, encoding="utf-8")
            out, problem = run(path)
        if problem:
            return [f"{new_line.splitlines()[0]} ile denedim, dosya " + problem[0]] + problem[1:]
        have = sections(out).get(title, [])
        if head_only:
            have = have[:len(want)]
        if have != want:
            return [f"{new_line.splitlines()[0]} ile denedim: " + first_difference(want, have),
                    "Sonuç function'ın içinde, parameter'lardan hesaplanmalı, elle yazılmamalı."]
    return []


def penalti_note(lines):
    """Meraklısına: sonuç her çalıştırmada değişir, bu yüzden yalnızca biçime bakılır."""
    if len(lines) != 2:
        return "iki satır bekleniyor: Penaltılar ve Kazanan"
    m = re.fullmatch(r"Penaltılar: Mühendislik (\d+) - (\d+) Tıp", lines[0])
    if not m:
        return f"1. satır 'Penaltılar: Mühendislik 4 - 3 Tıp' biçiminde olmalı, sizinki: {lines[0]!r}"
    home, away = int(m.group(1)), int(m.group(2))
    if home == away:
        return "penaltılar eşitlik bozulana kadar sürmeli"
    winner = "Mühendislik" if home > away else "Tıp"
    if lines[1] != f"Kazanan: {winner}":
        return f"2. satır beklenen: {'Kazanan: ' + winner!r}, sizinki: {lines[1]!r}"
    return None


def main():
    try:
        sys.stdout.reconfigure(errors="replace")
    except AttributeError:
        pass
    if not ODEV.exists():
        print("odev4.py bulunamadı. kontrol.py ile aynı klasöre koyun.")
        return
    out, problem = run(ODEV)
    if problem:
        print("odev4.py " + problem[0])
        for ln in problem[1:]:
            print(ln)
        print("Önce bunu düzeltin, sonra kontrolü tekrar çalıştırın.")
        return
    got = sections(out)
    src = ODEV.read_text(encoding="utf-8")
    passed = 0
    for title, want in EXPECTED.items():
        have = got.get(title)
        if have is None:
            print(f"✗ {title}: başlık satırı çıktıda yok. Başlığı yazdıran print() satırını silmeyin.")
            continue
        if not have or all("None" in ln for ln in have):
            print(f"✗ {title}: henüz bir değer gelmiyor. TODO'nun yerine kodunuzu yazın.")
            continue
        notes = []
        if have != want:
            notes.append(first_difference(want, have))
        notes += source_notes(title, src)
        if not notes:
            notes += variant_note(title, src)
        if notes:
            print(f"✗ {title}")
            for n in notes:
                print("    " + n)
        else:
            print(f"✓ {title}")
            passed += 1
    have = got.get("Meraklısına", [])
    if have:
        note = penalti_note(have)
        print(("· " if note else "✓ ") + "Meraklısına (zorunlu değil)")
        if note:
            print("    " + note)
    print(f"\n{passed} / {len(EXPECTED)} görev geçti.")


if len(sys.argv) > 2 and sys.argv[1] == "--calistir":
    run_with_inputs(sys.argv[2])
else:
    main()
