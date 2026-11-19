#!/usr/bin/env python3
"""Gera dist/index.html a partir de template.html + style.css + config.json.

Uso:
    python3 build.py                 # usa config.json
    python3 build.py clientes/x.json # usa outro arquivo; saída em dist/<nome>/
Só biblioteca padrão. Todo texto do config é escapado.
"""
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent
OBRIGATORIOS = ["nome", "slogan", "descricao_curta", "responsavel", "telefone_exibicao",
                "whatsapp", "endereco", "cidade", "estado", "servicos", "horarios",
                "sobre", "diferenciais", "cor_principal", "cor_escura"]


def e(valor):
    return html.escape(str(valor), quote=True)


def validar(cfg):
    faltando = [k for k in OBRIGATORIOS if k not in cfg or cfg[k] in ("", [], None)]
    if faltando:
        sys.exit(f"config incompleto, faltam: {', '.join(faltando)}")
    if not re.fullmatch(r"55\d{10,11}", str(cfg["whatsapp"])):
        sys.exit("whatsapp deve ter só dígitos, com 55 + DDD + número (ex.: 5519900000000)")
    for chave in ("cor_principal", "cor_escura"):
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", cfg[chave]):
            sys.exit(f"{chave} deve ser uma cor hex como #0f8b8d")


def montar(cfg):
    validar(cfg)
    endereco = ", ".join(p for p in [cfg["endereco"], cfg.get("bairro", ""),
                                      f'{cfg["cidade"]}/{cfg["estado"]}'] if p)
    if cfg.get("cep"):
        endereco += f' · CEP {cfg["cep"]}'
    link_zap = f'https://wa.me/{cfg["whatsapp"]}?text={quote(cfg.get("mensagem_whatsapp", ""))}'
    consulta = quote(f'{cfg["nome"]}, {cfg["endereco"]}, {cfg["cidade"]} {cfg["estado"]}')
    mapa = cfg.get("mapa_embed_url") or f"https://www.google.com/maps?q={consulta}&output=embed"

    servicos = "\n".join(
        f'        <div class="card"><h3>{e(s["titulo"])}</h3><p>{e(s["texto"])}</p></div>'
        for s in cfg["servicos"])
    sobre = "\n".join(f"        <p>{e(p)}</p>" for p in cfg["sobre"])
    difs = "\n".join(f"          <li>{e(d)}</li>" for d in cfg["diferenciais"])
    horarios = "\n".join(
        f'          <tr><td>{e(h["dia"])}</td><td>{e(h["horas"])}</td></tr>'
        for h in cfg["horarios"])
    insta = ""
    if cfg.get("instagram"):
        usuario = cfg["instagram"].lstrip("@")
        insta = (f'        <p><strong>Instagram:</strong> '
                 f'<a href="https://instagram.com/{quote(usuario)}" rel="noopener">@{e(usuario)}</a></p>')
    aviso = ""
    if cfg.get("modo_exemplo"):
        aviso = ('<div class="aviso-exemplo">Site de demonstração com dados fictícios. '
                 'Seu site será montado com as informações reais do seu consultório.</div>')

    json_ld = {
        "@context": "https://schema.org",
        "@type": "Dentist",
        "name": cfg["nome"],
        "description": cfg["descricao_curta"],
        "telephone": f'+{cfg["whatsapp"]}',
        "address": {"@type": "PostalAddress", "streetAddress": cfg["endereco"],
                    "addressLocality": cfg["cidade"], "addressRegion": cfg["estado"],
                    "postalCode": cfg.get("cep", ""), "addressCountry": "BR"},
    }
    json_ld_txt = json.dumps(json_ld, ensure_ascii=False).replace("</", "<\\/")

    valores = {
        "nome": e(cfg["nome"]), "slogan": e(cfg["slogan"]),
        "descricao_curta": e(cfg["descricao_curta"]), "cidade": e(cfg["cidade"]),
        "responsavel": e(cfg["responsavel"]), "cro": e(cfg.get("cro", "")),
        "telefone_exibicao": e(cfg["telefone_exibicao"]),
        "cor_principal": cfg["cor_principal"], "cor_escura": cfg["cor_escura"],
        "endereco_completo": e(endereco), "link_whatsapp": e(link_zap),
        "mapa_url": e(mapa), "servicos_html": servicos, "sobre_html": sobre,
        "diferenciais_html": difs, "horarios_html": horarios,
        "instagram_html": insta, "aviso_exemplo": aviso,
        "json_ld": json_ld_txt, "css": (RAIZ / "style.css").read_text(encoding="utf-8"),
        # exemplo fictício: não indexar e não publicar dados estruturados falsos
        "robots_meta": '  <meta name="robots" content="noindex, nofollow">' if cfg.get("modo_exemplo") else "",
        "json_ld_tag": "" if cfg.get("modo_exemplo")
        else f'  <script type="application/ld+json">{json_ld_txt}</script>',
    }
    saida = (RAIZ / "template.html").read_text(encoding="utf-8")
    # css e json_ld_tag primeiro (conteúdo já final); depois os demais marcadores
    for chave in ("css", "json_ld_tag"):
        saida = saida.replace("{{" + chave + "}}", valores[chave])
    saida = re.sub(r"\{\{(\w+)\}\}", lambda m: valores.get(m.group(1), m.group(0)), saida)
    restantes = re.findall(r"\{\{\w+\}\}", saida)
    if restantes:
        sys.exit(f"marcadores sem valor: {restantes}")
    return saida


def main():
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "config.json"
    cfg = json.loads(caminho.read_text(encoding="utf-8"))
    destino = RAIZ / "dist" if len(sys.argv) < 2 else RAIZ / "dist" / caminho.stem
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "index.html").write_text(montar(cfg), encoding="utf-8")
    print(f"ok: {destino / 'index.html'}")


if __name__ == "__main__":
    main()
