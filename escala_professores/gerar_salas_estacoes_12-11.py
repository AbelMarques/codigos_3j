# -*- coding: utf-8 -*-
# gerar_salas_estacoes_12-11.py - quadro de salas/estações de quinta-feira 12/11/2026 (refeito).
# Mudança: a sala 115 fica reservada para a DIRETORA o dia todo. Ninguém dá aula na 115.
# Marcos Paulo (antes 115 · Estúdio 1, 07:30–09:10) passa para a sala 121 · Estação 01, livre nesse horário.
import html, os
AQUI = os.path.dirname(os.path.abspath(__file__))
SALA_DIRETORA = "115"
SUB, DATA = "Quinta-feira, 12/11/2026", "5ª feira · 12/11/2026"
D = [
  ("ABEL", "120", "01", "07:00–12:00"), ("ABEL", "120", "01", "13:00–16:00"),
  ("AMANDA", "122", "01", "07:30–09:10"), ("AMANDA", "122", "01", "10:15–11:55"), ("AMANDA", "122", "01", "14:50–15:40"),
  ("BRUNO", "126", "01", "07:10–09:40"), ("BRUNO", "126", "01", "09:55–12:25"),
  ("DOUGLAS", "114", "01", "10:15–11:55"), ("DOUGLAS", "114", "01", "13:10–14:50"), ("DOUGLAS", "114", "01", "15:55–17:35"),
  ("JAYSON", "125", "01", "07:30–10:00"), ("JAYSON", "125", "01", "10:15–11:55"),
  ("JORGE", "116", "01", "07:10–08:50"),
  ("LUCAS", "116", "01", "09:10–10:00"), ("LUCAS", "116", "01", "10:45–12:25"),
  ("MARCELO", "128", "01", "07:30–09:10"), ("MARCELO", "128", "01", "10:15–12:45"),
  ("MARCOS JOSÉ", "119", "01", "09:10–10:00"), ("MARCOS JOSÉ", "119", "01", "10:15–11:55"),
  ("MARCOS PAULO", "121", "01", "07:30–09:10"),          # remanejado da 115 (Estúdio 1)
  ("MARJORIE", "121", "01", "11:05–12:45"),
  ("SANDRA", "119", "01", "07:30–09:10"),
  ("TIAGO", "118", "01", "07:50–09:30"), ("TIAGO", "118", "01", "09:45–11:25"),
  ("TÂNIA", "114", "01", "07:30–09:10"),
]
e = html.escape
m = lambda h: int(h[:2]) * 60 + int(h[3:5])

def checa(D):
    ocup = {}
    for p, s, est, h in D:
        assert s != SALA_DIRETORA, f"{p} está na sala {SALA_DIRETORA}, reservada para a diretora"
        a, b = m(h[:5]), m(h[-5:])
        for q, a2, b2 in ocup.get((s, est), []):
            assert b <= a2 or a >= b2, f"conflito {s}/{est}: {p} x {q} {h}"
        ocup.setdefault((s, est), []).append((p, a, b))
    por_prof = {}
    for p, s, est, h in D:
        for a2, b2 in por_prof.get(p, []):
            assert m(h[-5:]) <= a2 or m(h[:5]) >= b2, f"{p} em dois lugares {h}"
        por_prof.setdefault(p, []).append((m(h[:5]), m(h[-5:])))

def junta(itens):
    out = []
    for s, est, h in itens:
        if out and out[-1][0] == s and out[-1][1] == est: out[-1][2].append(h)
        else: out.append((s, est, [h]))
    return out

