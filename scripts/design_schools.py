#!/usr/bin/env python3
"""Data-Pro-Skill Data Design Schools Registry & Resolution Engine.

Defines the 5 canonical Data Design Schools available during `/dps-setup`,
`/dps-grill`, and `/dps-export`:

  1. tufte     — Edward Tufte (Classic Data-Ink, Booktabs & Floating Sidenotes) [Default]
  2. few       — Stephen Few (Perceptual BI Grid, Bullet Graphs & Threshold Alerts)
  3. knaflic   — Cole Nussbaumer Knaflic (Storytelling with Data: Grey Context + Focal Accent)
  4. swiss     — Swiss Grid & Jacques Bertin (International Typographic Grid & Semiology Matrix)
  5. editorial — The Economist / Financial Times (Editorial Kicker, Crimson Rule & Lollipop Charts)
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

SCHOOLS = {
    "tufte": {
        "id": "tufte",
        "number": 1,
        "name": "Edward Tufte (Classic Data-Ink & Sidenote School)",
        "short_name": "Edward Tufte",
        "founder": "Edward R. Tufte (1983, The Visual Display of Quantitative Information)",
        "css_file": "tufte.css",
        "primary_chart_type": "cleveland_dot",
        "tagline_en": "Ivory paper (#fffff8), Palatino serif, 58%/36% floating right Margin Notes, Booktabs tables & Cleveland dot plots with 95% CI whiskers.",
        "tagline_pt": "Papel marfim (#fffff8), serifa Palatino, coluna 58%/36% com Notas de Margem flutuantes, tabelas Booktabs e dot plots de Cleveland (IC 95%).",
        "best_for_en": "Academic research, scientific studies, public policy, and long-form analytical reports",
        "best_for_pt": "Pesquisa acadêmica, estudos científicos, políticas públicas e relatórios analíticos densos",
        "kicker_en": "EDWARD TUFTE ANALYTICAL STANDARD · DATA-INK EDITION",
        "kicker_pt": "PADRÃO ANALÍTICO EDWARD TUFTE · EDIÇÃO DATA-INK",
        "note_label_en": "§{n}",
        "note_label_pt": "§{n}",
        "footer_stamp_en": "Edward Tufte Data-Ink Standard",
        "footer_stamp_pt": "Padrão Edward Tufte Data-Ink",
        "layout_mode": "asymmetric_sidenotes",
        "palette": {
            "paper": "#fffff8",
            "paper_print": "#ffffff",
            "ink": "#111111",
            "muted": "#52524e",
            "primary": "#1b4f72",
            "secondary": "#555555",
            "accent": "#1c3d5a",
            "alert_neg": "#a61c1c",
            "alert_pos": "#1b4f72",
            "neutral_bar": "#c8c8be",
            "grid_line": "#e6e6de",
            "note_bg": "#f7f7ee",
            "card_bg": "#fafaf2",
        },
        "fonts": {
            "heading": "Georgia, Palatino, 'Palatino Linotype', serif",
            "body": "Georgia, Palatino, 'Palatino Linotype', serif",
            "ui": "-apple-system, BlinkMacSystemFont, 'Gill Sans', 'Helvetica Neue', sans-serif",
            "mono": "Consolas, 'Liberation Mono', Menlo, monospace",
        },
    },
    "few": {
        "id": "few",
        "number": 2,
        "name": "Stephen Few (Perceptual Dashboard & Bullet-Graph School)",
        "short_name": "Stephen Few",
        "founder": "Stephen Few (2004, Show Me the Numbers; 2006, Information Dashboard Design)",
        "css_file": "few.css",
        "primary_chart_type": "bullet_graph",
        "tagline_en": "Perceptual full-width BI grid (#f8fafc), humanist sans-serif, Bullet Graphs with qualitative bands & target lines, and inline threshold alerts.",
        "tagline_pt": "Grid perceptual de largura total (#f8fafc), sem serifa humanista, Bullet Graphs com faixas qualitativas/metas e alertas de limiar inline.",
        "best_for_en": "Operational intelligence, KPI tracking, business intelligence (BI) reviews, and multi-metric benchmarking",
        "best_for_pt": "Inteligência operacional, monitoramento de KPIs, revisões de BI e benchmarking quantitativo",
        "kicker_en": "STEPHEN FEW PERCEPTUAL BI STANDARD · SHOW ME THE NUMBERS",
        "kicker_pt": "PADRÃO PERCEPTUAL STEPHEN FEW · INTELIGÊNCIA DE DADOS",
        "note_label_en": "PERCEPTUAL DIAGNOSTIC #{n}",
        "note_label_pt": "DIAGNÓSTICO PERCEPTUAL #{n}",
        "footer_stamp_en": "Stephen Few Perceptual BI Standard",
        "footer_stamp_pt": "Padrão Perceptual Stephen Few",
        "layout_mode": "full_width_perceptual",
        "palette": {
            "paper": "#f8fafc",
            "paper_print": "#ffffff",
            "ink": "#0f172a",
            "muted": "#475569",
            "primary": "#0f172a",
            "secondary": "#64748b",
            "accent": "#0d9488",
            "alert_neg": "#dc2626",
            "alert_pos": "#0d9488",
            "neutral_bar": "#cbd5e1",
            "grid_line": "#e2e8f0",
            "note_bg": "#f1f5f9",
            "card_bg": "#ffffff",
            "band_poor": "#e2e8f0",
            "band_fair": "#cbd5e1",
            "band_good": "#94a3b8",
        },
        "fonts": {
            "heading": "'Inter', 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            "body": "'Inter', 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            "ui": "'Inter', 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            "mono": "'JetBrains Mono', Consolas, Menlo, monospace",
        },
    },
    "knaflic": {
        "id": "knaflic",
        "number": 3,
        "name": "Cole Nussbaumer Knaflic (Storytelling with Data / Preattentive Focus School)",
        "short_name": "Cole Knaflic (SWD)",
        "founder": "Cole Nussbaumer Knaflic (2015, Storytelling with Data)",
        "css_file": "knaflic.css",
        "primary_chart_type": "swd_focus_bar",
        "tagline_en": "Decluttered white canvas (#ffffff), context pushed to muted grey (#cbd5e1) with one bold preattentive focal color (#1e40af / #ea580c) & Action-Title callouts.",
        "tagline_pt": "Fundo branco limpo (#ffffff), contexto em cinza suave (#cbd5e1) com uma única cor focal pré-atentiva (#1e40af / #ea580c) e títulos de ação executivos.",
        "best_for_en": "C-level executive presentations, stakeholder alignment, strategy briefs, and Monday-morning action plans",
        "best_for_pt": "Apresentações executivas C-level, alinhamento de stakeholders, planos estratégicos e decisões de negócio",
        "kicker_en": "STORYTELLING WITH DATA · PREATTENTIVE EXECUTIVE EDITION",
        "kicker_pt": "STORYTELLING WITH DATA · EDIÇÃO EXECUTIVA PRÉ-ATENTIVA",
        "note_label_en": "💡 KEY TAKEAWAY #{n}",
        "note_label_pt": "💡 LIÇÃO EXECUTIVA #{n}",
        "footer_stamp_en": "Cole Knaflic Storytelling with Data Standard",
        "footer_stamp_pt": "Padrão Storytelling with Data (Cole Knaflic)",
        "layout_mode": "executive_single_column",
        "palette": {
            "paper": "#ffffff",
            "paper_print": "#ffffff",
            "ink": "#1e293b",
            "muted": "#64748b",
            "primary": "#1e40af",
            "secondary": "#94a3b8",
            "accent": "#1e40af",
            "alert_neg": "#ea580c",
            "alert_pos": "#1e40af",
            "neutral_bar": "#cbd5e1",
            "grid_line": "#f1f5f9",
            "note_bg": "#eff6ff",
            "card_bg": "#f8fafc",
        },
        "fonts": {
            "heading": "'Montserrat', 'Plus Jakarta Sans', 'Helvetica Neue', Inter, sans-serif",
            "body": "'Open Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
            "ui": "'Inter', 'Open Sans', -apple-system, BlinkMacSystemFont, sans-serif",
            "mono": "Consolas, 'Liberation Mono', Menlo, monospace",
        },
    },
    "swiss": {
        "id": "swiss",
        "number": 4,
        "name": "Swiss Grid & Jacques Bertin (International Typographic & Semiology School)",
        "short_name": "Swiss Grid / Bertin",
        "founder": "Josef Müller-Brockmann (1981, Grid Systems) & Jacques Bertin (1967, Sémiologie Graphique)",
        "css_file": "swiss.css",
        "primary_chart_type": "swiss_lollipop",
        "tagline_en": "Exposed architectural modular grid (1px/4px solid #0a0a0a), Neo-Grotesque typography, and Bertin high-contrast retinal variables (Vermilion #e63946 & Cobalt #1d3557).",
        "tagline_pt": "Grid modular arquitetônico exposto (1px/4px #0a0a0a), tipografia Neo-Grotesca e variáveis retinianas de Jacques Bertin (Vermelho #e63946 e Cobalto #1d3557).",
        "best_for_en": "Design-forward research manifestos, urban/demographic studies, multivariate matrices, and architectural compendia",
        "best_for_pt": "Manifestos de pesquisa, estudos urbanos/demográficos, matrizes multivariadas e compêndios técnicos",
        "kicker_en": "00 // SWISS INTERNATIONAL GRID & BERTIN SEMIOLOGY SYSTEM",
        "kicker_pt": "00 // SISTEMA DE GRID SUÍÇO & SEMIOLOGIA DE BERTIN",
        "note_label_en": "[§{n:02d} // GRID MODULE]",
        "note_label_pt": "[§{n:02d} // MÓDULO DE GRID]",
        "footer_stamp_en": "Swiss International Grid · Jacques Bertin Semiology Standard",
        "footer_stamp_pt": "Grid Internacional Suíço · Padrão Semiologia de Bertin",
        "layout_mode": "modular_swiss_grid",
        "palette": {
            "paper": "#f5f5f0",
            "paper_print": "#ffffff",
            "ink": "#0a0a0a",
            "muted": "#40403c",
            "primary": "#1d3557",
            "secondary": "#0a0a0a",
            "accent": "#e63946",
            "alert_neg": "#e63946",
            "alert_pos": "#1d3557",
            "neutral_bar": "#a8a8a0",
            "grid_line": "#d4d4cc",
            "note_bg": "#ffffff",
            "card_bg": "#ffffff",
        },
        "fonts": {
            "heading": "'Helvetica Neue', Helvetica, 'Inter', 'Liberation Sans', Arial, sans-serif",
            "body": "'Helvetica Neue', Helvetica, 'Inter', 'Liberation Sans', Arial, sans-serif",
            "ui": "'Helvetica Neue', Helvetica, 'Inter', Arial, sans-serif",
            "mono": "'JetBrains Mono', Consolas, 'Liberation Mono', monospace",
        },
    },
    "editorial": {
        "id": "editorial",
        "number": 5,
        "name": "The Economist / Financial Times Editorial (Data Journalism School)",
        "short_name": "Economist / FT Editorial",
        "founder": "The Economist Style Guide & Financial Times Visual Vocabulary (Alan Smith)",
        "css_file": "editorial.css",
        "primary_chart_type": "editorial_lollipop",
        "tagline_en": "Warm editorial newsprint (#fcf8f2), signature crimson top bar (#e3120b), Kicker + Headline + Standfirst hierarchy, and horizontal lollipop/range charts.",
        "tagline_pt": "Papel editorial aquecido (#fcf8f2), barra superior carmesim (#e3120b), hierarquia Kicker + Manchete + Subtítulo e gráficos lollipop jornalísticos.",
        "best_for_en": "Market research publications, public opinion polling, industry benchmark reports, and external press deliverables",
        "best_for_pt": "Publicações de pesquisa de mercado, pesquisas de opinião, benchmarks setoriais e relatórios para imprensa/clientes",
        "kicker_en": "SPECIAL BRIEFING · DATA JOURNALISM & VISUAL VOCABULARY",
        "kicker_pt": "RELATÓRIO ESPECIAL · JORNALISMO DE DADOS & VOCABULÁRIO VISUAL",
        "note_label_en": "EDITORIAL BRIEF #{n}",
        "note_label_pt": "NOTA EDITORIAL #{n}",
        "footer_stamp_en": "The Economist / FT Editorial Data Journalism Standard",
        "footer_stamp_pt": "Padrão Editorial The Economist / FT de Jornalismo de Dados",
        "layout_mode": "editorial_column",
        "palette": {
            "paper": "#fcf8f2",
            "paper_print": "#ffffff",
            "ink": "#1a1817",
            "muted": "#59544f",
            "primary": "#005689",
            "secondary": "#59544f",
            "accent": "#e3120b",
            "alert_neg": "#e3120b",
            "alert_pos": "#005689",
            "neutral_bar": "#cec6b9",
            "grid_line": "#e2dcd3",
            "note_bg": "#f4ece1",
            "card_bg": "#fffdf9",
        },
        "fonts": {
            "heading": "'IBM Plex Sans', 'Franklin Gothic Medium', 'Helvetica Neue', Inter, sans-serif",
            "body": "'Merriweather', 'Charter', Georgia, 'Times New Roman', serif",
            "ui": "'IBM Plex Sans', 'Helvetica Neue', Inter, sans-serif",
            "mono": "Consolas, 'Liberation Mono', monospace",
        },
    },
}

SCHOOL_ORDER = ["tufte", "few", "knaflic", "swiss", "editorial"]

SCHOOL_ALIASES = {
    # 1. Edward Tufte
    "1": "tufte",
    "tufte": "tufte",
    "edward-tufte": "tufte",
    "edward_tufte": "tufte",
    "edward tufte": "tufte",
    "classic": "tufte",
    "sidenote": "tufte",
    "sidenotes": "tufte",
    "booktabs": "tufte",
    # 2. Stephen Few
    "2": "few",
    "few": "few",
    "stephen-few": "few",
    "stephen_few": "few",
    "stephen few": "few",
    "perceptual": "few",
    "bullet": "few",
    "bullet-graph": "few",
    "bi": "few",
    "dashboard": "few",
    # 3. Cole Nussbaumer Knaflic (Storytelling with Data)
    "3": "knaflic",
    "knaflic": "knaflic",
    "cole-knaflic": "knaflic",
    "cole_knaflic": "knaflic",
    "cole knaflic": "knaflic",
    "storytelling": "knaflic",
    "storytelling-with-data": "knaflic",
    "storytelling_with_data": "knaflic",
    "swd": "knaflic",
    "executive": "knaflic",
    "mckinsey": "knaflic",
    # 4. Swiss Grid & Jacques Bertin
    "4": "swiss",
    "swiss": "swiss",
    "swiss-grid": "swiss",
    "swiss_grid": "swiss",
    "bertin": "swiss",
    "jacques-bertin": "swiss",
    "jacques_bertin": "swiss",
    "muller-brockmann": "swiss",
    "müller-brockmann": "swiss",
    "international": "swiss",
    "semiology": "swiss",
    "grid": "swiss",
    # 5. The Economist / FT Editorial
    "5": "editorial",
    "editorial": "editorial",
    "economist": "editorial",
    "the-economist": "editorial",
    "the_economist": "editorial",
    "ft": "editorial",
    "financial-times": "editorial",
    "financial_times": "editorial",
    "journalism": "editorial",
    "press": "editorial",
}


def normalize_school(value, default="tufte"):
    """Normalize any school identifier, number, or alias to a canonical school key."""
    if value is None:
        return default
    clean = str(value).strip().lower().strip('"').strip("'")
    if not clean or clean == "auto":
        return default
    if clean in SCHOOLS:
        return clean
    if clean in SCHOOL_ALIASES:
        return SCHOOL_ALIASES[clean]
    # Substring match fallback
    for alias, target in SCHOOL_ALIASES.items():
        if len(alias) >= 3 and alias in clean:
            return target
    return default


def get_school_spec(school_id="tufte"):
    """Return the full specification dictionary for the given school (defaults to Tufte)."""
    canon = normalize_school(school_id, default="tufte")
    return SCHOOLS[canon]


def resolve_css_for_school(school_id="tufte", custom_css_arg=None):
    """Locate the stylesheet path for the selected school."""
    spec = get_school_spec(school_id)
    css_filename = spec["css_file"]

    # If caller passed an explicit .css file that is not just a default directory
    if custom_css_arg:
        p = Path(custom_css_arg)
        if p.is_file() and p.suffix.lower() == ".css":
            # If caller explicitly passed tufte.css by default, swap to the active school's CSS if sibling exists
            if p.name == "tufte.css" and spec["id"] != "tufte":
                sibling = p.parent / css_filename
                if sibling.exists():
                    return sibling
            return p
        if p.is_dir():
            for rel in (f"styles/{css_filename}", css_filename, "styles/tufte.css", "tufte.css"):
                cand = p / rel
                if cand.exists():
                    return cand

    # Check repo / local .dps styles directory
    candidates = [
        REPO_ROOT / "references" / "styles" / css_filename,
        REPO_ROOT / "references" / css_filename,
        Path(".dps") / "references" / "styles" / css_filename,
        Path(".dps") / "references" / css_filename,
        REPO_ROOT / "references" / "styles" / "tufte.css",
    ]
    for cand in candidates:
        if cand.exists():
            return cand
    return None


def _read_json_safe(path):
    try:
        p = Path(path)
        if p.exists() and p.is_file():
            return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        pass
    return None


def resolve_active_school(explicit_school=None, search_dirs=None, md_meta=None, default="tufte"):
    """Resolve the active Data Design School across CLI, frontmatter, setup artifacts, and config.

    Priority order:
      1. Explicit CLI argument (`--school`), if provided and != "auto"
      2. Markdown YAML frontmatter (`design_school` key)
      3. Setup artifacts (`design_school.json`, `setup_manifest.json`, `00_profile.json`)
      4. `clarify_notes.md` in `.dps/outputs/`
      5. Project config (`.dps/config.json` or `config.json`)
      6. `DPS_DESIGN_SCHOOL` environment variable
      7. Canonical default (`"tufte"`)
    """
    # 1. Explicit CLI flag
    if explicit_school and str(explicit_school).strip().lower() not in ("", "auto", "none"):
        return normalize_school(explicit_school, default=default)

    # 2. Markdown YAML frontmatter
    if isinstance(md_meta, dict):
        for k in ("design_school", "school", "style_school"):
            if md_meta.get(k):
                return normalize_school(md_meta[k], default=default)

    # Build candidate search directories
    dirs = []
    if search_dirs:
        for d in search_dirs:
            if d:
                dp = Path(d)
                dirs.extend([dp, dp / "setup", dp.parent, dp.parent / "setup"])
    dirs.extend([
        Path(".dps/outputs/setup"),
        Path(".dps/outputs"),
        Path(".dps"),
        Path("outputs/setup"),
        Path("outputs"),
        Path("."),
    ])

    seen = set()
    unique_dirs = []
    for d in dirs:
        try:
            resolved = d.resolve()
        except Exception:
            resolved = d
        if resolved not in seen:
            seen.add(resolved)
            unique_dirs.append(d)

    # 3. Check setup_manifest.json, 00_profile.json, design_school.json
    for d in unique_dirs:
        for fname in ("design_school.json", "setup_manifest.json", "00_profile.json", "config.json"):
            data = _read_json_safe(d / fname)
            if isinstance(data, dict):
                for key in ("design_school", "school", "default_school"):
                    if data.get(key) and str(data[key]).lower() != "auto":
                        return normalize_school(data[key], default=default)

    # 4. Check clarify_notes.md
    for d in unique_dirs:
        cpath = d / "clarify_notes.md"
        if cpath.exists() and cpath.is_file():
            try:
                txt = cpath.read_text(encoding="utf-8")
                m = re.search(r"(?:design_school|Design School|Escola de Design)\s*[:=]\s*`*([a-zA-Z0-9_-]+)`*", txt, re.IGNORECASE)
                if m:
                    return normalize_school(m.group(1), default=default)
            except Exception:
                pass

    # 5. Environment variable
    env_school = os.environ.get("DPS_DESIGN_SCHOOL")
    if env_school:
        return normalize_school(env_school, default=default)

    return default


def save_school_selection(school_id, output_dir=".dps/outputs/setup", update_project_config=False):
    """Persist the chosen Data Design School to design_school.json (and optionally .dps/config.json)."""
    spec = get_school_spec(school_id)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "design_school": spec["id"],
        "design_school_name": spec["name"],
        "short_name": spec["short_name"],
        "founder": spec["founder"],
        "css_file": spec["css_file"],
        "primary_chart_type": spec["primary_chart_type"],
        "tagline_en": spec["tagline_en"],
        "tagline_pt": spec["tagline_pt"],
    }
    school_file = out_dir / "design_school.json"
    school_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    if update_project_config:
        dps_dir = Path(".dps")
        if dps_dir.exists() or out_dir.parts and ".dps" in out_dir.parts:
            cfg_path = dps_dir / "config.json"
            existing = _read_json_safe(cfg_path) or {}
            existing["design_school"] = spec["id"]
            existing["design_school_name"] = spec["name"]
            cfg_path.parent.mkdir(parents=True, exist_ok=True)
            cfg_path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")

    return payload


def format_schools_table_markdown(lang="en"):
    """Return a clean Markdown reference table of all 5 Data Design Schools."""
    is_pt = str(lang).lower().startswith("pt")
    if is_pt:
        lines = [
            "| # | ID (`--school`) | Escola de Design de Dados | Assinatura Visual & Tipográfica | Melhor Para |",
            "| :---: | :--- | :--- | :--- | :--- |",
        ]
        for sid in SCHOOL_ORDER:
            s = SCHOOLS[sid]
            default_tag = " *(Padrão)*" if sid == "tufte" else ""
            lines.append(
                f"| **{s['number']}** | `{s['id']}` | **{s['short_name']}**{default_tag} | {s['tagline_pt']} | {s['best_for_pt']} |"
            )
    else:
        lines = [
            "| # | ID (`--school`) | Data Design School | Visual & Typographic Signature | Best For |",
            "| :---: | :--- | :--- | :--- | :--- |",
        ]
        for sid in SCHOOL_ORDER:
            s = SCHOOLS[sid]
            default_tag = " *(Default)*" if sid == "tufte" else ""
            lines.append(
                f"| **{s['number']}** | `{s['id']}` | **{s['short_name']}**{default_tag} | {s['tagline_en']} | {s['best_for_en']} |"
            )
    return "\n".join(lines)


def interactive_pick_school(default="tufte", lang="en"):
    """Prompt the user in the terminal to pick one of the 5 Data Design Schools on setup."""
    canon_default = normalize_school(default, default="tufte")
    is_pt = str(lang).lower().startswith("pt")

    if is_pt:
        print("\n🎨 Escolha a Escola de Design de Dados para o projeto (/dps-setup & /dps-export):")
    else:
        print("\n🎨 Select a Data Design School for this project (/dps-setup & /dps-export):")

    for sid in SCHOOL_ORDER:
        s = SCHOOLS[sid]
        marker = " [Default]" if sid == canon_default else ""
        desc = s["tagline_pt"] if is_pt else s["tagline_en"]
        print(f"  {s['number']}. {s['short_name']:<24} ({s['id']:<9}) — {desc}{marker}")

    if not sys.stdin:
        return canon_default

    prompt_str = (
        f"\nEscolha [1-5 ou nome, Enter={canon_default}]: "
        if is_pt
        else f"\nChoice [1-5 or name, Enter={canon_default}]: "
    )
    try:
        ans = input(prompt_str).strip()
    except (EOFError, KeyboardInterrupt):
        print("")
        return canon_default

    if not ans:
        return canon_default
    return normalize_school(ans, default=canon_default)


def main():
    parser = argparse.ArgumentParser(description="Data-Pro-Skill Data Design Schools Manager")
    parser.add_argument("--list", action="store_true", help="List all available Data Design Schools")
    parser.add_argument("--pick", action="store_true", help="Interactively pick a Data Design School and save it")
    parser.add_argument("--set", dest="set_school", default=None, help="Set active Data Design School (tufte, few, knaflic, swiss, editorial)")
    parser.add_argument("--resolve", action="store_true", help="Print the currently resolved active Data Design School")
    parser.add_argument("-o", "-d", "--output", default=".dps/outputs/setup", help="Output or search setup directory")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--lang", default="en", choices=["en", "pt"], help="Display language")
    args = parser.parse_args()

    if args.list:
        if args.json:
            print(json.dumps(SCHOOLS, indent=2, ensure_ascii=False))
        else:
            print(format_schools_table_markdown(lang=args.lang))
        return

    if args.pick:
        chosen = interactive_pick_school(default=resolve_active_school(search_dirs=[args.output]), lang=args.lang)
        payload = save_school_selection(chosen, output_dir=args.output, update_project_config=True)
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(f"✓ Data Design School locked: {payload['design_school_name']} (`{payload['design_school']}`)")
        return

    if args.set_school:
        chosen = normalize_school(args.set_school)
        payload = save_school_selection(chosen, output_dir=args.output, update_project_config=True)
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(f"✓ Data Design School set to: {payload['design_school_name']} (`{payload['design_school']}`)")
        return

    if args.resolve:
        active = resolve_active_school(search_dirs=[args.output])
        spec = get_school_spec(active)
        print(json.dumps(spec, indent=2, ensure_ascii=False))
        return

    print(format_schools_table_markdown(lang=args.lang))


if __name__ == "__main__":
    main()
