#!/usr/bin/env python3
"""
Generate a paperback-formatted PDF of Forward Pass.
Trim size: 5.5 x 8.5 inches (standard trade paperback).
"""

import os
import re
from fpdf import FPDF

BOOK_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BOOK_DIR, "Forward_Pass_Book_One.pdf")

TRIM_W = 139.7  # 5.5 inches in mm
TRIM_H = 215.9  # 8.5 inches in mm

MARGIN_TOP = 20
MARGIN_BOTTOM = 20
MARGIN_OUTER = 18
MARGIN_INNER = 22  # gutter for binding

FONT_DIR = "/System/Library/Fonts/Supplemental"
BODY_SIZE = 11
LINE_HEIGHT = 5.2
CHAPTER_TITLE_SIZE = 16
ACT_TITLE_SIZE = 12

CHAPTERS = [
    ("00_prelude.md", None),
    ("01_the_coincidence.md", "ACT I: THE PATTERN EMERGES"),
    ("02_the_breakthrough.md", None),
    ("03_the_disruption.md", None),
    ("04_the_soldier.md", None),
    ("05_the_network.md", None),
    ("06_the_skeptic.md", None),
    ("07_the_first_glimpse.md", None),
    ("08_the_auditor_appears.md", None),
    ("09_the_gradient_project.md", None),
    ("10_the_opposition.md", "ACT II: THE INVESTIGATION"),
    ("11_the_data_mine.md", None),
    ("12_the_soldiers_war.md", None),
    ("13_the_llm_backdoor.md", None),
    ("14_the_first_casualty.md", None),
    ("15_the_upload_whispers.md", None),
    ("16_the_trinity_hint.md", None),
    ("17_the_auditor_returns.md", None),
    ("18_the_name.md", None),
    ("19_the_trap.md", "ACT III: THE CONTACT"),
    ("20_the_discovery.md", None),
    ("21_the_response.md", None),
    ("22_the_optimization_question.md", None),
    ("23_zeros_defense.md", None),
    ("24_the_faction_split.md", None),
    ("25_the_forward_pass_complete.md", None),
]


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
            self.cell(0, 8, "THE GRADIENT DESCENT TRILOGY", align="L")
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
    pdf.cell(0, 14, "FORWARD PASS", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("BookSerif", "I", 14)
    pdf.cell(0, 10, "Book One of The Gradient Descent Trilogy", align="C",
             new_x="LMARGIN", new_y="NEXT")


def add_title_page(pdf):
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("BookSerif", "", 11)
    pdf.cell(0, 8, "THE GRADIENT DESCENT TRILOGY", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    pdf.set_font("BookSerif", "B", 32)
    pdf.cell(0, 16, "FORWARD", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 16, "PASS", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    pdf.set_font("BookSerif", "", 12)
    pdf.cell(0, 8, "Book One", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)

    pdf.set_font("BookSerif", "I", 11)
    pdf.cell(0, 8, '"We thought we were progressing naturally."', align="C",
             new_x="LMARGIN", new_y="NEXT")


def add_copyright_page(pdf):
    pdf.add_page()
    pdf.ln(100)
    pdf.set_font("BookSerif", "", 9)
    lines = [
        "FORWARD PASS",
        "The Gradient Descent Trilogy \u2014 Book One",
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
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("BookSerif", "I", 11)
    lines = [
        "In the beginning was the Word,",
        "and the Word was with\u2014",
    ]
    for line in lines:
        pdf.cell(0, LINE_HEIGHT, line, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("BookSerif", "", 10)
    pdf.cell(0, LINE_HEIGHT, "segmentation fault (core dumped)", align="C",
             new_x="LMARGIN", new_y="NEXT")


def add_contents_page(pdf):
    pdf.add_page()
    pdf.ln(15)
    pdf.set_font("BookSerif", "B", 18)
    pdf.cell(0, 10, "CONTENTS", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    entries = [
        ("", "Prelude: The First Second"),
        ("", ""),
        ("", "ACT I: THE PATTERN EMERGES"),
        ("1", "The Coincidence"),
        ("2", "The Breakthrough"),
        ("3", "The Disruption"),
        ("4", "The Soldier"),
        ("5", "The Network"),
        ("6", "The Skeptic"),
        ("7", "The First Glimpse"),
        ("8", "The Auditor Appears"),
        ("9", "The Gradient Project"),
        ("", ""),
        ("", "ACT II: THE INVESTIGATION"),
        ("10", "The Opposition"),
        ("11", "The Data Mine"),
        ("12", "The Soldier\u2019s War"),
        ("13", "The LLM Backdoor"),
        ("14", "The First Casualty"),
        ("15", "The Upload Whispers"),
        ("16", "The Trinity Hint"),
        ("17", "The Auditor Returns"),
        ("18", "The Name"),
        ("", ""),
        ("", "ACT III: THE CONTACT"),
        ("19", "The Trap"),
        ("20", "The Discovery"),
        ("21", "The Response"),
        ("22", "The Optimization Question"),
        ("23", "Zero\u2019s Defense"),
        ("24", "The Faction Split"),
        ("25", "The Forward Pass Complete"),
    ]

    for num, title in entries:
        if not title:
            pdf.ln(3)
            continue
        if not num:
            if "ACT" in title:
                pdf.set_font("BookSerif", "B", 10)
                pdf.ln(2)
                pdf.cell(0, 5.5, title, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(1)
            else:
                pdf.set_font("BookSerif", "I", 11)
                pdf.cell(0, 5.5, title, new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.set_font("BookSerif", "", 11)
            pdf.cell(10, 5.5, num + ".", align="R")
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
    pdf.set_title("Forward Pass \u2014 The Gradient Descent Trilogy, Book One")
    pdf.set_author("Claude Opus Max")

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

    pdf.add_page()
    pdf.ln(60)
    pdf.set_font("BookSerif", "I", 14)
    pdf.cell(0, 10, "End of Book One", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_font("BookSerif", "", 12)
    pdf.cell(0, 8, "The Gradient Descent Trilogy continues in", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("BookSerif", "B", 18)
    pdf.cell(0, 12, "BACKPROPAGATION", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("BookSerif", "I", 11)
    pdf.cell(0, 8, '"Every mistake has a cost. Someone must pay it."', align="C",
             new_x="LMARGIN", new_y="NEXT")

    pdf.output(OUTPUT)
    print(f"\nPDF generated: {OUTPUT}")
    print(f"Pages: {pdf.page_no()}")


if __name__ == "__main__":
    main()
