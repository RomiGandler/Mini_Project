# Dictionary defining parameter limits and defaults for letter deformation
# For each letter (A, B, C, F, X, W), we define parameters with:
# 1. Minimum value (min)
# 2. Maximum value (max)
# 3. Default value (default)

PARAM_CONFIG = {
    'A': {
        'base_width_factor': {'min': 1.0, 'max': 1.8, 'default': 1.0},
        'top_width':         {'min': 0,   'max': 100,  'default': 0},
        'crossbar_h_shift':  {'min': -30,   'max': 40,  'default': 0},
        'shear_x':           {'min': 0,   'max': 35,  'default': 0},
        'thickness':         {'min': 6,   'max': 18,  'default': 6}
    },
    'B': {
        'width_factor':      {'min': 0.5, 'max': 1.0, 'default': 1.0},
        'waist_y_shift':     {'min': 0,   'max': 40,  'default': 0},
        'rotation_deg':      {'min': -30, 'max': 0,   'default': 0},
        'vertical_squash':   {'min': 0.4, 'max': 1.0, 'default': 1.0},
        'thickness':         {'min': 6,   'max': 18,  'default': 6}
    },
    'C': {
        'cut_top':           {'min': -60, 'max': 40,  'default': 40},
        'vertical_squash':   {'min': 0.45,'max': 1.0, 'default': 1.0},
        'rotation_deg':      {'min': 0,   'max': 45,  'default': 0},
        'thickness':         {'min': 6,   'max': 18,  'default': 6}
    },
    'F': {
        'bar_length':        {'min': 1.0, 'max': 2.0, 'default': 1.0},
        'middle_bar_shift':  {'min': -30, 'max': 40,  'default': 0},
        'shear_x':           {'min': -30, 'max': 30,  'default': 0},
        'spine_height':      {'min': 0.6, 'max': 1.2, 'default': 1.0},
        'thickness':         {'min': 6,   'max': 18,  'default': 6}
    },
    'X': {
        'cross_ratio':       {'min': 0.3, 'max': 0.7, 'default': 0.5},
        'spread_angle':      {'min': -30, 'max': 30,  'default': 0},
        'rotation_deg':      {'min': -30, 'max': 30,  'default': 0},
        'asymmetry':         {'min': -30, 'max': 30,  'default': 0},
        'thickness':         {'min': 6,   'max': 18,  'default': 6}
    },
    'W': {
        'peak_depth':        {'min': 0.5, 'max': 0.9, 'default': 0.7},
        'width_factor':      {'min': 0.3, 'max': 1.4, 'default': 1.0},
        'middle_height':     {'min': 0.3, 'max': 1.0, 'default': 0.5},
        'shear_x':           {'min': -25, 'max': 25,  'default': 0},
        'thickness':         {'min': 6,   'max': 18,  'default': 6}
    }
}

def get_limits(letter, param):
    """Helper function to retrieve limits in a convenient way"""
    if letter in PARAM_CONFIG and param in PARAM_CONFIG[letter]:
        return PARAM_CONFIG[letter][param]
    return None

def get_all_letters():
    """Returns a list of all available letters"""
    return list(PARAM_CONFIG.keys())
