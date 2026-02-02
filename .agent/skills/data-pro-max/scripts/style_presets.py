"""
Visualization Style Presets for Data Pro Max

Pre-configured matplotlib/seaborn styles for professional output.
Usage:
    from style_presets import apply_style
    apply_style('executive')
"""

import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import csv

STYLES_FILE = Path(__file__).parent.parent / "data" / "visualization_styles.csv"


def load_styles() -> dict:
    """Load visualization styles from CSV."""
    styles = {}
    with open(STYLES_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            styles[row["style_id"]] = row
    return styles


def apply_style(style_id: str = "executive") -> None:
    """
    Apply a predefined visualization style.
    
    Args:
        style_id: Style identifier (executive, academic, dashboard, etc.)
    """
    styles = load_styles()
    
    if style_id not in styles:
        available = ", ".join(styles.keys())
        raise ValueError(f"Unknown style '{style_id}'. Available: {available}")
    
    style = styles[style_id]
    
    # Apply matplotlib style
    mpl_style = style.get("matplotlib_style", "seaborn-whitegrid")
    try:
        plt.style.use(mpl_style)
    except OSError:
        plt.style.use("seaborn-v0_8-whitegrid")  # Fallback for newer matplotlib
    
    # Apply seaborn context
    context = style.get("seaborn_context", "notebook")
    sns.set_context(context)
    
    # Configure figure defaults
    figsize = style.get("figsize_default", "10x6")
    width, height = map(float, figsize.split("x"))
    dpi = int(style.get("dpi", 150))
    
    plt.rcParams.update({
        "figure.figsize": (width, height),
        "figure.dpi": dpi,
        "axes.spines.top": style.get("spine_style") == "full",
        "axes.spines.right": style.get("spine_style") == "full",
        "axes.grid": style.get("grid_style") != "hidden",
        "legend.loc": style.get("legend_position", "right"),
    })
    
    print(f"✓ Applied style: {style['name']} ({style.get('best_for', '')})")


def list_styles() -> None:
    """Print available visualization styles."""
    styles = load_styles()
    print("\n📊 Available Visualization Styles:\n")
    print(f"{'ID':<15} {'Name':<25} {'Best For'}")
    print("-" * 70)
    for sid, s in styles.items():
        print(f"{sid:<15} {s['name']:<25} {s.get('best_for', '')[:30]}")


def get_style_config(style_id: str) -> dict:
    """Get raw style configuration as dictionary."""
    styles = load_styles()
    return styles.get(style_id, {})


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Visualization Style Presets")
    parser.add_argument("--list", action="store_true", help="List available styles")
    parser.add_argument("--apply", type=str, help="Apply a style by ID")
    
    args = parser.parse_args()
    
    if args.list:
        list_styles()
    elif args.apply:
        apply_style(args.apply)
    else:
        list_styles()
