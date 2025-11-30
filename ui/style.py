from tkinter import *

# =============================================================
# HOVER EFFECT FOR BUTTONS
# =============================================================
def add_hover(btn, normal_color, hover_color):
    def on_enter(e):
        btn['background'] = hover_color
        btn['cursor'] = "hand2"

    def on_leave(e):
        btn['background'] = normal_color

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


# =============================================================
# THEME ENGINE (Light + Dark Mode)
# =============================================================

theme = {
    "mode": "light",
    "light_bg": "white",
    "light_fg": "#0d0d0d",
    "dark_bg": "#1f1f1f",
    "dark_fg": "#f2f2f2",
}

def toggle_theme(root):
    # Switch theme mode
    if theme["mode"] == "light":
        theme["mode"] = "dark"
    else:
        theme["mode"] = "light"

    apply_theme_to_all(root)


def apply_theme_to_all(widget):
    """Apply theme to widget + all child widgets"""
    
    # Set background + text color if widget supports it
    try:
        if theme["mode"] == "light":
            widget.configure(bg=theme["light_bg"], fg=theme["light_fg"])
        else:
            widget.configure(bg=theme["dark_bg"], fg=theme["dark_fg"])
    except:
        pass  # Some widgets don’t accept bg/fg

    # Recursively apply theme to children
    for child in widget.winfo_children():
        apply_theme_to_all(child)



# =============================================================
# FADE-IN ANIMATION FOR WINDOWS/CARDS
# =============================================================
def fade_in(win, delay=8):
    win.attributes("-alpha", 0.0)
    alpha = 0.0
    step = 0.07

    def _fade():
        nonlocal alpha
        alpha += step
        if alpha <= 1.0:
            win.attributes("-alpha", alpha)
            win.after(delay, _fade)

    _fade()
