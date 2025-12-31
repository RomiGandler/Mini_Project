"""
Interactive Letter Deformation Game
===================================
משחק אינטראקטיבי לעיוות אותיות A, B, C
השתמש בסליידרים כדי לשנות את האות בזמן אמת!
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

# ==========================================
# הגדרת טווחי הפרמטרים לכל אות
# ==========================================

PARAMS = {
    'A': [
        ('top_width', 0, 140, 0, 'Top Round'),
        ('crossbar_h_shift', -50, 60, 0, 'Bar Shift'),
        ('base_width_factor', 0.4, 2.0, 1.0, 'Leg Width'),
    ],
    'B': [
        ('waist_y_shift', -40, 50, 0, 'Waist Shift'),
        ('width_factor', 0.4, 2.2, 1.0, 'Width'),
        ('rotation_deg', -35, 35, 0, 'Rotation'),
    ],
    'C': [
        ('cut_top', -40, 100, 40, 'Cut Top'),
        ('cut_bottom', -40, 100, 40, 'Cut Bottom'),
        ('elongation_factor', 0.5, 1.8, 1.0, 'Elongation'),
        ('rotation_deg', -60, 60, 0, 'Rotation'),
    ]
}

DRAW_FUNCS = {
    'A': CanonicalLetters.draw_A,
    'B': CanonicalLetters.draw_B,
    'C': CanonicalLetters.draw_C,
}

# ==========================================
# משתנים גלובליים
# ==========================================

model = LetterSkeleton(size=(200, 200))
current_letter = 'A'
sliders = []
slider_axes = []

# ==========================================
# יצירת הממשק
# ==========================================

fig = plt.figure(figsize=(12, 8))
fig.suptitle("🎮 Interactive Letter Deformation Game", fontsize=18, fontweight='bold')

# אזור התמונה
ax_img = fig.add_axes([0.35, 0.3, 0.45, 0.6])
ax_img.axis('off')

# אזור בחירת אות
ax_radio = fig.add_axes([0.05, 0.6, 0.15, 0.25])
ax_radio.set_title("Choose Letter", fontsize=12)

# יצירת 4 אזורים לסליידרים
slider_positions = [0.22, 0.16, 0.10, 0.04]
for pos in slider_positions:
    ax_slider = fig.add_axes([0.35, pos, 0.45, 0.03])
    slider_axes.append(ax_slider)

# ==========================================
# פונקציות
# ==========================================

def update_image(val=None):
    """מעדכן את התמונה"""
    params = {}
    for i, slider in enumerate(sliders):
        param_info = PARAMS[current_letter][i]
        param_name = param_info[0]
        val = slider.val
        # המרה ל-int אם צריך
        if 'factor' not in param_name:
            val = int(val)
        params[param_name] = val
    
    DRAW_FUNCS[current_letter](model, **params)
    img = model.apply_morphology(thickness=6)
    ax_img.clear()
    ax_img.imshow(img, cmap='gray')
    ax_img.set_title(f"Letter: {current_letter}", fontsize=14)
    ax_img.axis('off')
    fig.canvas.draw_idle()

def create_sliders():
    """יוצר סליידרים לאות הנוכחית"""
    global sliders
    sliders = []
    
    params = PARAMS[current_letter]
    
    for i, ax in enumerate(slider_axes):
        ax.clear()
        if i < len(params):
            param_name, p_min, p_max, p_default, p_label = params[i]
            slider = Slider(ax, f"{p_label}\n[{p_min} to {p_max}]", 
                           p_min, p_max, valinit=p_default)
            slider.on_changed(update_image)
            sliders.append(slider)
            ax.set_visible(True)
        else:
            ax.set_visible(False)

def change_letter(label):
    """מחליף אות"""
    global current_letter
    current_letter = label
    create_sliders()
    update_image()

def reset(event):
    """מאפס לברירת מחדל"""
    params = PARAMS[current_letter]
    for i, slider in enumerate(sliders):
        slider.set_val(params[i][3])  # default value

# ==========================================
# יצירת הממשק
# ==========================================

# כפתורי בחירת אות
radio = RadioButtons(ax_radio, ('A', 'B', 'C'), active=0)
radio.on_clicked(change_letter)

# כפתור Reset
ax_reset = fig.add_axes([0.05, 0.4, 0.15, 0.06])
btn_reset = Button(ax_reset, '🔄 Reset', color='lightgray')
btn_reset.on_clicked(reset)

# הוראות
instructions = """
HOW TO PLAY:

1. Choose a letter
   (A / B / C)

2. Move the sliders

3. Watch the letter
   change in real-time!

[min to max] shows
the allowed range
"""
fig.text(0.02, 0.05, instructions, fontsize=10, family='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# הפעלה ראשונית
create_sliders()
update_image()

plt.show()