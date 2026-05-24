#!/usr/bin/env python3
"""
Generate a paperback-formatted PDF from chapter markdown files.
Trim size: 5.5 x 8.5 inches (standard trade paperback).

Usage:
    python3 generate_pdf.py

Dependencies:
    pip install fpdf2

Customize:
    - BOOK_TITLE, SERIES_NAME, AUTHOR, EPIGRAPH
    - CHAPTERS list with (filename, act_header_or_None)
"""

import os
import re
from fpdf import FPDF

BOOK_DIR = os.path.dirname(os.path.abspath(__file__))

# ┌──────────────────────────────────────────┐
# │  BOOK METADATA — customize per story     │
# └──────────────────────────────────────────┘
BOOK_TITLE = "YOUR BOOK TITLE"
SERIES_NAME = "YOUR SERIES NAME"
BOOK_NUMBER = "Book One"
AUTHOR = "Author Name"
EPIGRAPH_LINES = [
    "Your epigraph line one,",
    "your epigraph line two.",
]
EPIGRAPH_ATTRIBUTION = ""
OUTPUT = os.path.join(BOOK_DIR, f"{BOOK_TITLE.replace(' ', '_')}.pdf")

# ┌──────────────────────────────────────────┐
# │  CHAPTERS — (filename, act_header|None)  │
# └──────────────────────────────────────────┘
CHAPTERS = [
    # ("00_prologue.md", None),
    # ("01_first_chapter.md", "ACT I: BEGINNING"),
    # ("02_second_chapter.md", None),
]

TRIM_W = 139.7  # 5.5 inches in mm
TRIM_H = 215.9  # 8.5 inches in mm

MARGIN_TOP = 20
MARGIN_BOTTOM = 20
MARGIN_OUTER = 18
MARGIN_INNER = 22

FONT_DIR = "/System/Library/Fonts/Supplemental"
BODY_SIZE = 11
LINE_HEIGHT = 5.2
CHAPTER_TITLE_SIZE = 16
ACT_TITLE_SIZE = 12


class BookPDF(FPDF):
    def __init__(self):
        super().__init__(unit="mm", format=(TRIM_W, TRIM_H))
        self.set_auto_page_break(auto=True, margin=MARGIN_BOTTOM)
        self.is_front_matter = True
        self.current_chapter_title = ""
        self._register_fonts()

    def _register_fonts(self):
        self.add_font("BookSerif", "",
                       os.path.join(FONT_DIR, "Times New Roman.ttf"))
        self.add_font("BookSerif", "B",
                       os.path.join(FONT_DIR, "Times New Roman Bold.ttf"))
        self.add_font("BookSerif", "I",
                       os.path.join(FONT_DIR, "Times New Roman Italic.ttf"))
        self.add_font("BookSerif", "BI",
                       os.path.join(FONT_DIR, "Times New Roman Bold Italic.ttf"))

    def _set_margins_for_page(self):
        if self.page_no() % 2 == 0:
            self.set_left_margin(MARGIN_OUTER)
            self.set_right_margin(MARGIN_INNER)
        else:
            self.set_left_margin(MARGIN_INNER)
            self.set_right_margin(MARGIN_OUTER)

    def header(self):
        self._set_margins_for_page()
        if self.is_front_matter or self.page_no() <= 4:
            return
        self.set_font("BookSerif", "I", 8)
        self.set_text_color(120, 120, 120)
        if self.page_no() % 2 == 0:
            self.cell(0, 8, SERIES_NAME, align="L")
        else:
            self.cell(0, 8, self.current_chapter_title.upper(), align="R")
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def footer(self):
        if self.is_front_matter:
            return
        self.set_y(-MARGIN_BOTTOM + 5)
        self.set_font("BookSerif", "", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, str(self.page_no() - 4), align="C")
        self.set_text_color(0, 0, 0)


def strip_markdown(text):
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"\1", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"~~(.+?)~~", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"^\|.*\|$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*]\s+", "  \u2022 ", text, flags=re.MULTILINE)
    return text


