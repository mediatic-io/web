"""Aplica el bloque "SEGUIR LEYENDO" a los HTML de artículos ya generados (sin necesidad de ejecutar build.py).

Uso:  python3 aplicar_seguir.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from seguir_leyendo import parchear

L = open(os.path.join(HERE, 'build.py'), encoding='utf-8').read().split('\n')
ini = next(i for i, l in enumerate(L) if l.startswith('ART_META={'))
fin = next(i for i, l in enumerate(L) if l.startswith('ART_META=dict(sorted('))
ns = {'os': os}
exec('\n'.join(L[ini:fin + 1]), ns)
ART_META, RELATED = ns['ART_META'], ns['RELATED']

WEB = os.path.dirname(HERE)
for f in ART_META:
    p = os.path.join(WEB, f)
    if not os.path.exists(p):
        continue
    s = open(p, encoding='utf-8').read()
    n = parchear(s, f, ART_META, RELATED)
    if n != s:
        open(p, 'w', encoding='utf-8').write(n)
        print('actualizado', f)
