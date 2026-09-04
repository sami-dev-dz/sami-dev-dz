# -*- coding: utf-8 -*-
"""Génère les deux SVG du diagramme de pipeline pour le README de profil.

Pourquoi deux fichiers et non un seul avec du CSS.

GitHub nettoie le HTML des READMEs et n'exécute pas les feuilles de style : une
media query `prefers-color-scheme` posée dans un `<style>` ne survit pas. La
méthode qui fonctionne partout est un `<picture>` avec deux sources, une par
thème. Chaque fichier porte donc ses couleurs en dur.

Pourquoi pas shields.io ni une carte de statistiques : ces services rendent des
images depuis leurs propres serveurs. Lors de la revue du README, deux d'entre
eux renvoyaient 503 et 402. Une image cassée sur une page de candidature est
pire que pas d'image. Ces deux SVG vivent dans le dépôt : ils ne peuvent pas
tomber.

Les couleurs sont celles de GitHub lui-même — le diagramme doit avoir l'air
d'appartenir à la page, pas d'y avoir été collé.

Lancement :  python build-pipeline-svg.py
"""
import io

W, H = 760, 196

THEMES = {
    "light": dict(
        ink="#1f2328", muted="#59636e", rule="#d1d9e0",
        accent="#0969da", accent_soft="#ddf4ff", danger="#cf222e",
        surface="#ffffff",
    ),
    "dark": dict(
        ink="#e6edf3", muted="#9198a1", rule="#3d444d",
        accent="#4493f8", accent_soft="#121d2f", danger="#f85149",
        surface="#0d1117",
    ),
}

MONO = "ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace"
SANS = "-apple-system,BlinkMacSystemFont,Segoe UI,Noto Sans,Helvetica,Arial,sans-serif"

# Les cinq étapes de la chaîne, dans l'ordre où elles s'exécutent.
STAGES = [
    ("4 RSS feeds", "TechCrunch, Verge,\nTom's, Wired"),
    ("dedupe", "in-memory cache"),
    ("dedupe", "WordPress API"),
    ("draft + cover", "Gemini 2.5 Pro\n+ Flash"),
    ("review", "Telegram"),
]

BOX_W, BOX_H, GAP = 128, 52, 22
X0, Y0 = 12, 26


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size, fill, family=SANS, weight="400", anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>')


def build(t):
    c = THEMES[t]
    o = []
    o.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" '
        f'aria-label="Editorial pipeline: four RSS feeds, two deduplication '
        f'stages, an LLM drafting step, then a human review gate with three '
        f'outcomes - publish, draft, or cancel, which deletes the uploaded image.">'
    )
    # Marqueur de flèche, une définition réutilisée par tous les connecteurs.
    o.append(
        f'<defs><marker id="a" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" '
        f'markerHeight="6" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="{c["rule"]}"/>'
        f'</marker></defs>'
    )

    # --- les cinq étapes ---------------------------------------------
    for i, (titre, sous) in enumerate(STAGES):
        x = X0 + i * (BOX_W + GAP)
        dernier = i == len(STAGES) - 1
        trait = c["accent"] if dernier else c["rule"]
        fond = c["accent_soft"] if dernier else "none"
        largeur = "1.5" if dernier else "1"
        o.append(
            f'<rect x="{x}" y="{Y0}" width="{BOX_W}" height="{BOX_H}" rx="6" '
            f'fill="{fond}" stroke="{trait}" stroke-width="{largeur}"/>'
        )
        o.append(text(x + BOX_W / 2, Y0 + 22, titre, 13,
                      c["accent"] if dernier else c["ink"],
                      weight="600", anchor="middle"))
        for j, ligne in enumerate(sous.split("\n")):
            o.append(text(x + BOX_W / 2, Y0 + 36 + j * 12.5, ligne, 9.5,
                          c["muted"], family=MONO, anchor="middle"))

        # Connecteur vers l'étape suivante.
        if not dernier:
            x1 = x + BOX_W
            o.append(
                f'<line x1="{x1 + 3}" y1="{Y0 + BOX_H / 2}" x2="{x1 + GAP - 4}" '
                f'y2="{Y0 + BOX_H / 2}" stroke="{c["rule"]}" stroke-width="1.2" '
                f'marker-end="url(#a)"/>'
            )

    # --- sorties de rejet sous les deux barrières ---------------------
    # Ce qui est refusé compte autant que ce qui passe : c'est la seule raison
    # d'être des deux étages.
    for i in (1, 2):
        cx = X0 + i * (BOX_W + GAP) + BOX_W / 2
        o.append(
            f'<path d="M{cx} {Y0 + BOX_H} L{cx} {Y0 + BOX_H + 22}" '
            f'stroke="{c["rule"]}" stroke-width="1.2" stroke-dasharray="3 3" '
            f'marker-end="url(#a)"/>'
        )
    o.append(text(X0 + BOX_W + GAP + BOX_W / 2, Y0 + BOX_H + 40,
                  "already covered", 10, c["muted"], family=MONO, anchor="middle"))
    o.append(text(X0 + 2 * (BOX_W + GAP) + BOX_W / 2, Y0 + BOX_H + 40,
                  "already published", 10, c["muted"], family=MONO, anchor="middle"))
    o.append(text(X0 + 1.5 * (BOX_W + GAP) + BOX_W / 2, Y0 + BOX_H + 56,
                  "nothing is written twice", 10, c["muted"], anchor="middle"))

    # --- les trois issues, sous la porte humaine ----------------------
    gx = X0 + 4 * (BOX_W + GAP)
    issues = [("publish", c["accent"]), ("draft", c["muted"]), ("cancel", c["danger"])]
    spine = gx - 16          # colonne verticale, a gauche des pastilles
    y_haut = Y0 + BOX_H + 12
    ys = [Y0 + BOX_H + 22 + i * 30 for i in range(3)]

    # Une seule descente, puis des embranchements courts. Un trait par issue
    # traverserait les pastilles precedentes : c'est exactement ce que la
    # premiere version faisait.
    o.append(
        f'<path d="M{gx + BOX_W / 2} {Y0 + BOX_H} L{gx + BOX_W / 2} {y_haut} '
        f'L{spine} {y_haut} L{spine} {ys[-1] + 12}" '
        f'stroke="{c["rule"]}" stroke-width="1.2" fill="none"/>'
    )

    for (nom, couleur), y in zip(issues, ys):
        o.append(
            f'<line x1="{spine}" y1="{y + 12}" x2="{gx - 3}" y2="{y + 12}" '
            f'stroke="{c["rule"]}" stroke-width="1.2"/>'
        )
        o.append(
            f'<rect x="{gx}" y="{y}" width="{BOX_W}" height="24" rx="12" '
            f'fill="none" stroke="{couleur}" stroke-width="1"/>'
        )
        o.append(text(gx + BOX_W / 2, y + 16, nom, 11.5, couleur,
                      family=MONO, weight="500", anchor="middle"))

    # Le détail qui fait la différence entre une chaîne qui marche et une
    # chaîne qu'on peut laisser tourner. Ancré assez a gauche pour ne pas
    # toucher la colonne verticale.
    o.append(text(spine - 14, ys[2] + 7, "deletes the uploaded image", 10,
                  c["muted"], family=MONO, anchor="end"))
    o.append(text(spine - 14, ys[2] + 22, "so no orphan media piles up", 10,
                  c["muted"], anchor="end"))

    o.append("</svg>")
    return "\n".join(o) + "\n"


for nom in THEMES:
    chemin = f"pipeline-{nom}.svg"
    io.open(chemin, "w", encoding="utf-8").write(build(nom))
    print("ecrit:", chemin)
