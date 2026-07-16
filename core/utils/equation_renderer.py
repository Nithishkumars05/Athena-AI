from docx.oxml import OxmlElement
import re


# -----------------------------
# MAIN FUNCTION
# -----------------------------

def add_equation(paragraph, latex):

    latex = latex.strip()

    latex = latex.strip("$")

    equation = parse_expression(latex)

    paragraph._p.append(equation)



# -----------------------------
# PARSER
# -----------------------------

def parse_expression(expr):

    omath = OxmlElement("m:oMath")


    # Summation
    if "\\sum" in expr:

        return create_sum(expr)


    # Fraction
    if "\\frac" in expr:

        return create_fraction(expr)


    # Square root
    if "\\sqrt" in expr:

        return create_root(expr)


    # Normal equation

    omath.append(
        create_run(
            convert_symbols(expr)
        )
    )

    return omath



# -----------------------------
# SUMMATION
# -----------------------------

def create_sum(expr):

    nary = OxmlElement("m:nary")


    naryPr = OxmlElement("m:naryPr")

    char = OxmlElement("m:chr")
    char.set(
        "{http://schemas.openxmlformats.org/officeDocument/2006/math}val",
        "∑"
    )

    naryPr.append(char)

    nary.append(naryPr)



    # limits

    sub = re.search(
        r"_\{(.+?)\}",
        expr
    )

    sup = re.search(
        r"\^\{(.+?)\}",
        expr
    )


    if sub:

        sub_xml = OxmlElement("m:sub")

        sub_xml.append(
            create_run(sub.group(1))
        )

        nary.append(sub_xml)



    if sup:

        sup_xml = OxmlElement("m:sup")

        sup_xml.append(
            create_run(sup.group(1))
        )

        nary.append(sup_xml)



    expr = re.sub(
        r".*?\}",
        "",
        expr
    )


    e = OxmlElement("m:e")

    e.append(
        create_run(
            convert_symbols(expr)
        )
    )


    nary.append(e)


    return nary



# -----------------------------
# FRACTION
# -----------------------------

def create_fraction(expr):

    f = OxmlElement("m:f")


    match = re.search(
        r"\\frac\{(.*?)\}\{(.*?)\}",
        expr
    )


    if match:

        num, den = match.groups()


        numerator = OxmlElement("m:num")

        numerator.append(
            create_run(
                convert_symbols(num)
            )
        )


        denominator = OxmlElement("m:den")

        denominator.append(
            create_run(
                convert_symbols(den)
            )
        )


        f.append(numerator)
        f.append(denominator)



    return f



# -----------------------------
# ROOT
# -----------------------------

def create_root(expr):

    root = OxmlElement("m:rad")


    e = OxmlElement("m:e")


    value = re.search(
        r"\\sqrt\{(.*?)\}",
        expr
    )


    if value:

        e.append(
            create_run(
                convert_symbols(value.group(1))
            )
        )


    root.append(e)

    return root



# -----------------------------
# RUN CREATOR
# -----------------------------

def create_run(text):

    r = OxmlElement("m:r")

    t = OxmlElement("m:t")

    t.text = text

    r.append(t)

    return r



# -----------------------------
# SYMBOL CONVERTER
# -----------------------------

def convert_symbols(text):


    symbols = {

        # Greek
        r"\alpha":"α",
        r"\beta":"β",
        r"\gamma":"γ",
        r"\Delta":"Δ",
        r"\theta":"θ",
        r"\lambda":"λ",
        r"\mu":"μ",
        r"\pi":"π",


        # Math
        r"\infty":"∞",
        r"\dots":"…",
        r"\cdots":"⋯",

        r"\leq":"≤",
        r"\geq":"≥",
        r"\neq":"≠",

        r"\times":"×",
        r"\pm":"±",

        r"\rightarrow":"→",

    }


    for k,v in symbols.items():

        text=text.replace(k,v)


    # superscripts

    text=re.sub(
        r"\^\{(.*?)\}",
        r"^\1",
        text
    )


    # subscripts

    text=re.sub(
        r"_\{(.*?)\}",
        r"_\1",
        text
    )


    return text