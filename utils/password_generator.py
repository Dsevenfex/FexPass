# utils/password_generator.py

import itertools
import re
from colorama import Fore, Style
from datetime import datetime
import os

_LEET_MAP = str.maketrans({
    'a': '4', 'A': '4',
    'e': '3', 'E': '3',
    'i': '1', 'I': '1',
    'o': '0', 'O': '0',
    's': '5', 'S': '5',
    't': '7', 'T': '7'
})

def _to_leet(s: str) -> str:
    return s.translate(_LEET_MAP)

def _clean_token(s):
    if not s:
        return None
    s = str(s).strip()
    if not s:
        return None
    if s.upper() == "N":  #
        return None
    return s

def _birth_variants(birth_str):
    if not birth_str:
        return []
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', birth_str):
        return []
    dd, mm, yyyy = birth_str.split('/')
    yy = yyyy[-2:]
    variants = set()
    variants.add(dd + mm + yyyy)   # ddmmyyyy
    variants.add(dd + mm + yy)     # ddmmyy
    variants.add(yyyy)             # yyyy
    variants.add(yy)               # yy
    variants.add(mm + dd + yyyy)   # mmddyyyy
    variants.add(mm + dd + yy)     # mmddyy
    variants.add(mm + dd)          # mmdd
    variants.add(dd + mm)          # ddmm
    variants.add(mm)               # mm
    variants.add(dd)               # dd
    variants.add(yyyy + mm + dd)   # yyyymmdd
    return [v for v in variants if v]

def _variations(token):
    """
    produce reasonable textual variations for a token
    """
    v = set()
    v.add(token)
    v.add(token.lower())
    v.add(token.upper())
    v.add(token.title())
    if token.isalpha():
        v.add(token.capitalize())
    v.add(_to_leet(token))
    return v

def password_generate(user_data: dict):

    try:
        min_len = int(user_data.get("min_length", 6))
    except:
        min_len = 6

    token_keys = ["Username","Name","Surname","Pet","Color","Fnumber","Fperson","Game","Sport","Friend","Word","Animal","Place"]
    tokens = []
    for k in token_keys:
        t = _clean_token(user_data.get(k))
        if t:
            tokens.append(t)

    birth = _clean_token(user_data.get("Birth"))
    birth_vars = _birth_variants(birth)

    favnum = _clean_token(user_data.get("Fnumber"))
    extra_suffixes = ["!", "@", "#", "123", "2024", "1234", "007", "01", "2025"]
    if favnum and favnum.isdigit():
        extra_suffixes.insert(0, favnum)

    base_variants = set()
    for t in tokens:
        for tv in _variations(t):
            base_variants.add(tv)

    for b in birth_vars:
        base_variants.add(b)

    combos_to_try = []
    for a, b in itertools.permutations(tokens, 2):
        if a and b and a != b:
            combos_to_try.append(a + b)
            combos_to_try.append(a + "_" + b)
            combos_to_try.append(a + "-" + b)
            combos_to_try.append(a + "." + b)
    if len(tokens) >= 3:
        for perm in itertools.permutations(tokens, 3):
            a, b, c = perm
            if a != b and b != c and a != c:
                combos_to_try.append(a + b + c)

    combo_variants = set()
    for combo in combos_to_try:
        if 3 <= len(combo) <= 40:
            for v in _variations(combo):
                combo_variants.add(v)

    candidates = set()

    for v in base_variants:
        if len(v) >= min_len:
            candidates.add(v)
        else:
            for s in extra_suffixes + birth_vars:
                cand = v + s
                if len(cand) >= min_len:
                    candidates.add(cand)

    for v in combo_variants:
        if len(v) >= min_len:
            candidates.add(v)
        else:
            for s in extra_suffixes + birth_vars:
                cand = v + s
                if len(cand) >= min_len:
                    candidates.add(cand)

    for t in tokens:
        cleaned = _clean_token(t)
        if not cleaned:
            continue
        for b in birth_vars:
            cand1 = cleaned + b
            cand2 = b + cleaned
            for c in (cand1, cand2):
                if len(c) >= min_len:
                    candidates.add(c)
                else:
                    for s in extra_suffixes:
                        cand3 = c + s
                        if len(cand3) >= min_len:
                            candidates.add(cand3)

    common_words = ["password","pass","admin","qwerty","welcome","letmein"]
    for w in common_words:
        for v in _variations(w):
            if len(v) >= min_len:
                candidates.add(v)
            else:
                for s in extra_suffixes + birth_vars:
                    cand = v + s
                    if len(cand) >= min_len:
                        candidates.add(cand)

    cleaned_final = []
    for p in candidates:
        if not p:
            continue
        ps = str(p).strip()
        if len(ps) >= min_len:
            cleaned_final.append(ps)

    cleaned_final = sorted(set(cleaned_final), key=lambda x: (len(x), x))

    MAX_RESULTS = 10000
    if len(cleaned_final) > MAX_RESULTS:
        cleaned_final = cleaned_final[:MAX_RESULTS]

    print(Line := "-"*40)
    print(f"{Fore.GREEN}Generated {len(cleaned_final)} password candidates (min length {min_len}){Style.RESET_ALL}")
    print(Line)
    for pwd in cleaned_final:
        print(pwd)
    print(Line)

    try:
        raw_name = _clean_token(user_data.get("Name")) or ""
        raw_surname = _clean_token(user_data.get("Surname")) or ""
    
        if raw_name or raw_surname:
            base = (raw_name + raw_surname).lower()
        else:
            base = (_clean_token(user_data.get("Username")) or "generated_passwords").lower()
    
        base = re.sub(r'[^a-z0-9._-]', '', base)
    
        if not base:
            base = "generated_passwords"
    
        os.makedirs("outputs", exist_ok=True)
        fname = os.path.join("outputs", f"{base}.txt")
    
        if os.path.exists(fname):
            i = 1
            base_try = base
            while os.path.exists(os.path.join("outputs", f"{base_try}.txt")):
                i += 1
                base_try = f"{base}_{i}"
            fname = os.path.join("outputs", f"{base_try}.txt")
    
        with open(fname, "w", encoding="utf-8") as f:
            for pwd in cleaned_final:
                f.write(pwd + "\n")
        print(f"{Fore.GREEN}Saved to {fname}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Could not save to file: {e}{Style.RESET_ALL}")

    return cleaned_final
