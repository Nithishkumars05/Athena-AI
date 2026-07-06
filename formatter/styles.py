from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_LINE_SPACING
from docx.enum.section import WD_SECTION


def apply_document_style(doc):
    """
    Apply global document formatting.
    """

    # --------------------------
    # Page Margins
    # --------------------------

    for section in doc.sections:
        section.top_margin = Pt(72)
        section.bottom_margin = Pt(72)
        section.left_margin = Pt(72)
        section.right_margin = Pt(72)

    # --------------------------
    # Normal Style
    # --------------------------

    normal = doc.styles["Normal"]

    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)

    # Force Word to use Times New Roman
    normal.element.rPr.rFonts.set(
        qn("w:eastAsia"),
        "Times New Roman"
    )

    normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    normal.paragraph_format.space_after = Pt(6)

    # --------------------------
    # Heading 1
    # --------------------------

    heading1 = doc.styles["Heading 1"]

    heading1.font.name = "Times New Roman"
    heading1.font.size = Pt(18)
    heading1.font.bold = True

    heading1.element.rPr.rFonts.set(
        qn("w:eastAsia"),
        "Times New Roman"
    )

    # --------------------------
    # Heading 2
    # --------------------------

    heading2 = doc.styles["Heading 2"]

    heading2.font.name = "Times New Roman"
    heading2.font.size = Pt(16)
    heading2.font.bold = True

    heading2.element.rPr.rFonts.set(
        qn("w:eastAsia"),
        "Times New Roman"
    )

    # --------------------------
    # Heading 3
    # --------------------------

    heading3 = doc.styles["Heading 3"]

    heading3.font.name = "Times New Roman"
    heading3.font.size = Pt(14)
    heading3.font.bold = True

    heading3.element.rPr.rFonts.set(
        qn("w:eastAsia"),
        "Times New Roman"
    )