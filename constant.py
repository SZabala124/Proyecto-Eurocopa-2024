IVA = 16
PANEL_OPTIONS = {
    "default": {
        "panel": {
            "height": 30,
            "width": 200,
            "title_align": "center",
        },
        "min_lines": 10,
        "max_lines": 20,
    },
    "users": {
        "panel": {
            "height": None,
            "width": 80,
            "title_align": "center",
        },
        "min_lines": 5,
        "max_lines": 15,
    },
    "customers": {
        "panel": {
            "height": None,
            "width": 80,
            "title_align": "center",
        },
        "min_lines": 5,
        "max_lines": 15,
    },
    "tickets": {
        "panel": {
            "height": None,
            "width": 80,
            "title_align": "center",
        },
        "min_lines": 8,
        "max_lines": 20,
    },
    "matches": {
        "panel": {
            "height": None,
            "width": 108,
            "title_align": "center",
        },
        "min_lines": 8,
        "max_lines": 20,
    },
    "stadiums": {
        "panel": {
            "height": None,
            "width": None,
            "title_align": "center",
        },
        "min_lines": 4,
        "max_lines": 20,
    },
    "security": {
        "panel": {
            "height": 15,
            "width": 80,
            "title_align": "center",
        },
        "min_lines": 3,
        "max_lines": 10,
    },
    "products": {
        "panel": {
            "height": None,
            "width": 80,
            "title_align": "center",
        },
        "min_lines": 8,
        "max_lines": 20,
    },
    "reports": {
        "panel": {
            "height": None,
            "width": 120,
            "title_align": "center",
        },
        "min_lines": 8,
        "max_lines": 20,
    },
}


USER_ACCESS_BY_TYPE = {
    None: {
        "main_menu": ["1", "s"],
    },
    "admin": {
        "main_menu": ["2", "3", "4", "5", "6", "7", "8", "9", "10", "s"],
    },
    "seller": {
        "main_menu": ["4", "5", "7", "9", "10", "s"],
    },
    "security": {
        "main_menu": ["6", "9", "10", "s"],
    },
}