def parse_chapter(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    title_match = re.match(r"^#\s+(.+)", raw)
    title = title_match.group(1).strip() if title_match else os.path.basename(filepath)

    body = strip_markdown(raw)
    lines = body.split("\n")
    if lines and lines[0].strip() == title:
        lines = lines[1:]

    return title, "\n".join(lines)


def add_half_title(pdf):
    pdf.add_page()
    pdf.ln(60)
    pdf.set_font("BookSerif", "B", 28)
    pdf.cell(0, 14, BOOK_TITLE.upper(), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("BookSerif", "I", 14)
    pdf.cell(0, 10, f"{BOOK_NUMBER} of {SERIES_NAME}", align="C",
             new_x="LMARGIN", new_y="NEXT")


def add_title_page(pdf):
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("BookSerif", "", 11)
    pdf.cell(0, 8, SERIES_NAME, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    pdf.set_font("BookSerif", "B", 32)
    for word in BOOK_TITLE.upper().split():
        pdf.cell(0, 16, word, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    pdf.set_font("BookSerif", "", 12)
    pdf.cell(0, 8, BOOK_NUMBER, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)

    pdf.set_font("BookSerif", "I", 11)
    if EPIGRAPH_LINES:
        pdf.cell(0, 8, EPIGRAPH_LINES[0], align="C",
                 new_x="LMARGIN", new_y="NEXT")


def add_copyright_page(pdf):
    pdf.add_page()
    pdf.ln(100)
    pdf.set_font("BookSerif", "", 9)
    lines = [
        BOOK_TITLE.upper(),
        f"{SERIES_NAME} \u2014 {BOOK_NUMBER}",
        "",
        "This is a work of fiction. Names, characters, places, and incidents",
        "either are the product of the author\u2019s imagination or are used",
        "fictitiously. Any resemblance to actual persons, living or dead,",
        "events, or locales is entirely coincidental.",
        "",
        "All rights reserved.",
        "",
        "First Edition, 2026",
    ]
    for line in lines:
        pdf.cell(0, 5, line, align="C", new_x="LMARGIN", new_y="NEXT")


def add_epigraph(pdf):
    if not EPIGRAPH_LINES:
        return
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("BookSerif", "I", 11)
    for line in EPIGRAPH_LINES:
        pdf.cell(0, LINE_HEIGHT, line, align="C", new_x="LMARGIN", new_y="NEXT")
    if EPIGRAPH_ATTRIBUTION:
        pdf.ln(4)
        pdf.set_font("BookSerif", "", 10)
        pdf.cell(0, LINE_HEIGHT, EPIGRAPH_ATTRIBUTION, align="C",
                 new_x="LMARGIN", new_y="NEXT")


def add_contents_page(pdf):
    pdf.add_page()
    pdf.ln(15)
    pdf.set_font("BookSerif", "B", 18)
    pdf.cell(0, 10, "CONTENTS", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    for filename, act_header in CHAPTERS:
        title_match = None
        filepath = os.path.join(BOOK_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                first_line = f.readline()
                title_match = re.match(r"^#\s+(.+)", first_line)

        title = title_match.group(1).strip() if title_match else filename.replace(".md", "").replace("_", " ").title()

        if act_header:
            pdf.set_font("BookSerif", "B", 10)
            pdf.ln(2)
            pdf.cell(0, 5.5, act_header, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)

        pdf.set_font("BookSerif", "", 11)
        pdf.cell(0, 5.5, "  " + title, new_x="LMARGIN", new_y="NEXT")


def render_body(pdf, text):
    paragraphs = re.split(r"\n\n+", text.strip())

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if para == "---":
            pdf.ln(4)
            x = pdf.get_x()
            w = pdf.w - pdf.l_margin - pdf.r_margin
            y = pdf.get_y()
            pdf.set_draw_color(180, 180, 180)
            center = x + w / 2
            pdf.line(center - 15, y, center + 15, y)
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(4)
            continue

        if para.startswith("\u2022") or para.startswith("  \u2022"):
            pdf.set_font("BookSerif", "", BODY_SIZE)
            pdf.multi_cell(0, LINE_HEIGHT, para)
            pdf.ln(1)
            continue

        is_italic_block = (
            para.startswith("*") and para.endswith("*") and not para.startswith("**")
        ) or (
            para.startswith("\u201c") or para.startswith(">")
        )

        if para.startswith(">"):
            para = para.lstrip("> ")

        if is_italic_block:
            para = para.strip("*")
            pdf.set_font("BookSerif", "I", BODY_SIZE)
        else:
            pdf.set_font("BookSerif", "", BODY_SIZE)

        pdf.multi_cell(0, LINE_HEIGHT, para)
        pdf.ln(1.5)


def main():
    pdf = BookPDF()
    pdf.set_title(f"{BOOK_TITLE} \u2014 {SERIES_NAME}, {BOOK_NUMBER}")
    pdf.set_author(AUTHOR)

    add_half_title(pdf)
    add_title_page(pdf)
    add_copyright_page(pdf)
    add_epigraph(pdf)
    add_contents_page(pdf)

    pdf.is_front_matter = False

    for filename, act_header in CHAPTERS:
        filepath = os.path.join(BOOK_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  SKIP (not found): {filename}")
            continue

        title, body = parse_chapter(filepath)
        pdf.current_chapter_title = title

        pdf.add_page()
        pdf.ln(25)

        if act_header:
            pdf.set_font("BookSerif", "B", ACT_TITLE_SIZE)
            pdf.cell(0, 8, act_header, align="C", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(8)

        pdf.set_font("BookSerif", "B", CHAPTER_TITLE_SIZE)
        pdf.cell(0, 10, title, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)

        render_body(pdf, body)

    pdf.output(OUTPUT)
    print(f"\nPDF generated: {OUTPUT}")
    print(f"Pages: {pdf.page_no()}")


if __name__ == "__main__":
    main()
