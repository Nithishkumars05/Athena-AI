from ui_new.theme import Theme

QSS = f"""

/* -------------------------------------------------
   GLOBAL
------------------------------------------------- */

QWidget {{
    background-color: {Theme.BG};
    color: {Theme.TEXT};
    font-family: "Segoe UI";
    font-size: 13px;
}}


/* -------------------------------------------------
   CARDS
------------------------------------------------- */

QFrame#Card {{
    background-color: {Theme.SURFACE};
    border: 1px solid {Theme.BORDER};
    border-radius: 16px;
}}

QFrame#Card:hover {{
    border: 1px solid {Theme.ACCENT};
}}


/* -------------------------------------------------
   BUTTONS
------------------------------------------------- */

QPushButton {{
    background-color: {Theme.ACCENT};
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 18px;
    font-size: 13px;
    font-weight: 600;
}}

QPushButton:hover {{
    background-color: {Theme.ACCENT_HOVER};
}}

QPushButton:pressed {{
    background-color: {Theme.ACCENT};
}}


/* -------------------------------------------------
   INPUT BOXES
------------------------------------------------- */

QLineEdit,
QTextEdit {{
    background-color: {Theme.SURFACE};
    border: 1px solid {Theme.BORDER};
    border-radius: 10px;
    padding: 10px;
    color: {Theme.TEXT};
}}

QLineEdit:focus,
QTextEdit:focus {{
    border: 1px solid {Theme.ACCENT};
}}


/* -------------------------------------------------
   LABELS
------------------------------------------------- */

QLabel#Title {{
    font-size: 24px;
    font-weight: bold;
    color: {Theme.TEXT};
}}

QLabel#Subtitle {{
    font-size: 13px;
    color: {Theme.TEXT_SECONDARY};
}}


/* -------------------------------------------------
   SCROLLBAR
------------------------------------------------- */

QScrollArea {{
    border: none;
    background: transparent;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
}}

QScrollBar::handle:vertical {{
    background: {Theme.BORDER};
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {Theme.TEXT_SECONDARY};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    background: transparent;
}}

"""