"""
DataPro Styles Module - Visualization style presets.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class StylePreset:
    """A visualization style preset."""
    name: str
    font_title: str
    font_body: str
    figsize: tuple
    dpi: int
    background: str
    grid: bool
    palette_id: str
    best_for: str
    
    
# Professional style presets
PRESETS = {
    "professional": StylePreset(
        name="Professional",
        font_title="Arial",
        font_body="Arial",
        figsize=(10, 6),
        dpi=150,
        background="white",
        grid=True,
        palette_id="neutral_blue",
        best_for="Business reports, presentations",
    ),
    "tufte": StylePreset(
        name="Tufte",
        font_title="Georgia",
        font_body="Georgia",
        figsize=(7, 4.5),
        dpi=300,
        background="white",
        grid=False,
        palette_id="tufte_dense",
        best_for="Edward Tufte style high data-ink ratio plots",
    ),
    "academic": StylePreset(
        name="Academic",
        font_title="Times New Roman",
        font_body="Times New Roman", 
        figsize=(8, 6),
        dpi=300,
        background="white",
        grid=False,
        palette_id="neutral_gray",
        best_for="Research papers, theses",
    ),
    "dashboard": StylePreset(
        name="Dashboard",
        font_title="Inter",
        font_body="Inter",
        figsize=(12, 8),
        dpi=100,
        background="#1e1e1e",
        grid=True,
        palette_id="tech_vibrant",
        best_for="Interactive dashboards, dark mode",
    ),
    "presentation": StylePreset(
        name="Presentation",
        font_title="Montserrat",
        font_body="Open Sans",
        figsize=(14, 8),
        dpi=100,
        background="white",
        grid=False,
        palette_id="corporate_blue",
        best_for="Slide decks, presentations",
    ),
    "survey": StylePreset(
        name="Survey Report",
        font_title="Roboto",
        font_body="Roboto",
        figsize=(10, 6),
        dpi=150,
        background="white",
        grid=True,
        palette_id="survey_classic",
        best_for="Survey analysis reports",
    ),
}


class StylePresets:
    """Manage and apply visualization style presets."""
    
    def __init__(self):
        self.presets = PRESETS
        self.current = "professional"
    
    def list_presets(self) -> List[str]:
        """List all available preset names."""
        return list(self.presets.keys())
    
    def get_preset(self, name: str) -> Optional[StylePreset]:
        """Get a specific preset by name."""
        return self.presets.get(name)
    
    def set_current(self, name: str) -> bool:
        """Set the current preset."""
        if name in self.presets:
            self.current = name
            return True
        return False
    
    def get_current(self) -> StylePreset:
        """Get the current preset."""
        return self.presets[self.current]
    
    def apply_matplotlib(self, preset_name: Optional[str] = None):
        """Apply preset settings to matplotlib."""
        import matplotlib.pyplot as plt
        
        preset = self.presets.get(preset_name or self.current)
        if not preset:
            return
        
        plt.rcParams.update({
            "font.family": preset.font_body,
            "figure.figsize": preset.figsize,
            "figure.dpi": preset.dpi,
            "axes.facecolor": preset.background,
            "axes.grid": preset.grid,
            "axes.titlesize": 14,
            "axes.labelsize": 12,
        })
    
    def get_figsize(self, preset_name: Optional[str] = None) -> tuple:
        """Get figure size for a preset."""
        preset = self.presets.get(preset_name or self.current)
        return preset.figsize if preset else (10, 6)
    
    def get_dpi(self, preset_name: Optional[str] = None) -> int:
        """Get DPI for a preset."""
        preset = self.presets.get(preset_name or self.current)
        return preset.dpi if preset else 150


@dataclass
class PDFTheme:
    """A theme for PDF reports."""
    name: str
    primary_color: str
    secondary_color: str
    font_main: str
    font_title: str
    titlepage_color: str
    titlepage_text_color: str
    line_spacing: float
    best_for: str


PDF_THEMES = {
    "executive": PDFTheme(
        name="Executive",
        primary_color="1a5276",
        secondary_color="2980b9",
        font_main="Inter",
        font_title="Inter-Bold",
        titlepage_color="1a5276",
        titlepage_text_color="FFFFFF",
        line_spacing=1.3,
        best_for="Professional business reports",
    ),
    "minimalist": PDFTheme(
        name="Minimalist",
        primary_color="232b2b",
        secondary_color="333333",
        font_main="Helvetica",
        font_title="Helvetica-Bold",
        titlepage_color="FFFFFF",
        titlepage_text_color="232b2b",
        line_spacing=1.4,
        best_for="Clean, modern documents",
    ),
    "academic": PDFTheme(
        name="Academic",
        primary_color="000000",
        secondary_color="000000",
        font_main="Times New Roman",
        font_title="Times New Roman",
        titlepage_color="FFFFFF",
        titlepage_text_color="000000",
        line_spacing=1.5,
        best_for="Research papers and technical journals",
    ),
    "dark": PDFTheme(
        name="Dark Mode",
        primary_color="3498db",
        secondary_color="9b59b6",
        font_main="Inter",
        font_title="Inter-Bold",
        titlepage_color="1e1e1e",
        titlepage_text_color="FFFFFF",
        line_spacing=1.3,
        best_for="Tech reports and digital dashboard exports",
    ),
    "tufte": PDFTheme(
        name="Tufte",
        primary_color="111111",
        secondary_color="333333",
        font_main="Palatino",
        font_title="Palatino-Bold",
        titlepage_color="FFFFFF",
        titlepage_text_color="111111",
        line_spacing=1.4,
        best_for="Edward Tufte handouts style reports",
    ),
}


# Global instance
_styles = StylePresets()

def get_styles() -> StylePresets:
    """Get the global StylePresets instance."""
    return _styles


def set_tufte_theme(ax=None):
    """
    Applies Edward Tufte's data visualization principles to matplotlib.
    Removes top and right spines, minimizes gridlines, sets serif typography.
    """
    try:
        import matplotlib.pyplot as plt
        
        # Configure global parameters
        plt.rcParams.update({
            "font.family": "serif",
            "font.serif": ["Georgia", "Palatino", "Times New Roman", "DejaVu Serif"],
            "figure.figsize": (7, 4.5),
            "figure.dpi": 300,
            "axes.facecolor": "white",
            "figure.facecolor": "white",
            "axes.grid": False,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": True,
            "axes.spines.bottom": True,
            "axes.edgecolor": "#111111",
            "axes.linewidth": 0.6,
            "xtick.major.size": 4,
            "ytick.major.size": 4,
            "xtick.color": "#111111",
            "ytick.color": "#111111",
            "text.color": "#111111",
            "axes.labelcolor": "#111111",
        })
        
        if ax:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_linewidth(0.6)
            ax.spines['bottom'].set_linewidth(0.6)
            ax.tick_params(axis='both', which='both', length=4, width=0.6, colors='#111111')
    except ImportError:
        pass