rotulo = lambda est: f"<span class=est>Estação {est}</span>"
css = """@page{size:A4 landscape;margin:8mm}body{font-family:'Segoe UI',Arial,sans-serif;color:#1c2b33;font-size:10.6px;margin:0}
h1{font-size:20px;color:#045967;margin:0}.sub{color:#555;margin:1px 0 6px}.cols{display:flex;gap:12px}.col{flex:1}
h2{font-size:13px;background:#045967;color:#fff;padding:3px 10px;margin:0}
table{border-collapse:collapse;width:100%}th{background:#e6f0f2;text-align:left;padding:3px 6px;font-size:10.5px;border-bottom:2px solid #045967}
td{padding:2px 6px;border-bottom:1px solid #d5dde0}td.p{font-weight:700;white-space:nowrap;vertical-align:middle}td.c{text-align:center}
td.big{font-size:16px;font-weight:800;color:#045967;background:#f1f7f8;border-right:1px solid #d5dde0}
.est{background:#fff3d6;border:1px solid #e8c36a;border-radius:10px;padding:0 8px;font-size:10px;white-space:nowrap}
.estg{background:#c2185b;color:#fff;border-radius:10px;padding:0 8px;font-size:10px;font-weight:700;white-space:nowrap}
tr.grav td{background:#fde8ec;color:#8a1534;font-weight:700}tr.grav td.big{background:#f1f7f8;color:#045967}td small{font-weight:400}
.grade{margin-top:6px;display:flex;gap:6px;align-items:stretch;flex-wrap:wrap}.grade b{color:#8a1534}
.slot{border:1px solid #c2185b;border-radius:6px;padding:2px 7px;background:#fff5f7;font-size:10.5px;white-space:nowrap}
.aviso{margin-top:7px;border:3px solid #c2185b;border-radius:10px;padding:7px 12px;background:#fde8ec;color:#8a1534;text-align:center}
.aviso .t{font-size:15px;font-weight:800;letter-spacing:.3px}.aviso .s{font-size:11.5px;margin-top:2px}
.dataesc{margin-top:5px;text-align:center;font-size:22px;font-weight:800;color:#045967;letter-spacing:1px}
tr.dir td{background:#e8eaf6;color:#283593;font-weight:700}tr.dir td.big{background:#f1f7f8;color:#045967}
.estd{background:#283593;color:#fff;border-radius:10px;padding:0 8px;font-size:10px;font-weight:700;white-space:nowrap}
.res{margin-top:6px;border:3px solid #283593;border-radius:10px;padding:6px 12px;background:#e8eaf6;color:#283593;text-align:center}
.res .t{font-size:15px;font-weight:800;letter-spacing:.3px}.res .s{font-size:11.5px;margin-top:2px}"""

checa(D)
profs = {}
for p, s, est, h in D: profs.setdefault(p, []).append((s, est, h))
por_prof = ""
for p in sorted(profs):
    blocos = junta(sorted(profs[p], key=lambda x: x[2]))
    for i, (s, est, hs) in enumerate(blocos):
        nome = f"<td class=p rowspan={len(blocos)}>{e(p)}</td>" if i == 0 else ""
        por_prof += f"<tr>{nome}<td class=c>{s}</td><td class=c>{rotulo(est)}</td><td>{' &nbsp;·&nbsp; '.join(hs)}</td></tr>"

salas = {}
for p, s, est, h in D: salas.setdefault(s, {}).setdefault((est, p), []).append(h)
salas[SALA_DIRETORA] = None
por_sala = ""
for s in sorted(salas):
    if salas[s] is None:
        por_sala += (f"<tr class=dir><td class='c big'>{s}</td><td class=c><span class=estd>Diretoria</span></td>"
                     f"<td class=p>DIRETORA <small>(sala reservada)</small></td><td>Dia todo</td></tr>")
        continue
    ls = sorted(salas[s].items(), key=lambda kv: (kv[0][0], min(kv[1])))
    for i, ((est, p), hs) in enumerate(ls):
        cel = f"<td class='c big' rowspan={len(ls)}>{s}</td>" if i == 0 else ""
        por_sala += f"<tr>{cel}<td class=c>{rotulo(est)}</td><td class=p>{e(p)}</td><td>{' &nbsp;·&nbsp; '.join(sorted(hs))}</td></tr>"

page = f"""<!doctype html><html lang=pt-BR><head><meta charset=utf-8><title>Salas e estações</title><style>{css}</style></head><body>
<h1>Quadro de salas e estações</h1><div class=sub>{SUB} · distribuição por professor(a) e por sala · horários de aula</div>
<div class=cols>
<div class=col><h2>Por professor(a)</h2><table><tr><th>Professor(a)</th><th>Sala</th><th>Local</th><th>Horário</th></tr>{por_prof}</table></div>
<div class=col><h2>Por sala e estação</h2><table><tr><th>Sala</th><th>Local</th><th>Professor(a)</th><th>Horário</th></tr>{por_sala}</table></div>
</div>
<div class=res><div class=t>SALA {SALA_DIRETORA} RESERVADA PARA A DIRETORA O DIA TODO</div>
<div class=s>Nesta quinta-feira não haverá aulas nem gravações na sala {SALA_DIRETORA} (Estúdio 1). O professor Marcos Paulo (07:30–09:10) foi remanejado para a <b>sala 121 · Estação 01</b>.</div></div>
<div class=dataesc>{DATA}</div>
</body></html>"""
open(os.path.join(AQUI, "Salas_Estacoes_12-11.html"), "w", encoding="utf-8").write(page)
print("ok 12-11 · sala", SALA_DIRETORA, "livre para a diretora")
