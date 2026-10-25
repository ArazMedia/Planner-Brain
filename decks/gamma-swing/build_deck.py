#!/usr/bin/env python3
"""Build the Gamma Swing Trading deck for Dominic.

    python3 decks/gamma-swing/build_deck.py

Writes gamma_swing.pptx next to this file.
Charts are Black-Scholes illustrations with the inputs printed on the slide.
"""

from __future__ import annotations

import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parent
CHART_DIR = Path("/tmp/gamma-charts")
CHART_DIR.mkdir(parents=True, exist_ok=True)

W = 13.333333
H = 7.5
ML = 0.42
CONTENT_W = 12.49
TOP = 1.08
BOTTOM = 7.02

FONT = "Liberation Sans"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

# Dark, quiet, high contrast. Regime colors are used as labels, not as body text.
BG = "0E1218"
CARD = "171D28"
NEST = "222A38"
LINE = "313A4B"
TEXT = "F4F7FB"
BODY = "D5DDE8"
DIM = "B4BECC"
FOOT = "A8B3C2"
TEAL = "3DDCB0"
TEAL_DIM = "14352F"
CORAL = "FF7676"
CORAL_DIM = "3A2226"
AMBER = "E6B54A"
AMBER_DIM = "332C16"
BLUE = "8EBEFF"
BLUE_DIM = "1A2838"
PURPLE = "C9B2FF"
PURPLE_DIM = "2A2340"
CYAN = "7AD7E4"
WHITE = "F4F7FB"

font_manager.fontManager.addfont(FONT_REG)
font_manager.fontManager.addfont(FONT_BOLD)
plt.rcParams["font.family"] = "Liberation Sans"
plt.rcParams["axes.unicode_minus"] = False


def rgb(value: str) -> RGBColor:
    value = value.lstrip("#")
    return RGBColor(int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def check_ascii(text: str) -> None:
    bad = [(i, ch, hex(ord(ch))) for i, ch in enumerate(text) if ord(ch) > 126]
    if bad:
        raise SystemExit(f"Non-ASCII {bad} in {text!r}")
    if "|" in text:
        raise SystemExit(f"Absolute-value bar in {text!r}")


# --- Black-Scholes (European, no dividend). Teaching charts only. ---

def _ncdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _npdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def _d1(s: float, k: float, t: float, r: float, sig: float) -> float:
    return (math.log(s / k) + (r + 0.5 * sig * sig) * t) / (sig * math.sqrt(t))


def _d2(s: float, k: float, t: float, r: float, sig: float) -> float:
    return _d1(s, k, t, r, sig) - sig * math.sqrt(t)


def call_price(s: float, k: float, t: float, r: float, sig: float) -> float:
    if t <= 1e-8:
        return max(s - k, 0.0)
    return s * _ncdf(_d1(s, k, t, r, sig)) - math.exp(-r * t) * k * _ncdf(_d2(s, k, t, r, sig))


def call_delta(s: float, k: float, t: float, r: float, sig: float) -> float:
    if t <= 1e-8:
        return 1.0 if s > k else 0.0
    return _ncdf(_d1(s, k, t, r, sig))


def call_gamma(s: float, k: float, t: float, r: float, sig: float) -> float:
    return _npdf(_d1(s, k, t, r, sig)) / (s * sig * math.sqrt(t))


def bs_facts() -> dict:
    """Numbers printed on slides. All of them come from this function."""
    r = 0.04
    g30 = call_gamma(100, 100, 30 / 365, r, 0.20)
    g7 = call_gamma(100, 100, 7 / 365, r, 0.20)
    g1 = call_gamma(100, 100, 1 / 365, r, 0.20)
    shares = []
    for days in (1, 7, 30):
        t = days / 365
        shares.append((call_delta(101, 100, t, r, 0.20) - call_delta(100, 100, t, r, 0.20)) * 100)
    # 14-day ATM crush, IV 50% to 25%.
    t14 = 14 / 365
    crush_start = call_price(100, 100, t14, r, 0.50)
    crush_flat = call_price(100, 100, t14, r, 0.25)
    crush_up = call_price(102, 100, t14, r, 0.25)
    # 21-day delta bands and payoff debits. IV 25% unless noted.
    t21 = 21 / 365
    bands = []
    for strike in (106, 100, 95):
        delta = call_delta(100, strike, t21, r, 0.25)
        price = call_price(100, strike, t21, r, 0.25)
        bands.append({"k": strike, "delta": delta, "price": price, "shares": delta * 100})
    call_25 = call_price(100, 100, t21, r, 0.25)
    short_25 = call_price(100, 105, t21, r, 0.25)
    spread_25 = call_25 - short_25
    rich = {}
    for sig in (0.18, 0.40):
        atm = call_price(100, 100, t21, r, sig)
        spr = atm - call_price(100, 105, t21, r, sig)
        rich[sig] = {"call": atm, "spread": spr, "max_gain": 5.0 - spr}
    decay = []
    for days in range(45, 0, -1):
        t = days / 365
        single = call_price(100, 100, t, r, 0.25)
        spread = single - call_price(100, 105, t, r, 0.25)
        decay.append((days, single, spread))
    return {
        "g_ratio_1": g1 / g30,
        "g_ratio_7": g7 / g30,
        "shares": shares,
        "crush_start": crush_start,
        "crush_flat": crush_flat,
        "crush_up": crush_up,
        "bands": bands,
        "call_25": call_25,
        "short_25": short_25,
        "spread_25": spread_25,
        "max_gain_25": 5.0 - spread_25,
        "rich": rich,
        "decay": decay,
    }


FACTS = bs_facts()


def money(value: float) -> str:
    return f"{value:.2f}"


def _style_ax(ax, ylabel: str, xlabel: str) -> None:
    ax.set_facecolor("#171D28")
    ax.tick_params(colors="#C5CEDA", labelsize=11, width=0)
    ax.xaxis.label.set_color("#D5DDE8")
    ax.yaxis.label.set_color("#D5DDE8")
    ax.xaxis.label.set_size(12)
    ax.yaxis.label.set_size(12)
    for spine in ax.spines.values():
        spine.set_color("#313A4B")
    ax.grid(True, color="#313A4B", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)


def _legend(ax, loc="upper right") -> None:
    leg = ax.legend(loc=loc, frameon=True, fontsize=11)
    frame = leg.get_frame()
    frame.set_facecolor("#171D28")
    frame.set_edgecolor("#313A4B")
    for text in leg.get_texts():
        text.set_color("#F4F7FB")


def chart_gamma() -> Path:
    r = 0.04
    strikes = [80 + i * 0.1 for i in range(401)]
    g30 = call_gamma(100, 100, 30 / 365, r, 0.20)
    fig, ax = plt.subplots(figsize=(8.15, 4.70), dpi=160)
    fig.patch.set_facecolor("#0E1218")
    for days, color, label in (
        (30, "#8EBEFF", "30 days"),
        (7, "#E6B54A", "7 days"),
        (1, "#FF7676", "1 day"),
    ):
        ys = [call_gamma(100, k, days / 365, r, 0.20) / g30 for k in strikes]
        ax.plot(strikes, ys, color=color, linewidth=2.4, label=label)
    ax.axvline(100, color="#A8B3C2", linewidth=1.0, linestyle=(0, (3, 3)))
    _style_ax(ax, "Gamma, scaled so the 30-day peak is 1", "Strike. Spot is 100")
    _legend(ax, "upper left")
    ax.set_xlim(80, 120)
    ax.set_ylim(0, FACTS["g_ratio_1"] * 1.14)
    fig.subplots_adjust(left=0.11, right=0.97, top=0.94, bottom=0.16)
    path = CHART_DIR / "gamma.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def chart_hedge_shares() -> Path:
    labels = ["1 day", "7 days", "30 days"]
    values = FACTS["shares"]
    fig, ax = plt.subplots(figsize=(6.4, 4.15), dpi=160)
    fig.patch.set_facecolor("#0E1218")
    ax.bar(labels, values, color=["#FF7676", "#E6B54A", "#8EBEFF"], width=0.62)
    for i, value in enumerate(values):
        ax.text(i, value + 0.6, f"{value:.1f}", ha="center", va="bottom", color="#F4F7FB", fontsize=13)
    _style_ax(ax, "Shares bought, per short call", "Time left. Same 1-point rally")
    ax.set_ylim(0, max(values) * 1.22)
    fig.subplots_adjust(left=0.16, right=0.96, top=0.92, bottom=0.16)
    path = CHART_DIR / "hedge.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def chart_delta() -> Path:
    r = 0.04
    strikes = [85 + i * 0.1 for i in range(301)]
    deltas = [call_delta(100, k, 21 / 365, r, 0.25) for k in strikes]
    fig, ax = plt.subplots(figsize=(7.5, 4.55), dpi=160)
    fig.patch.set_facecolor("#0E1218")
    ax.axhline(0.40, color="#E6B54A", linewidth=1.1, linestyle=(0, (4, 3)), zorder=2)
    ax.axhline(0.60, color="#E6B54A", linewidth=1.1, linestyle=(0, (4, 3)), zorder=2)
    ax.text(85.4, 0.625, "mid band  0.40 to 0.60", color="#E6B54A", fontsize=11)
    ax.plot(strikes, deltas, color="#8EBEFF", linewidth=2.6, zorder=3)
    offsets = {95: (8, 10), 100: (10, -26), 106: (8, 10)}
    for band in FACTS["bands"]:
        ax.scatter([band["k"]], [band["delta"]], s=42, color="#F4F7FB", zorder=4)
        ax.annotate(
            f"{band['k']:.0f} strike   {band['delta']:.2f}",
            (band["k"], band["delta"]),
            textcoords="offset points",
            xytext=offsets[band["k"]],
            color="#F4F7FB",
            fontsize=11,
        )
    _style_ax(ax, "Call delta", "Strike. Spot is 100")
    ax.set_xlim(85, 115)
    ax.set_ylim(0, 1.02)
    fig.subplots_adjust(left=0.10, right=0.97, top=0.93, bottom=0.16)
    path = CHART_DIR / "delta.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def chart_decay() -> Path:
    days = [row[0] for row in FACTS["decay"]]
    single = [row[1] for row in FACTS["decay"]]
    spread = [row[2] for row in FACTS["decay"]]
    fig, ax = plt.subplots(figsize=(7.6, 4.45), dpi=160)
    fig.patch.set_facecolor("#0E1218")
    ax.plot(days, single, color="#8EBEFF", linewidth=2.5, label="Single ATM call")
    ax.plot(days, spread, color="#3DDCB0", linewidth=2.5, label="100 / 105 call spread")
    _style_ax(ax, "Option price, spot held at 100", "Days left")
    ax.invert_xaxis()
    _legend(ax, "upper right")
    fig.subplots_adjust(left=0.10, right=0.97, top=0.92, bottom=0.16)
    path = CHART_DIR / "decay.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def chart_crush() -> Path:
    labels = ["Start\nspot 100\nIV 50%", "Spot flat\nspot 100\nIV 25%", "Spot up 2\nspot 102\nIV 25%"]
    values = [FACTS["crush_start"], FACTS["crush_flat"], FACTS["crush_up"]]
    colors = ["#8EBEFF", "#FF7676", "#E6B54A"]
    fig, ax = plt.subplots(figsize=(6.7, 4.20), dpi=160)
    fig.patch.set_facecolor("#0E1218")
    ax.bar(labels, values, color=colors, width=0.66)
    for i, value in enumerate(values):
        ax.text(i, value + 0.06, money(value), ha="center", va="bottom", color="#F4F7FB", fontsize=14)
    _style_ax(ax, "Call price", "14-day ATM call. Spot starts at 100")
    ax.set_ylim(0, max(values) * 1.22)
    fig.subplots_adjust(left=0.14, right=0.97, top=0.92, bottom=0.24)
    path = CHART_DIR / "crush.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def chart_payoff() -> Path:
    debit_call = FACTS["call_25"]
    debit_spread = FACTS["spread_25"]
    spots = [90 + i * 0.25 for i in range(101)]
    single = [max(s - 100, 0) - debit_call for s in spots]
    spread = [min(max(s - 100, 0), 5) - debit_spread for s in spots]
    fig, ax = plt.subplots(figsize=(7.3, 4.35), dpi=160)
    fig.patch.set_facecolor("#0E1218")
    ax.axhline(0, color="#A8B3C2", linewidth=1.0)
    ax.plot(spots, single, color="#8EBEFF", linewidth=2.5, label="Long 100 call")
    ax.plot(spots, spread, color="#3DDCB0", linewidth=2.5, label="Long 100 / short 105")
    _style_ax(ax, "Profit at expiry, per share", "Spot at expiry")
    _legend(ax, "upper left")
    ax.set_xlim(90, 115)
    ax.set_ylim(-3.6, 14.2)
    fig.subplots_adjust(left=0.12, right=0.97, top=0.92, bottom=0.16)
    path = CHART_DIR / "payoff.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def build_charts() -> dict[str, Path]:
    return {
        "gamma": chart_gamma(),
        "hedge": chart_hedge_shares(),
        "delta": chart_delta(),
        "decay": chart_decay(),
        "crush": chart_crush(),
        "payoff": chart_payoff(),
    }


class Deck:
    def __init__(self) -> None:
        self.prs = Presentation()
        self.prs.slide_width = Emu(12192000)
        self.prs.slide_height = Emu(6858000)
        self.prs.core_properties.title = "Gamma Swing Trading"
        self.prs.core_properties.subject = "Dealer gamma, walls, and candle-close swings"
        self.prs.core_properties.author = "For Dominic"
        self.blank = self._blank()
        self.n = 0
        self.titles: list[str] = []
        self.records: list[dict] = []
        self.warnings: list[str] = []
        self._fonts = {
            False: ImageFont.truetype(FONT_REG, 10),
            True: ImageFont.truetype(FONT_BOLD, 10),
        }

    def _blank(self):
        for layout in self.prs.slide_layouts:
            if layout.name.lower() == "blank":
                return layout
        return self.prs.slide_layouts[-1]

    def _font(self, size: float, bold: bool) -> ImageFont.FreeTypeFont:
        key = (round(size, 2), bold)
        cached = getattr(self, "_font_cache", None)
        if cached is None:
            self._font_cache = {}
            cached = self._font_cache
        if key not in cached:
            path = FONT_BOLD if bold else FONT_REG
            cached[key] = ImageFont.truetype(path, size)
        return cached[key]

    def _audit(self, text: str, x, y, w, h, size, bold, ml, mr, mt, mb, spacing) -> None:
        check_ascii(text)
        usable_w = (w - ml - mr) * 72
        font = self._font(size, bold)
        lines = 0
        for para in text.split("\n"):
            if para == "":
                lines += 1
                continue
            words = para.split(" ")
            cur = ""
            lines += 1
            for word in words:
                trial = word if cur == "" else cur + " " + word
                width = font.getlength(trial)
                if width <= usable_w:
                    cur = trial
                    continue
                if cur == "":
                    self.warnings.append(
                        f"slide {self.n:02d} word wider than box ({word!r} {width:.0f}>{usable_w:.0f}) {text[:80]!r}"
                    )
                    cur = word
                    continue
                lines += 1
                if font.getlength(word) > usable_w:
                    self.warnings.append(
                        f"slide {self.n:02d} word wider than box ({word!r}) {text[:80]!r}"
                    )
                cur = word
        line_h = size * spacing
        need = lines * line_h / 72 + mt + mb
        if need > h + 0.02:
            self.warnings.append(
                f"slide {self.n:02d} text height {need:.2f} > box {h:.2f} size {size} lines {lines}: {text[:90]!r}"
            )
        if y + h > 7.12 and y < 7.05:
            self.warnings.append(f"slide {self.n:02d} text runs into footer y {y:.2f} h {h:.2f}: {text[:60]!r}")

    def _apply_run(self, run, text: str, size: float, bold: bool, color: str) -> None:
        check_ascii(text)
        run.text = text
        run.font.name = FONT
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = False
        run.font.color.rgb = rgb(color)
        r_pr = run._r.get_or_add_rPr()
        r_pr.set("lang", "en-US")
        for tag in ("a:latin", "a:ea", "a:cs"):
            el = r_pr.find(qn(tag))
            if el is None:
                el = r_pr.makeelement(qn(tag), {})
                r_pr.append(el)
            el.set("typeface", FONT)

    def _style_paragraph(self, paragraph, align: str, size: float, spacing: float) -> None:
        paragraph.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[align]
        paragraph.space_before = Pt(0)
        paragraph.space_after = Pt(0)
        paragraph.line_spacing = Pt(size * spacing)

    def text(
        self,
        slide,
        x,
        y,
        w,
        h,
        content,
        size=16,
        bold=False,
        color=BODY,
        align="left",
        anchor="top",
        spacing=1.18,
        ml=0.04,
        mr=0.04,
        mt=0.02,
        mb=0.02,
    ):
        if content is None or content == "":
            return None
        self._audit(content, x, y, w, h, size, bold, ml, mr, mt, mb, spacing)
        self.records.append({"slide": self.n, "text": content})
        box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        frame = box.text_frame
        frame.word_wrap = True
        frame.auto_size = None
        frame.margin_left = Inches(ml)
        frame.margin_right = Inches(mr)
        frame.margin_top = Inches(mt)
        frame.margin_bottom = Inches(mb)
        frame.anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[anchor]
        lines = content.split("\n")
        for i, line in enumerate(lines):
            paragraph = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
            self._style_paragraph(paragraph, align, size, spacing)
            run = paragraph.add_run()
            self._apply_run(run, line, size, bold, color)
        if os.environ.get("DEBUG_BOXES") == "1":
            self.rect(slide, x, y, w, h, None, line="FF00AA", line_w=0.75)
        return box

    def rich(self, slide, x, y, w, h, paragraphs, align="left", anchor="top", ml=0.06, mr=0.06, mt=0.04, mb=0.04):
        """paragraphs: list of list of (text, size, bold, color)."""
        plain = "\n".join("".join(run[0] for run in para) for para in paragraphs)
        max_size = max(run[1] for para in paragraphs for run in para)
        any_bold = any(run[2] for para in paragraphs for run in para)
        self._audit(plain, x, y, w, h, max_size, any_bold, ml, mr, mt, mb, 1.18)
        self.records.append({"slide": self.n, "text": plain})
        box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        frame = box.text_frame
        frame.word_wrap = True
        frame.auto_size = None
        frame.margin_left = Inches(ml)
        frame.margin_right = Inches(mr)
        frame.margin_top = Inches(mt)
        frame.margin_bottom = Inches(mb)
        frame.anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[anchor]
        for i, runs in enumerate(paragraphs):
            paragraph = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
            size = max(run[1] for run in runs)
            self._style_paragraph(paragraph, align, size, 1.18)
            for text, rsize, bold, color in runs:
                run = paragraph.add_run()
                self._apply_run(run, text, rsize, bold, color)
        return box

    def rect(self, slide, x, y, w, h, fill, line=None, line_w=1.0):
        if x < -0.02 or y < -0.02 or x + w > W + 0.02 or y + h > H + 0.02:
            raise SystemExit(f"Shape off slide {self.n}: {x:.2f},{y:.2f} {w:.2f}x{h:.2f}")
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        shape.shadow.inherit = False
        if fill is None:
            shape.fill.background()
        else:
            shape.fill.solid()
            shape.fill.fore_color.rgb = rgb(fill)
        if line is None:
            shape.line.fill.background()
        else:
            shape.line.color.rgb = rgb(line)
            shape.line.width = Pt(line_w)
        return shape

    def round(self, slide, x, y, w, h, fill, line=None, line_w=1.0, adj=0.15):
        if x < -0.02 or y < -0.02 or x + w > W + 0.02 or y + h > H + 0.02:
            raise SystemExit(f"Shape off slide {self.n}: {x:.2f},{y:.2f} {w:.2f}x{h:.2f}")
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        shape.shadow.inherit = False
        try:
            shape.adjustments[0] = adj
        except Exception:
            pass
        if fill is None:
            shape.fill.background()
        else:
            shape.fill.solid()
            shape.fill.fore_color.rgb = rgb(fill)
        if line is None:
            shape.line.fill.background()
        else:
            shape.line.color.rgb = rgb(line)
            shape.line.width = Pt(line_w)
        return shape

    def oval(self, slide, x, y, w, h, fill, line=None, line_w=1.0):
        shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(w), Inches(h))
        shape.shadow.inherit = False
        shape.fill.solid()
        shape.fill.fore_color.rgb = rgb(fill)
        if line is None:
            shape.line.fill.background()
        else:
            shape.line.color.rgb = rgb(line)
            shape.line.width = Pt(line_w)
        return shape

    def arrow(self, slide, x, y, w, h, fill, direction="right"):
        kind = {
            "right": MSO_SHAPE.RIGHT_ARROW,
            "left": MSO_SHAPE.LEFT_ARROW,
            "up": MSO_SHAPE.UP_ARROW,
            "down": MSO_SHAPE.DOWN_ARROW,
        }[direction]
        shape = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
        shape.shadow.inherit = False
        shape.fill.solid()
        shape.fill.fore_color.rgb = rgb(fill)
        shape.line.fill.background()
        return shape

    def panel(self, slide, x, y, w, h, accent=None, fill=CARD):
        self.rect(slide, x, y, w, h, fill, line=LINE, line_w=1.0)
        if accent:
            self.rect(slide, x, y, w, 0.055, accent)

    def chip(self, slide, x, y, w, h, label, fill, fg, size=12):
        self.round(slide, x, y, w, h, fill, adj=0.5)
        self.text(slide, x, y, w, h, label, size=size, bold=True, color=fg, align="center", anchor="middle", ml=0.06, mr=0.06, mt=0.0, mb=0.0)

    def hline(self, slide, x, y, w, color, thickness=0.018):
        self.rect(slide, x, y, w, thickness, color)

    def vline(self, slide, x, y, h, color, thickness=0.018):
        self.rect(slide, x, y, thickness, h, color)

    def footer(self, slide, cover=False):
        label = "For Dominic" if cover else "Gamma swing  -  Dominic"
        self.text(slide, 0.42, 7.16, 8.2, 0.26, label, size=12, color=FOOT, anchor="middle", ml=0.0, mr=0.0, mt=0.0, mb=0.0)
        self.text(
            slide,
            10.4,
            7.16,
            2.5,
            0.26,
            f"{self.n:02d}",
            size=12,
            color=FOOT,
            align="right",
            anchor="middle",
            ml=0.0,
            mr=0.0,
            mt=0.0,
            mb=0.0,
        )

    def chrome(self, kicker: str, title: str):
        self.n += 1
        self.titles.append(title)
        slide = self.prs.slides.add_slide(self.blank)
        self.rect(slide, 0, 0, W, H, BG)
        self.rect(slide, 0, 0, W, 0.055, TEAL)
        self.text(slide, ML, 0.14, 12.4, 0.24, kicker.upper(), size=12, bold=True, color=AMBER, ml=0.0, mr=0.0, mt=0.0, mb=0.0)
        self.text(slide, ML, 0.36, 12.5, 0.48, title, size=28, bold=True, color=TEXT, ml=0.0, mr=0.0, mt=0.0, mb=0.0, spacing=1.05)
        self.rect(slide, ML, 0.90, 0.50, 0.028, TEAL)
        self.rect(slide, ML + 0.50, 0.906, CONTENT_W - 0.50, 0.012, LINE)
        self.footer(slide)
        return slide

    def dashed_h(self, slide, x, y, w, color, thickness=0.016, dash=0.14, gap=0.09):
        cursor = x
        end = x + w
        while cursor < end - 0.01:
            seg = min(dash, end - cursor)
            self.rect(slide, cursor, y, seg, thickness, color)
            cursor += dash + gap

    def candle(self, slide, cx, y_high, y_low, y_open, y_close, color, body=0.20):
        top = min(y_high, y_low)
        bot = max(y_high, y_low)
        self.rect(slide, cx - 0.012, top, 0.024, max(0.02, bot - top), color)
        body_top = min(y_open, y_close)
        body_bot = max(y_open, y_close)
        if body_bot - body_top < 0.10:
            body_bot = body_top + 0.10
        self.rect(slide, cx - body / 2, body_top, body, body_bot - body_top, color)

    def stamp(self, slide, x, y, word="ILLUSTRATIVE"):
        width = 1.92 if word == "ILLUSTRATIVE" else 1.22
        self.chip(slide, x, y, width, 0.32, word, AMBER_DIM, AMBER, size=12)

    def picture(self, slide, path: Path, x, y, w):
        image = Image.open(path)
        h = w * image.height / image.width
        if y + h > 7.08:
            self.warnings.append(f"slide {self.n:02d} picture overflows y {y:.2f} h {h:.2f}")
        slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
        return h

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.prs.save(path)


def cols(n, gap=0.18, x=ML, width=CONTENT_W):
    cw = (width - gap * (n - 1)) / n
    return [(x + i * (cw + gap), cw) for i in range(n)]


# Slides. ASCII only. No absolute-value bars.


def block(d, s, x, y, w, h, title, body, accent=None, ts=18, bs=15):
    d.panel(s, x, y, w, h, accent=accent)
    d.text(s, x + 0.18, y + 0.12, w - 0.36, 0.38, title, size=ts, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    d.text(s, x + 0.18, y + 0.52, w - 0.36, h - 0.66, body, size=bs, color=BODY, ml=0, mr=0, mt=0, mb=0, spacing=1.16)


def ymap(price, pmin, pmax, top, bot):
    return bot - (price - pmin) / (pmax - pmin) * (bot - top)


def slide_cover(d: Deck) -> None:
    d.n += 1
    d.titles.append("Gamma swing trading")
    s = d.prs.slides.add_slide(d.blank)
    d.rect(s, 0, 0, W, H, BG)
    d.rect(s, 0, 0, W, 0.055, TEAL)
    d.text(s, 0.55, 1.05, 7.2, 0.26, "FOR DOMINIC", size=14, bold=True, color=AMBER, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.52, 1.32, 7.4, 0.92, "Gamma", size=58, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0, spacing=1.0)
    d.text(s, 0.52, 2.22, 7.5, 0.66, "swing trading", size=36, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0, spacing=1.0)
    d.rect(s, 0.55, 2.98, 2.05, 0.032, TEAL)
    d.text(
        s, 0.55, 3.16, 7.15, 1.25,
        "Dealer hedging, the walls, and the candle close.\nCash account. Long calls, long puts, debit spreads.\nSwings, earnings, and an occasional 0DTE.",
        size=18, color=BODY, ml=0, mr=0, mt=0, mb=0, spacing=1.18,
    )
    row1 = [
        (0.55, "4h and 15m", 1.48),
        (2.15, "20 / 50 / 200", 1.72),
        (3.99, "Unusual Whales", 1.88),
        (5.99, "TradingView", 1.52),
    ]
    row2 = [(0.55, "Swings", 1.12), (1.79, "Earnings", 1.28), (3.19, "Occasional 0DTE", 2.08)]
    for x, label, w in row1:
        d.chip(s, x, 4.85, w, 0.36, label, NEST, BODY, size=12)
    for x, label, w in row2:
        d.chip(s, x, 5.35, w, 0.36, label, NEST, BODY, size=12)
    d.text(s, 0.55, 6.05, 4.5, 0.30, "October 2026", size=14, color=DIM, ml=0, mr=0, mt=0, mb=0)

    # Regime card
    d.rect(s, 8.22, 0.85, 4.66, 2.42, TEAL_DIM)
    d.text(s, 8.42, 0.98, 4.3, 0.26, "POSITIVE GAMMA", size=13, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 8.42, 1.28, 4.3, 0.30, "Sell rallies. Buy dips.", size=16, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    d.arrow(s, 9.15, 1.72, 0.32, 0.40, TEAL, "down")
    d.arrow(s, 10.85, 1.72, 0.32, 0.40, TEAL, "up")
    d.text(s, 8.85, 2.16, 0.95, 0.26, "sell", size=12, color=TEAL, align="center", ml=0, mr=0, mt=0, mb=0)
    d.text(s, 10.55, 2.16, 0.95, 0.26, "buy", size=12, color=TEAL, align="center", ml=0, mr=0, mt=0, mb=0)
    d.text(s, 8.42, 2.55, 4.2, 0.50, "Price ranges and pins.", size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)

    d.rect(s, 8.22, 3.27, 4.66, 0.50, AMBER_DIM)
    d.text(s, 8.22, 3.27, 4.66, 0.50, "THE FLIP    behavior changes here", size=13, bold=True, color=AMBER, align="center", anchor="middle", ml=0.1, mr=0.1, mt=0, mb=0)

    d.rect(s, 8.22, 3.77, 4.66, 2.55, CORAL_DIM)
    d.text(s, 8.42, 3.90, 4.3, 0.26, "NEGATIVE GAMMA", size=13, bold=True, color=CORAL, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 8.42, 4.20, 4.3, 0.30, "Buy rallies. Sell dips.", size=16, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    d.arrow(s, 9.15, 4.64, 0.32, 0.40, CORAL, "up")
    d.arrow(s, 10.85, 4.64, 0.32, 0.40, CORAL, "down")
    d.text(s, 8.85, 5.08, 0.95, 0.26, "buy", size=12, color=CORAL, align="center", ml=0, mr=0, mt=0, mb=0)
    d.text(s, 10.55, 5.08, 0.95, 0.26, "sell", size=12, color=CORAL, align="center", ml=0, mr=0, mt=0, mb=0)
    d.text(s, 8.42, 5.55, 4.2, 0.55, "Price trends and accelerates.", size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.rect(s, 8.22, 0.85, 4.66, 5.47, None, line=LINE, line_w=1.25)
    d.footer(s, cover=True)


def slide_map(d: Deck) -> None:
    s = d.chrome("Start here", "Read it as a map")
    items = [
        (TEAL, "What you get", "A way to read the regime,\nmark the levels, and pick\nthe contract.\n\nThe trigger is a candle close."),
        (AMBER, "What this is not", "No win rate. No backtest.\nNo fixed dollar risk.\n\nYou choose the dollars\non every trade."),
        (CORAL, "What stays true", "Cash only. No margin.\nNo naked short options.\n\nLong calls, long puts,\nand debit spreads."),
    ]
    for (x, w), (accent, title, body) in zip(cols(3), items):
        block(d, s, x, 1.18, w, 3.15, title, body, accent=accent, ts=18, bs=15)
    steps = [("1", "Regime"), ("2", "Walls"), ("3", "Close"), ("4", "Contract"), ("5", "Your dollars")]
    xs = cols(5, gap=0.28)
    for i, ((x, w), (num, label)) in enumerate(zip(xs, steps)):
        d.panel(s, x, 4.52, w, 1.15, accent=TEAL)
        d.text(s, x + 0.12, 4.64, w - 0.24, 0.28, num, size=12, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
        d.text(s, x + 0.12, 4.96, w - 0.24, 0.50, label, size=16, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
        if i < 4:
            d.arrow(s, x + w + 0.02, 4.92, 0.24, 0.22, TEAL, "right")
    d.panel(s, ML, 5.86, CONTENT_W, 0.98, accent=BLUE)
    d.text(
        s, ML + 0.22, 6.00, CONTENT_W - 0.4, 0.72,
        "Numbers that are not the October 16, 2026 SPY book are marked EXAMPLE.\nCharts are Black-Scholes. The inputs are printed on the slide.",
        size=15, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_tools(d: Deck) -> None:
    s = d.chrome("The account", "The tools this deck assumes")
    rows = [
        ("Chart", "TradingView. The 4h and the 15m."),
        ("Averages", "The 20, the 50, and the 200, on both."),
        ("Levels", "Unusual Whales. Open interest for the swing."),
        ("Check", "A second public gamma source, before a swing."),
        ("Work", "Swings, earnings, and an occasional 0DTE."),
        ("Account", "Cash. You pay the debit. No naked shorts."),
    ]
    for i, (label, line) in enumerate(rows):
        y = 1.18 + i * 0.90
        d.panel(s, ML, y, 8.05, 0.78)
        d.rect(s, ML, y, 1.55, 0.78, NEST)
        d.text(s, ML, y, 1.55, 0.78, label, size=14, bold=True, color=AMBER, align="center", anchor="middle", ml=0.04, mr=0.04, mt=0, mb=0)
        d.text(s, ML + 1.70, y, 6.15, 0.78, line, size=16, color=TEXT, anchor="middle", ml=0.08, mr=0.08, mt=0, mb=0)
    d.panel(s, 8.68, 1.18, 4.23, 5.40, accent=TEAL)
    d.text(s, 8.88, 1.38, 3.85, 0.36, "Allowed", size=16, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 8.88, 1.80, 3.85, 1.70, "Long call\nLong put\nCall debit spread\nPut debit spread", size=16, color=TEXT, ml=0, mr=0, mt=0, mb=0, spacing=1.2)
    d.hline(s, 8.88, 3.70, 3.85, LINE, 0.015)
    d.text(s, 8.88, 3.88, 3.85, 0.36, "Not this account", size=16, bold=True, color=CORAL, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 8.88, 4.32, 3.85, 1.90, "Naked short call\nNaked short put\nMargin\nShort stock as a hedge", size=16, color=BODY, ml=0, mr=0, mt=0, mb=0, spacing=1.2)


def slide_core(d: Deck) -> None:
    s = d.chrome("The point", "Gamma shows where the hedge pushes")
    steps = [
        ("1", "Customers trade\noptions"),
        ("2", "Dealers take\nthe other side"),
        ("3", "Dealers hedge\nwith the stock"),
        ("4", "Gamma says how\nhard that pushes"),
    ]
    xs = cols(4, gap=0.36)
    for i, ((x, w), (num, label)) in enumerate(zip(xs, steps)):
        d.panel(s, x, 1.28, w, 1.95, accent=TEAL)
        d.text(s, x + 0.16, 1.44, w - 0.32, 0.30, num, size=14, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
        d.text(s, x + 0.16, 1.84, w - 0.32, 1.10, label, size=16, color=TEXT, ml=0, mr=0, mt=0, mb=0)
        if i < 3:
            d.arrow(s, x + w + 0.04, 2.05, 0.28, 0.26, TEAL, "right")
    d.panel(s, ML, 3.46, CONTENT_W, 1.05, accent=AMBER)
    d.text(
        s, ML + 0.24, 3.58, CONTENT_W - 0.48, 0.80,
        "Dealers hedge. Gamma shows where that hedging pushes price.",
        size=22, bold=True, color=TEXT, anchor="middle", ml=0, mr=0, mt=0, mb=0,
    )
    notes = [
        (TEAL, "The push is pressure from the hedge. It is not a promise."),
        (AMBER, "You still need the price action, and a candle close."),
        (CORAL, "Direction comes from the break, or from the rejection."),
    ]
    for (x, w), (accent, line) in zip(cols(3), notes):
        d.panel(s, x, 4.72, w, 1.55)
        d.rect(s, x, 4.72, 0.08, 1.55, accent)
        d.text(s, x + 0.24, 4.90, w - 0.42, 1.20, line, size=16, color=BODY, ml=0, mr=0, mt=0, mb=0)


def slide_dealers(d: Deck) -> None:
    s = d.chrome("Dealers", "Three lines on dealers")
    rows = [
        (
            "Dealers hold large options positions from institutional and retail trading",
            "Their book is the other side of that flow. You read the net book, not one order.",
        ),
        (
            "Dealers use the underlying stock to hedge their options positions",
            "They buy or sell shares against the option. That hedge is in the stock you chart.",
        ),
        (
            "Delta tells them how many shares they need to stay neutral",
            "Delta is the share count. When delta changes, the count is wrong, so they trade again.",
        ),
    ]
    for i, (quote, gloss) in enumerate(rows):
        y = 1.18 + i * 1.88
        d.panel(s, ML, y, CONTENT_W, 1.74, accent=AMBER)
        d.text(s, ML + 0.24, y + 0.18, 1.1, 0.32, f"0{i+1}", size=14, bold=True, color=AMBER, ml=0, mr=0, mt=0, mb=0)
        d.text(s, ML + 0.24, y + 0.50, CONTENT_W - 0.5, 0.55, '"' + quote + '"', size=16, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
        d.text(s, ML + 0.24, y + 1.10, CONTENT_W - 0.5, 0.46, gloss, size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)


def slide_delta(d: Deck) -> None:
    s = d.chrome("Delta", "Delta is their share count")
    d.panel(s, ML, 1.18, 7.55, 4.05, accent=BLUE)
    d.text(s, 0.64, 1.38, 7.1, 0.70, "One contract stands for 100 shares.\nExposure is delta times those 100 shares.", size=18, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    rows = [("Call delta 0.20", "about 20 shares"), ("Call delta 0.50", "about 50 shares"), ("Call delta 0.80", "about 80 shares")]
    for i, (left, right) in enumerate(rows):
        y = 2.30 + i * 0.85
        d.rect(s, 0.68, y, 3.15, 0.70, NEST)
        d.rect(s, 3.95, y, 3.55, 0.70, NEST)
        d.text(s, 0.68, y, 3.15, 0.70, left, size=16, color=BODY, align="center", anchor="middle", ml=0.08, mr=0.08, mt=0, mb=0)
        d.arrow(s, 3.68, y + 0.20, 0.22, 0.28, BLUE, "right")
        d.text(s, 3.95, y, 3.55, 0.70, right, size=16, bold=True, color=TEXT, align="center", anchor="middle", ml=0.08, mr=0.08, mt=0, mb=0)
    d.panel(s, 8.15, 1.18, 4.76, 4.05, accent=CORAL)
    d.text(s, 8.35, 1.40, 4.4, 0.40, "You are not the dealer", size=18, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    d.text(
        s, 8.35, 1.95, 4.35, 2.95,
        "You do not hedge with stock.\nYou do not short shares.\n\nYou read their hedge so you know the push.\nThen you buy a call, a put, or a debit spread.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )
    d.panel(s, ML, 5.40, CONTENT_W, 1.42, accent=AMBER)
    d.text(
        s, ML + 0.24, 5.55, CONTENT_W - 0.48, 1.12,
        "A long put with delta -0.50 acts like short 50 shares. You still only own the put.\nYou did not borrow stock. The sign is direction. The number is size. Later you will ignore the sign on purpose.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_gamma_def(d: Deck) -> None:
    s = d.chrome("Gamma", "Gamma is how fast delta changes")
    d.panel(s, ML, 1.18, CONTENT_W, 1.15, accent=AMBER)
    d.text(
        s, ML + 0.24, 1.32, CONTENT_W - 0.48, 0.88,
        "Dealers re-hedge when delta changes. Gamma sets how much, and how often.",
        size=22, bold=True, color=TEXT, anchor="middle", ml=0, mr=0, mt=0, mb=0,
    )
    block(
        d, s, ML, 2.52, 6.15, 2.95, "High gamma",
        "A small move changes delta a lot.\nThe share hedge is rebuilt in size.\nDealers are back in the stock often.\n\nThis is the strike, near expiry.",
        accent=CORAL, ts=18, bs=16,
    )
    block(
        d, s, 6.76, 2.52, 6.15, 2.95, "Low gamma",
        "The same move barely changes delta.\nThe hedge is a small update.\nThey can sit.\n\nThis is far from the strike, or far from expiry.",
        accent=BLUE, ts=18, bs=16,
    )
    d.text(
        s, ML, 5.65, CONTENT_W, 1.15,
        "Calls and puts have the same gamma. The sign of the book is a separate question.\nThe next slide is the shape, from the model. The one after that is the share count.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_gamma_chart(d: Deck) -> None:
    s = d.chrome("Black-Scholes", "Gamma peaks at the strike, near expiry")
    h = d.picture(s, d.charts["gamma"], ML, 1.12, 7.55)
    r1 = f"{FACTS['g_ratio_1']:.1f}"
    r7 = f"{FACTS['g_ratio_7']:.1f}"
    notes = [
        (TEAL, "The peak is at the money. Here, strike 100."),
        (CORAL, f"1-day gamma at the peak is about {r1} times the 30-day peak."),
        (AMBER, f"7-day gamma at the peak is about {r7} times the 30-day peak."),
        (BLUE, "Far from the strike the line is flat. Little re-hedging."),
    ]
    for i, (accent, line) in enumerate(notes):
        y = 1.18 + i * 1.22
        d.panel(s, 8.15, y, 4.76, 1.10)
        d.rect(s, 8.15, y, 0.08, 1.10, accent)
        d.text(s, 8.40, y + 0.14, 4.30, 0.82, line, size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.text(
        s, ML, 6.55, 7.6, 0.42,
        "Scaled so the 30-day peak is 1.",
        size=13, color=DIM, ml=0, mr=0, mt=0, mb=0,
    )
    # h is used only to keep the picture return honest
    _ = h
    d.text(
        s, ML, 6.78, CONTENT_W, 0.28,
        "EXAMPLE. Black-Scholes, European, no dividend. Spot 100, IV 20%, rate 4%. Not a forecast.",
        size=12, color=DIM, ml=0, mr=0, mt=0, mb=0,
    )


def slide_hedge_chart(d: Deck) -> None:
    s = d.chrome("Re-hedge", "One point of price, three hedges")
    d.picture(s, d.charts["hedge"], 0.55, 1.25, 6.90)
    sh = FACTS["shares"]
    block(
        d, s, 7.70, 1.20, 5.20, 3.55, "What the bars are",
        "EXAMPLE. The dealer is short one\nATM call. Strike 100.\n\nSpot goes from 100 to 101.\n\nThe bars are the shares they must\nbuy to get back to neutral.\n\n"
        + f"{sh[0]:.1f}, {sh[1]:.1f}, and {sh[2]:.1f} shares.",
        accent=CORAL, ts=18, bs=15,
    )
    d.panel(s, 7.70, 4.90, 5.20, 1.85, accent=TEAL)
    d.text(
        s, 7.90, 5.08, 4.85, 1.50,
        "Flip the book. If the dealer is long that call, the same sizes are shares they sell. Same gamma. Opposite trade.",
        size=15, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )
    d.text(
        s, ML, 6.78, CONTENT_W, 0.28,
        "EXAMPLE. Black-Scholes, European, no dividend. IV 20%, rate 4%. Share counts match the bars. Not a forecast.",
        size=12, color=DIM, ml=0, mr=0, mt=0, mb=0,
    )


def slide_regimes(d: Deck) -> None:
    s = d.chrome("Regimes", "Two ways the hedge can push")
    d.rect(s, ML, 1.22, 6.05, 4.55, TEAL_DIM, line=LINE)
    d.text(s, 0.66, 1.40, 5.6, 0.32, "POSITIVE GAMMA", size=14, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.66, 1.85, 5.6, 1.15, "Above the flip.\nDealers sell rallies and buy dips.", size=20, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    d.arrow(s, 1.15, 3.30, 0.40, 0.50, TEAL, "down")
    d.arrow(s, 2.55, 3.30, 0.40, 0.50, TEAL, "up")
    d.text(s, 0.85, 3.88, 1.05, 0.28, "sell", size=14, color=TEAL, align="center", ml=0, mr=0, mt=0, mb=0)
    d.text(s, 2.25, 3.88, 1.05, 0.28, "buy", size=14, color=TEAL, align="center", ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.66, 4.40, 5.5, 1.05, "Price ranges, and it can pin.\nPin means price sticks near a heavy strike.", size=16, color=BODY, ml=0, mr=0, mt=0, mb=0)

    d.rect(s, 6.87, 1.22, 6.04, 4.55, CORAL_DIM, line=LINE)
    d.text(s, 7.11, 1.40, 5.6, 0.32, "NEGATIVE GAMMA", size=14, bold=True, color=CORAL, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 7.11, 1.85, 5.6, 1.15, "Below the flip.\nDealers chase the move.", size=20, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    d.arrow(s, 7.60, 3.30, 0.40, 0.50, CORAL, "up")
    d.arrow(s, 9.00, 3.30, 0.40, 0.50, CORAL, "down")
    d.text(s, 7.30, 3.88, 1.05, 0.28, "buy", size=14, color=CORAL, align="center", ml=0, mr=0, mt=0, mb=0)
    d.text(s, 8.70, 3.88, 1.05, 0.28, "sell", size=14, color=CORAL, align="center", ml=0, mr=0, mt=0, mb=0)
    d.text(s, 7.11, 4.40, 5.5, 1.05, "Price can trend, and it can accelerate.\nFades get run over.", size=16, color=BODY, ml=0, mr=0, mt=0, mb=0)

    d.panel(s, ML, 5.95, CONTENT_W, 0.90, accent=AMBER)
    d.text(
        s, ML + 0.22, 6.08, CONTENT_W - 0.4, 0.64,
        "This deck reads dealer gamma. Above the flip is positive. Below the flip is negative.",
        size=16, color=TEXT, anchor="middle", ml=0, mr=0, mt=0, mb=0,
    )


def slide_positive(d: Deck) -> None:
    s = d.chrome("Positive gamma", "They sell the rally and buy the dip")
    d.panel(s, ML, 1.18, 8.15, 5.55)
    d.stamp(s, 0.62, 1.36, "ILLUSTRATIVE")
    # range
    d.hline(s, 1.15, 2.35, 6.6, CYAN, 0.03)
    d.hline(s, 1.15, 5.55, 6.6, PURPLE, 0.03)
    d.text(s, 1.15, 1.95, 3.2, 0.32, "Call wall", size=14, bold=True, color=CYAN, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 1.15, 5.68, 3.2, 0.32, "Put wall", size=14, bold=True, color=PURPLE, ml=0, mr=0, mt=0, mb=0)
    d.arrow(s, 3.55, 2.55, 0.42, 0.55, TEAL, "down")
    d.text(s, 4.15, 2.60, 3.3, 0.70, "Rally into the call wall.\nDealers sell stock.", size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.arrow(s, 3.55, 4.70, 0.42, 0.55, TEAL, "up")
    d.text(s, 4.15, 4.65, 3.3, 0.70, "Dip into the put wall.\nDealers buy stock.", size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 1.20, 3.55, 2.3, 0.70, "Price stays\nin the range.", size=15, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    # chop marks
    for i, yy in enumerate((3.15, 3.55, 3.95, 4.35)):
        xx = 2.55 + (i % 2) * 0.35
        d.oval(s, xx, yy, 0.14, 0.14, TEAL)
    block(
        d, s, 8.75, 1.18, 4.16, 5.55, "What you do",
        "Fade the edges.\n\nOnly after a rejection\ncandle closes back\ninside.\n\nDo not trade the\nbreakout.\n\nThe playbook is\na later slide.",
        accent=TEAL, ts=18, bs=16,
    )


def slide_negative(d: Deck) -> None:
    s = d.chrome("Negative gamma", "They chase, so the move can run")
    d.panel(s, ML, 1.18, 8.15, 5.55)
    d.stamp(s, 0.62, 1.36, "ILLUSTRATIVE")
    d.hline(s, 1.15, 2.55, 6.6, CYAN, 0.03)
    d.hline(s, 1.15, 5.15, 6.6, PURPLE, 0.03)
    d.text(s, 1.15, 2.15, 2.4, 0.32, "Call wall", size=14, bold=True, color=CYAN, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 1.15, 5.28, 2.4, 0.32, "Put wall", size=14, bold=True, color=PURPLE, ml=0, mr=0, mt=0, mb=0)
    d.arrow(s, 3.70, 1.50, 0.40, 0.52, CORAL, "up")
    d.text(s, 4.25, 1.48, 3.5, 0.70, "Rally. Dealers buy.\nThe rally gets fuel.", size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.arrow(s, 3.70, 5.45, 0.40, 0.52, CORAL, "down")
    d.text(s, 4.25, 5.40, 3.5, 0.85, "Drop. Dealers sell.\nThe drop gets fuel.", size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 1.20, 3.45, 2.5, 0.80, "A break can\nrun.", size=16, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    block(
        d, s, 8.75, 1.18, 4.16, 5.55, "What you do",
        "Do not fade the\nfirst touch.\n\nTrade the break\non a 4h close.\n\nGo with it.\n\nThe playbook is\na later slide.",
        accent=CORAL, ts=18, bs=16,
    )


def slide_hedge_sign(d: Deck) -> None:
    s = d.chrome("Example", "Same calls, opposite hedge")
    d.text(
        s, ML, 1.12, CONTENT_W, 0.55,
        "EXAMPLE. 10 contracts. Deltas are chosen so the share count is obvious. This is one call book, not every book.",
        size=15, color=DIM, ml=0, mr=0, mt=0, mb=0,
    )
    # positive
    d.panel(s, ML, 1.75, 6.15, 4.95, accent=TEAL)
    d.text(s, 0.64, 1.92, 5.7, 0.72, "Positive book\nDealer is long the calls", size=18, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    d.text(
        s, 0.64, 2.72, 5.7, 3.70,
        "Start. Delta +0.50.\nHedge: short 500 shares.\n\nLater. Delta +0.60.\nHedge: short 600 shares.\n\nThey sell 100 shares\ninto the rally.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )
    d.panel(s, 6.76, 1.75, 6.15, 4.95, accent=CORAL)
    d.text(s, 7.00, 1.92, 5.7, 0.72, "Negative book\nDealer is short the calls", size=18, bold=True, color=CORAL, ml=0, mr=0, mt=0, mb=0)
    d.text(
        s, 7.00, 2.72, 5.7, 3.70,
        "Start. Delta -0.50.\nHedge: long 500 shares.\n\nLater. Delta -0.60.\nHedge: long 600 shares.\n\nThey buy 100 shares\ninto the rally.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_flip(d: Deck) -> None:
    s = d.chrome("The flip", "The flip is a change in behavior")
    d.panel(s, ML, 1.18, 7.35, 5.55)
    d.text(s, 0.64, 1.36, 4.0, 0.30, "Price", size=13, bold=True, color=DIM, ml=0, mr=0, mt=0, mb=0)
    d.rect(s, 1.55, 1.85, 4.3, 1.85, TEAL_DIM)
    d.text(s, 1.75, 2.05, 3.95, 0.70, "Above the flip\nPositive gamma. Fade.", size=16, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    d.arrow(s, 5.95, 2.15, 0.36, 0.42, TEAL, "down")
    d.arrow(s, 5.95, 2.85, 0.36, 0.42, TEAL, "up")
    d.rect(s, 0.70, 3.70, 6.55, 0.08, AMBER)
    d.text(s, 0.70, 3.85, 6.55, 0.36, "FLIP    net gamma changes sign", size=14, bold=True, color=AMBER, align="center", ml=0, mr=0, mt=0, mb=0)
    d.rect(s, 1.55, 4.35, 4.3, 1.95, CORAL_DIM)
    d.text(s, 1.75, 4.55, 3.95, 0.80, "Below the flip\nNegative gamma. Chase.", size=16, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    d.arrow(s, 5.95, 4.50, 0.36, 0.42, CORAL, "up")
    d.arrow(s, 5.95, 5.20, 0.36, 0.42, CORAL, "down")
    block(
        d, s, 7.95, 1.18, 4.96, 2.55, "Not a level to lean on",
        "The flip marks a change\nin behavior.\n\nSupport and resistance\nare the walls.",
        accent=AMBER, ts=16, bs=16,
    )
    block(
        d, s, 7.95, 3.90, 4.96, 2.83, "It can sit on a wall",
        "The flip can fall between\ntwo strikes.\n\nIf it sits on a wall, that\nedge is the regime line\nand the level, together.",
        accent=BLUE, ts=16, bs=16,
    )


def slide_flip_quiet(d: Deck) -> None:
    s = d.chrome("The flip", "On the flip, the hedge goes quiet")
    d.panel(s, ML, 1.18, CONTENT_W, 2.55, accent=AMBER)
    d.text(
        s, ML + 0.28, 1.40, CONTENT_W - 0.55, 2.10,
        "There is near-zero hedging on the flip itself.\n\nPrice often consolidates there, until it picks a side.\nA tight chop on the line is not a signal. It is the wait.",
        size=20, color=TEXT, ml=0, mr=0, mt=0, mb=0,
    )
    steps = [
        (AMBER, "On the line", "Little stock to buy or sell for the gamma hedge. Price often sits."),
        (TEAL, "Accepts above", "A close holds above the flip. Expect fade behavior. Read it as positive."),
        (CORAL, "Accepts below", "A close holds below the flip. Expect chase behavior. Read it as negative."),
    ]
    for (x, w), (accent, title, body) in zip(cols(3), steps):
        block(d, s, x, 3.95, w, 2.75, title, body, accent=accent, ts=18, bs=16)


def slide_flip_close(d: Deck) -> None:
    s = d.chrome("The flip", "A wick is not a new side")
    # two candle panels
    d.panel(s, ML, 1.18, 6.15, 4.35)
    d.stamp(s, 0.60, 1.34, "ILLUSTRATIVE")
    d.hline(s, 0.70, 2.85, 5.55, AMBER, 0.028)
    d.text(s, 0.75, 2.48, 1.6, 0.30, "Flip", size=13, bold=True, color=AMBER, ml=0, mr=0, mt=0, mb=0)
    d.candle(s, 3.15, 1.85, 4.55, 3.55, 3.85, DIM)
    d.text(s, 3.55, 3.15, 2.6, 1.15, "Wick through.\nClose back on\nthe old side.", size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.70, 4.85, 5.5, 0.45, "Still the old regime.", size=16, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)

    d.panel(s, 6.76, 1.18, 6.15, 4.35)
    d.stamp(s, 6.94, 1.34, "ILLUSTRATIVE")
    d.hline(s, 7.05, 2.85, 1.35, AMBER, 0.028)
    d.text(s, 7.10, 2.48, 1.2, 0.30, "Flip", size=13, bold=True, color=AMBER, ml=0, mr=0, mt=0, mb=0)
    d.candle(s, 7.85, 1.70, 4.15, 2.15, 2.45, TEAL)
    d.text(s, 8.55, 2.15, 3.9, 1.20, "The close is through\nthe flip. It still\nhas to hold.", size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 7.05, 4.85, 5.5, 0.45, "Possible new side.", size=16, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)

    d.panel(s, ML, 5.70, CONTENT_W, 1.12, accent=BLUE)
    d.text(
        s, ML + 0.24, 5.86, CONTENT_W - 0.45, 0.82,
        "Use the 4h close, or the daily close. Do not change the plan on a touch.\nIf later candles hold on the new side, treat the regime as changed and read the book again.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_walls(d: Deck) -> None:
    s = d.chrome("Levels", "The walls are support and resistance")
    d.panel(s, ML, 1.18, 7.45, 5.55)
    d.stamp(s, 0.60, 1.34, "ILLUSTRATIVE")
    # schematic ladder, not to a real ticker
    levels = [
        (1.85, CYAN, "115   call wall    resistance"),
        (2.85, AMBER, "108   flip    behavior, not a wall"),
        (4.05, TEXT, "100   spot"),
        (5.35, PURPLE, "90    put wall    support"),
    ]
    d.vline(s, 1.55, 1.70, 4.55, LINE, 0.02)
    for y, color, label in levels:
        if color == AMBER:
            d.dashed_h(s, 1.15, y, 3.3, color, 0.02, 0.12, 0.08)
        else:
            d.hline(s, 1.15, y, 3.3, color, 0.028)
        d.oval(s, 1.47, y - 0.07, 0.16, 0.16, color)
        d.text(s, 4.55, y - 0.16, 3.05, 0.40, label, size=14, color=color, anchor="middle", ml=0, mr=0, mt=0, mb=0)
    block(
        d, s, 8.05, 1.18, 4.86, 5.55, "How to use them",
        "Call wall: the heavy call\nstrike above. Resistance.\n\nPut wall: the heavy put\nstrike below. Support.\n\nThey are the swing map.\n\nThe regime decides if you\nfade them, or if you trade\na close through them.\n\nThe flip is drawn here so\nyou do not confuse it\nwith a wall.",
        accent=CYAN, ts=18, bs=15,
    )


def slide_walls_regime(d: Deck) -> None:
    s = d.chrome("Levels", "The regime picks fade or break")
    block(
        d, s, ML, 1.18, 6.15, 5.55, "Positive gamma at a wall",
        "The hedge leans back\ninto the range.\n\nA tag is not the trade.\n\nA rejection candle that\ncloses back inside is\nthe fade.\n\nDo not buy the breakout\nwhile spot is still\nabove the flip.",
        accent=TEAL, ts=20, bs=18,
    )
    block(
        d, s, 6.76, 1.18, 6.15, 5.55, "Negative gamma at a wall",
        "The hedge can turn into\na chase once price goes\nthrough.\n\nA touch is not the trade.\n\nA 4h close outside the\nrange is the trade.\nGo with it.\n\nDo not fade the wall\nonly because it is a wall.",
        accent=CORAL, ts=20, bs=18,
    )


def slide_opex(d: Deck) -> None:
    s = d.chrome("Levels", "Walls move. Big expiries reset them")
    d.panel(s, ML, 1.18, 6.15, 5.55, accent=BLUE)
    d.text(s, 0.64, 1.40, 5.7, 0.40, "The wall is this book", size=20, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    # moving wall diagram
    d.text(s, 0.70, 2.05, 2.2, 0.30, "Earlier", size=13, bold=True, color=DIM, ml=0, mr=0, mt=0, mb=0)
    d.hline(s, 0.70, 2.55, 2.4, CYAN, 0.03)
    d.text(s, 3.20, 2.35, 1.5, 0.36, "call wall", size=14, color=CYAN, ml=0, mr=0, mt=0, mb=0)
    d.arrow(s, 2.55, 3.15, 0.36, 0.46, AMBER, "down")
    d.text(s, 3.05, 3.20, 2.6, 0.40, "open interest shifts", size=14, color=AMBER, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.70, 3.90, 2.2, 0.30, "Later", size=13, bold=True, color=DIM, ml=0, mr=0, mt=0, mb=0)
    d.hline(s, 0.70, 4.45, 2.4, CYAN, 0.03)
    d.text(s, 3.20, 4.25, 2.4, 0.36, "new call wall", size=14, color=CYAN, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.70, 5.15, 5.5, 1.25, "Read them again.\nYesterday's line can be dead.", size=18, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    block(
        d, s, 6.76, 1.18, 6.15, 5.55, "OPEX",
        "Open interest is what\nbuilds the wall.\n\nWhen that expiry passes,\nthose contracts are gone.\n\nThe monthly expiry is\nthe big reset.\n\nSPY also expires through\nthe week. After a large\none, rebuild the map\nbefore you trust the\nold levels.",
        accent=AMBER, ts=20, bs=18,
    )


def slide_charm(d: Deck) -> None:
    s = d.chrome("Textbook only", "Charm and vanna, in one pass")
    block(
        d, s, ML, 1.18, 6.15, 4.15, "Charm",
        "The change in delta as time\npasses, with price and IV\nheld still.\n\nAlso called delta decay.\n\nA hedge can drift on a flat\nday because the clock moved.",
        accent=BLUE, ts=22, bs=18,
    )
    block(
        d, s, 6.76, 1.18, 6.15, 4.15, "Vanna",
        "The change in delta when IV\nchanges, with price held still.\n\nIt is also the change in vega\nwhen price changes.\n\nA hedge can shift on a\nvolatility move, even if the\nstock has not.",
        accent=PURPLE, ts=22, bs=18,
    )
    d.panel(s, ML, 5.52, CONTENT_W, 1.28, accent=AMBER)
    d.text(
        s, ML + 0.24, 5.70, CONTENT_W - 0.48, 0.95,
        "Textbook definitions. This deck does not trade charm or vanna.\nYou trade gamma, the walls, and the close. These two only explain a hedge that moves on a quiet tape.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_uw_rules(d: Deck) -> None:
    s = d.chrome("Unusual Whales", "Four rules on your gamma page")
    rules = [
        ("01", "Heatmap colors are net gamma.", "Not put gamma. Not call gamma by itself. The combined number."),
        ("02", "By-strike draws two lines.", "The call wall, and spot. It does not draw the put wall. It does not draw the flip."),
        ("03", "You find the put wall.", "It is the longest purple bar below spot."),
        ("04", "You find the flip.", "It is where the heatmap color changes. Not a printed line."),
    ]
    for i, (num, title, body) in enumerate(rules):
        col = i % 2
        row = i // 2
        x = ML + col * 6.34
        y = 1.18 + row * 2.35
        d.panel(s, x, y, 6.15, 2.18, accent=PURPLE)
        d.text(s, x + 0.2, y + 0.16, 1.0, 0.36, num, size=14, bold=True, color=PURPLE, ml=0, mr=0, mt=0, mb=0)
        d.text(s, x + 0.2, y + 0.52, 5.75, 0.45, title, size=18, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
        d.text(s, x + 0.2, y + 1.10, 5.75, 0.85, body, size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.text(
        s, ML, 5.95, CONTENT_W, 0.85,
        "Open interest is the swing. Directionalized Volume is the day. The next drawings are schematics.\nThey are marked ILLUSTRATIVE. They are not screenshots, and the heatmap colors are stand-ins.",
        size=15, color=DIM, ml=0, mr=0, mt=0, mb=0,
    )


def slide_heatmap(d: Deck) -> None:
    s = d.chrome("Heatmap", "The color is net gamma")
    d.stamp(s, ML, 1.12, "ILLUSTRATIVE")
    d.text(s, 2.50, 1.14, 8.5, 0.30, "Stand-in colors. Not the Unusual Whales palette.", size=14, color=AMBER, ml=0, mr=0, mt=0, mb=0)
    headers = ["0DTE", "+2d", "+7d", "+14d", "month", "+2mo"]
    pos = [800, 790, 780, 770]
    neg = [760, 750, 740, 730]
    gx = 1.35
    header_y = 1.58
    cell_w, cell_h, gap = 0.92, 0.46, 0.06
    for i, label in enumerate(headers):
        d.text(s, gx + i * (cell_w + gap), header_y, cell_w, 0.28, label, size=12, bold=True, color=DIM, align="center", ml=0, mr=0, mt=0, mb=0)
    def draw_row(y, strike, fill, mark):
        d.text(s, 0.42, y, 0.85, cell_h, str(strike), size=13, bold=True, color=DIM, align="right", anchor="middle", ml=0, mr=0.06, mt=0, mb=0)
        for i in range(6):
            x = gx + i * (cell_w + gap)
            d.rect(s, x, y, cell_w, cell_h, fill)
            d.text(s, x, y, cell_w, cell_h, mark, size=13, bold=True, color=TEXT, align="center", anchor="middle", ml=0, mr=0, mt=0, mb=0)
    y = 1.95
    for strike in pos:
        draw_row(y, strike, "1C6B58", "+")
        y += cell_h + gap
    d.rect(s, gx, y + 0.02, 6 * cell_w + 5 * gap, 0.045, AMBER)
    d.text(s, gx, y + 0.08, 5.8, 0.28, "FLIP  =  where the color changes", size=13, bold=True, color=AMBER, ml=0, mr=0, mt=0, mb=0)
    y += 0.42
    for strike in neg:
        draw_row(y, strike, "7A3038", "-")
        y += cell_h + gap
    d.panel(s, 8.55, 1.58, 4.35, 5.05, accent=PURPLE)
    d.text(s, 8.75, 1.80, 4.0, 0.70, "Read it this way", size=18, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    d.text(
        s, 8.75, 2.55, 3.95, 3.80,
        "Plus cells: positive\nnet gamma.\n\nMinus cells: negative\nnet gamma.\n\nThe sign is the lesson.\nThe shade is not live data.\n\nOn the real page, match\nthe color to the legend.\nDo not memorize a hue.",
        size=15, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_bystrike(d: Deck) -> None:
    s = d.chrome("By strike", "This chart does not draw every level")
    d.stamp(s, ML, 1.12, "ILLUSTRATIVE")
    strikes = [
        (790, 36), (785, 58), (780, 128), (775, 84), (770, 48),
        (765, 40), (760, 160), (755, 72), (750, 108), (745, 30),
    ]
    top = 1.58
    pitch = 0.50
    label_x = 0.42
    bar_x = 1.25
    max_w = 4.70
    scale = max_w / 160
    d.panel(s, 0.42, 1.50, 6.15, 5.25)
    for i, (strike, length) in enumerate(strikes):
        y = top + i * pitch
        d.text(s, label_x, y, 0.72, 0.36, str(strike), size=12, bold=True, color=DIM, align="right", anchor="middle", ml=0, mr=0.04, mt=0, mb=0)
        d.rect(s, bar_x, y + 0.04, length * scale, 0.28, "A78BFA")
    # spot between 765 (index 5) and 760 (index 6)
    y765 = top + 5 * pitch + 0.18
    y760 = top + 6 * pitch + 0.18
    spot_y = (y765 + y760) / 2
    d.hline(s, bar_x, spot_y, max_w, WHITE, 0.022)
    d.text(s, bar_x + max_w - 0.85, spot_y - 0.30, 0.80, 0.26, "spot", size=12, bold=True, color=WHITE, align="right", ml=0, mr=0, mt=0, mb=0)
    # call wall marker starts after the 775 bar, so the label is not on the bar
    call_y = top + 3 * pitch + 0.18
    bar_end = bar_x + 84 * scale
    d.hline(s, bar_end + 0.10, call_y, max_w - (84 * scale) - 0.10, CYAN, 0.028)
    d.text(s, bar_end + 0.12, call_y - 0.30, 1.45, 0.26, "call wall", size=12, bold=True, color=CYAN, ml=0, mr=0, mt=0, mb=0)

    notes = [
        (CYAN, "Drawn for you", "Spot, and the call wall. Those two lines are on the chart."),
        (PURPLE, "You mark the put wall", "Longest purple bar below spot. Here that is 760. It is not drawn as a line."),
        (AMBER, "Ignore the trap", "The long bar at 780 is above spot. Longest bar on the wrong side is not the put wall."),
        (CORAL, "Flip is not here", "Do not look for it on this chart. The color change is on the heatmap."),
    ]
    for i, (accent, title, body) in enumerate(notes):
        y = 1.18 + i * 1.38
        d.panel(s, 6.78, y, 6.13, 1.26)
        d.rect(s, 6.78, y, 0.08, 1.26, accent)
        d.text(s, 7.04, y + 0.08, 5.7, 0.32, title, size=15, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
        d.text(s, 7.04, y + 0.42, 5.7, 0.74, body, size=14, color=BODY, ml=0, mr=0, mt=0, mb=0)


def slide_oi_volume(d: Deck) -> None:
    s = d.chrome("Two clocks", "Open interest is the swing. Volume is the day")
    block(
        d, s, ML, 1.18, 6.15, 4.35, "Open interest",
        "Contracts that are still open.\n\nThis is the book already on.\n\nIt builds the walls and\nthe flip.\n\nUse it for swing levels\nand for the regime.",
        accent=TEAL, ts=22, bs=18,
    )
    block(
        d, s, 6.76, 1.18, 6.15, 4.35, "Directionalized Volume",
        "What traded in the session,\nwith a direction on the flow.\n\nThis is the intraday view.\n\nIt does not set the swing\nwall, and it does not set\nthe monthly regime.",
        accent=AMBER, ts=22, bs=18,
    )
    d.panel(s, ML, 5.72, CONTENT_W, 1.10, accent=CORAL)
    d.text(
        s, ML + 0.24, 5.88, CONTENT_W - 0.48, 0.80,
        "Do not swap them. A midday push on Directionalized Volume does not move your wall.",
        size=18, color=TEXT, anchor="middle", ml=0, mr=0, mt=0, mb=0,
    )


def slide_crosscheck(d: Deck) -> None:
    s = d.chrome("Check", "Check the three levels in public")
    d.panel(s, ML, 1.18, 5.9, 5.55, accent=BLUE)
    d.text(s, 0.66, 1.40, 5.4, 0.40, "Write these down", size=20, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    for i, (name, gloss) in enumerate((("Put wall", "Support. From open interest."), ("Call wall", "Resistance. From open interest."), ("Flip", "Where net gamma changes sign."))):
        y = 2.05 + i * 1.35
        d.rect(s, 0.70, y, 0.56, 0.56, BLUE_DIM, line=BLUE, line_w=1.25)
        d.text(s, 0.70, y, 0.56, 0.56, str(i + 1), size=18, bold=True, color=BLUE, align="center", anchor="middle", ml=0, mr=0, mt=0, mb=0)
        d.text(s, 1.45, y, 4.4, 0.36, name, size=18, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
        d.text(s, 1.45, y + 0.40, 4.4, 0.40, gloss, size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)
    block(
        d, s, 6.52, 1.18, 6.39, 5.55, "If the second source disagrees",
        "You want the same story,\nnot the same pixel.\n\nSame expiry?\n\nOpen interest, not today's\nvolume?\n\nDealer gamma, or the\ncustomer sign? Customer\ngamma flips the colors.\n\nIf it still disagrees, you\nstill need a close. No trade\noff a level you cannot\nfind twice.",
        accent=AMBER, ts=18, bs=16,
    )


def slide_month(d: Deck) -> None:
    s = d.chrome("Time", "The month sets the posture")
    block(
        d, s, ML, 1.18, 6.15, 3.35, "Today's open interest",
        "Sets the playbook.\n\nSpot above the flip:\npositive. You fade.\n\nSpot below the flip:\nnegative. You trade\nthe break.",
        accent=TEAL, ts=20, bs=18,
    )
    block(
        d, s, 6.76, 1.18, 6.15, 3.35, "The past month",
        "Sets the risk posture.\n\nA positive month is a\npinning environment.\n\nA negative month is\nfaster. Breaks can run.\nStops need more room.",
        accent=AMBER, ts=20, bs=18,
    )
    d.panel(s, ML, 4.72, CONTENT_W, 2.05, accent=BLUE)
    d.text(
        s, ML + 0.28, 4.92, CONTENT_W - 0.55, 1.65,
        "The room changes how many contracts your dollars buy.\nThe dollar amount is still yours, every trade.\nThis deck never sets a percent, and it never sets a dollar risk.\nIf today and the month disagree, trade today's book. Let the month change the room, not the playbook.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_clocks(d: Deck) -> None:
    s = d.chrome("Time", "Where each clock sits")
    clocks = [
        ("1", "Month", "Risk posture. You pick the dollars.", AMBER),
        ("2", "Open interest", "Walls, the flip, and the playbook.", TEAL),
        ("3", "4h close", "The range, and the trigger.", BLUE),
        ("4", "15m", "Entry timing. The 20, 50, and 200.", PURPLE),
    ]
    for i, (num, title, body, accent) in enumerate(clocks):
        y = 1.18 + i * 1.20
        d.panel(s, ML, y, 8.05, 1.08, accent=accent)
        d.text(s, 0.62, y + 0.16, 0.55, 0.70, num, size=20, bold=True, color=accent, anchor="middle", ml=0, mr=0, mt=0, mb=0)
        d.text(s, 1.30, y + 0.12, 6.8, 0.36, title, size=18, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
        d.text(s, 1.30, y + 0.52, 6.8, 0.42, body, size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)
    block(
        d, s, 8.65, 1.18, 4.26, 5.55, "Two extras",
        "A daily close is the\none to add when the\nlevel is a major wall,\nor the flip.\n\nThe averages do not\nreplace the walls.\nThey confirm them.\n\nThe 15m does not\noverrule the 4h.",
        accent=BLUE, ts=18, bs=16,
    )


def slide_align(d: Deck) -> None:
    s = d.chrome("Price and gamma", "Trade the range and the walls together")
    # aligned
    d.panel(s, ML, 1.18, 6.15, 4.20)
    d.stamp(s, 0.58, 1.32, "ILLUSTRATIVE")
    d.text(s, 0.62, 1.72, 3.0, 0.32, "They line up", size=18, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    d.rect(s, 1.10, 2.30, 3.3, 2.55, "1A2836", line=TEAL, line_w=1.5)
    d.text(s, 4.55, 2.25, 1.8, 0.55, "Call wall\n= box top", size=14, color=CYAN, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 4.55, 4.25, 1.8, 0.55, "Put wall\n= box bottom", size=14, color=PURPLE, ml=0, mr=0, mt=0, mb=0)
    # conflict
    d.panel(s, 6.76, 1.18, 6.15, 4.20)
    d.stamp(s, 6.92, 1.32, "ILLUSTRATIVE")
    d.text(s, 6.96, 1.72, 4.0, 0.32, "They do not", size=18, bold=True, color=CORAL, ml=0, mr=0, mt=0, mb=0)
    d.hline(s, 7.3, 2.35, 2.3, CYAN, 0.03)
    d.rect(s, 7.55, 2.85, 1.8, 1.35, "1A2836", line=AMBER, line_w=1.5)
    d.hline(s, 7.3, 4.70, 2.3, PURPLE, 0.03)
    d.text(s, 9.7, 2.15, 2.8, 0.45, "Walls outside", size=14, color=CYAN, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 9.7, 3.25, 2.8, 0.70, "4h box is\nonly the middle", size=14, color=AMBER, ml=0, mr=0, mt=0, mb=0)
    d.panel(s, ML, 5.55, CONTENT_W, 1.25, accent=TEAL)
    d.text(
        s, ML + 0.24, 5.72, CONTENT_W - 0.48, 0.95,
        "It works best when they line up. Then the playbook levels and the chart levels are the same prices.\nWhen they are not, you have two stories. Do not average them into a new price.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_disagree(d: Deck) -> None:
    s = d.chrome("Price and gamma", "If the maps disagree, wait")
    items = [
        (AMBER, "Box inside the walls", "The edges of the box are price action only. Do not call them walls. The walls are still outside."),
        (BLUE, "Through a wall, no close", "Price has poked a wall and the 4h has not closed out. Wait for that close. A wick is not a side."),
        (CORAL, "Wall inside the box", "The wall is the level. The rest of the box is range. Do not split the difference and invent a third price."),
    ]
    for i, (accent, title, body) in enumerate(items):
        y = 1.18 + i * 1.85
        d.panel(s, ML, y, CONTENT_W, 1.72, accent=accent)
        d.text(s, ML + 0.24, y + 0.16, CONTENT_W - 0.5, 0.40, title, size=20, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
        d.text(s, ML + 0.24, y + 0.68, CONTENT_W - 0.5, 0.85, body, size=16, color=BODY, ml=0, mr=0, mt=0, mb=0)


def slide_spy_numbers(d: Deck) -> None:
    s = d.chrome("October 16, 2026", "The SPY book from that close")
    cards = [
        (PURPLE, "Put wall", "760", "Support. Bottom of the box."),
        (CYAN, "Call wall", "775", "Resistance. Top of the box."),
        (AMBER, "Flip", "about 774.5", "Behavior change. On the ceiling."),
        (TEXT, "Spot", "about 763.2", "Under the flip. Inside the walls."),
    ]
    for (x, w), (accent, name, value, gloss) in zip(cols(4, gap=0.16), cards):
        d.panel(s, x, 1.22, w, 3.15, accent=accent)
        d.text(s, x + 0.16, 1.40, w - 0.32, 0.32, name, size=14, bold=True, color=accent, ml=0, mr=0, mt=0, mb=0)
        d.text(s, x + 0.16, 1.85, w - 0.32, 0.85, value, size=28, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
        d.text(s, x + 0.16, 2.90, w - 0.32, 1.15, gloss, size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.rect(s, ML, 4.55, CONTENT_W, 1.05, CORAL_DIM, line=CORAL, line_w=1.25)
    d.text(
        s, ML + 0.24, 4.68, CONTENT_W - 0.48, 0.80,
        "Regime: negative gamma. Spot is under the flip. Most of 760 to 775 is under it too.",
        size=18, color=TEXT, anchor="middle", ml=0, mr=0, mt=0, mb=0,
    )
    d.text(
        s, ML, 5.80, CONTENT_W, 0.95,
        "These are the open-interest levels from the October 16, 2026 SPY close, as used for this example.\n775 minus 760 is 15 points. On spot about 763, that box is about 2% wide.",
        size=15, color=DIM, ml=0, mr=0, mt=0, mb=0,
    )


def slide_spy_box(d: Deck) -> None:
    s = d.chrome("October 16, 2026", "The 4h range was the walls")
    d.panel(s, ML, 1.16, 7.85, 5.60)
    pmin, pmax = 754.0, 782.0
    top, bot = 1.70, 6.35
    axis_x = 2.15
    d.vline(s, axis_x, top, bot - top, LINE, 0.02)
    # range shade
    y_call = ymap(775, pmin, pmax, top, bot)
    y_put = ymap(760, pmin, pmax, top, bot)
    y_flip = ymap(774.5, pmin, pmax, top, bot)
    y_spot = ymap(763.2, pmin, pmax, top, bot)
    d.rect(s, 2.45, y_call, 3.55, y_put - y_call, "243044")
    d.text(s, 2.60, (y_call + y_put) / 2 - 0.28, 3.2, 0.55, "4h range\n760 to 775", size=16, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    d.hline(s, 1.85, y_call, 4.35, CYAN, 0.03)
    d.dashed_h(s, 1.85, y_flip, 4.35, AMBER, 0.018, 0.10, 0.07)
    d.hline(s, 1.85, y_put, 4.35, PURPLE, 0.03)
    d.oval(s, 2.85, y_spot - 0.09, 0.18, 0.18, WHITE)
    d.text(s, 6.30, y_call - 0.18, 1.75, 0.32, "775 call wall", size=13, bold=True, color=CYAN, anchor="middle", ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.55, y_flip - 0.16, 1.20, 0.32, "flip", size=13, bold=True, color=AMBER, anchor="middle", ml=0, mr=0, mt=0, mb=0)
    d.text(s, 6.30, y_spot - 0.16, 1.75, 0.32, "763.2 spot", size=13, bold=True, color=WHITE, anchor="middle", ml=0, mr=0, mt=0, mb=0)
    d.text(s, 6.30, y_put - 0.16, 1.75, 0.32, "760 put", size=13, bold=True, color=PURPLE, anchor="middle", ml=0, mr=0, mt=0, mb=0)
    # zoom
    d.panel(s, 8.45, 1.16, 4.46, 2.55, accent=AMBER)
    d.text(s, 8.65, 1.32, 4.1, 0.30, "Top of the box, opened up", size=14, bold=True, color=AMBER, ml=0, mr=0, mt=0, mb=0)
    ztop, zbot = 1.80, 3.40
    zy_call = ymap(775, 773.5, 776.2, ztop, zbot)
    zy_flip = ymap(774.5, 773.5, 776.2, ztop, zbot)
    d.hline(s, 8.75, zy_call, 2.3, CYAN, 0.03)
    d.dashed_h(s, 8.75, zy_flip, 2.3, AMBER, 0.018, 0.10, 0.06)
    d.text(s, 11.15, zy_call - 0.16, 1.55, 0.32, "775", size=14, bold=True, color=CYAN, anchor="middle", ml=0, mr=0, mt=0, mb=0)
    d.text(s, 11.15, zy_flip - 0.16, 1.55, 0.32, "774.5", size=14, bold=True, color=AMBER, anchor="middle", ml=0, mr=0, mt=0, mb=0)
    d.text(s, 8.65, 3.22, 4.05, 0.36, "Half a point apart. Linear scale.", size=12, color=DIM, ml=0, mr=0, mt=0, mb=0)
    block(
        d, s, 8.45, 3.88, 4.46, 2.88, "What the picture says",
        "The box and the walls\nare the same prices.\n\nThe flip is glued to\nthe call wall.\n\nAlmost the whole box\nis negative gamma.",
        accent=CORAL, ts=16, bs=15,
    )


def slide_spy_plan(d: Deck) -> None:
    s = d.chrome("October 16, 2026", "What you do with that book")
    cards = [
        (CORAL, "Close through 760", "Still under the flip.\nNegative gamma stands.\nGo with the downside.\nPut side."),
        (AMBER, "Poke, then back in", "The close is inside\nthe box.\nFailed break.\nNo trade. Old plan."),
        (TEAL, "Holds above 775", "You crossed the flip\nand the call wall.\nRegime likely changed.\nRe-read before you act."),
    ]
    for (x, w), (accent, title, body) in zip(cols(3), cards):
        block(d, s, x, 1.20, w, 3.55, title, body, accent=accent, ts=18, bs=16)
    d.panel(s, ML, 4.95, CONTENT_W, 1.82, accent=BLUE)
    d.text(
        s, ML + 0.24, 5.12, CONTENT_W - 0.48, 1.48,
        "Inside 760 to 775 you wait. The regime in the box is negative, so you do not fade either wall.\nThe upside is not a normal break. The flip is about 774.5, so a hold above 775 is a new book.\nDo not fade it on the old plan, and do not chase it on the old plan.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )

def slide_pos_play(d: Deck) -> None:
    s = d.chrome("Playbook", "Positive gamma: fade the edge")
    rules = [
        "1   Spot is above the flip. The regime is positive.",
        "2   Price tags the call wall, or the put wall.",
        "3   A rejection candle closes back inside the range.",
        "4   Enter on that close. Not on the tag.",
        "5   Stop is beyond that candle's high, or its low.",
        "6   You exit if a later candle closes past that extreme.",
        "7   Do not trade the breakout while this regime holds.",
    ]
    d.panel(s, ML, 1.18, 8.05, 5.55, accent=TEAL)
    d.text(s, 0.64, 1.36, 7.6, 0.36, "The rules", size=18, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.64, 1.85, 7.6, 4.55, "\n".join(rules), size=16, color=BODY, ml=0, mr=0, mt=0, mb=0, spacing=1.22)
    block(
        d, s, 8.65, 1.18, 4.26, 2.55, "Which contract",
        "Fade the call wall\nwith a put.\n\nFade the put wall\nwith a call.",
        accent=TEAL, ts=16, bs=16,
    )
    block(
        d, s, 8.65, 3.90, 4.26, 2.83, "If it holds outside",
        "A close outside is not\nyour entry here.\n\nIf that close holds,\nthe regime likely\nchanged. Rebuild.\nDo not chase it\non this plan.",
        accent=AMBER, ts=16, bs=15,
    )


def slide_pos_candle(d: Deck) -> None:
    s = d.chrome("Playbook", "What the rejection has to look like")
    d.panel(s, ML, 1.16, 8.35, 5.60)
    d.stamp(s, 6.15, 1.30, "ILLUSTRATIVE")
    # call wall near top, put wall near bottom
    d.hline(s, 0.70, 2.15, 5.3, CYAN, 0.03)
    d.hline(s, 0.70, 5.55, 5.3, PURPLE, 0.03)
    d.text(s, 0.75, 1.78, 2.2, 0.30, "Call wall", size=13, bold=True, color=CYAN, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.75, 5.68, 2.2, 0.30, "Put wall", size=13, bold=True, color=PURPLE, ml=0, mr=0, mt=0, mb=0)
    # rejection at call wall: wick above line, close below line
    d.candle(s, 2.15, 1.70, 3.55, 2.85, 3.15, TEAL)
    d.text(s, 2.50, 1.58, 2.7, 0.30, "Stop beyond this high", size=12, color=CORAL, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 2.55, 2.95, 2.6, 0.55, "Enter on this\nclose, inside", size=13, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    # rejection at put wall
    d.candle(s, 4.55, 4.15, 6.15, 4.85, 5.15, TEAL)
    d.text(s, 4.95, 4.72, 2.7, 0.60, "Enter on this\nclose, inside", size=13, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 4.95, 6.20, 3.0, 0.30, "Stop beyond this low", size=12, color=CORAL, ml=0, mr=0, mt=0, mb=0)
    block(
        d, s, 8.95, 1.16, 3.96, 5.60, "The close decides",
        "The wick can leave\nthe range.\n\nThe body has to finish\nback inside.\n\nA close outside is not\na fade.\n\nThe stop sits beyond\nthe rejection extreme.\nA wick through the stop\nis not the exit.\nA later close through\nit is.",
        accent=TEAL, ts=16, bs=14,
    )


def slide_neg_play(d: Deck) -> None:
    s = d.chrome("Playbook", "Negative gamma: trade the break")
    rules = [
        "1   Spot is below the flip. The regime is negative.",
        "2   Inside the range, you do nothing.",
        "3   A 4h candle closes outside, through the wall.",
        "4   Go with that close.",
        "5   Down break: put side. Up break: call side if still under the flip.",
        "6   You exit if a later 4h close comes back inside.",
        "7   Do not fade the first touch.",
    ]
    d.panel(s, ML, 1.18, 8.05, 5.55, accent=CORAL)
    d.text(s, 0.64, 1.36, 7.6, 0.36, "The rules", size=18, bold=True, color=CORAL, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.64, 1.85, 7.6, 4.55, "\n".join(rules), size=16, color=BODY, ml=0, mr=0, mt=0, mb=0, spacing=1.22)
    block(
        d, s, 8.65, 1.18, 4.26, 2.55, "Which contract",
        "Break up: long call,\nor a call debit spread.\n\nBreak down: long put,\nor a put debit spread.",
        accent=CORAL, ts=16, bs=16,
    )
    block(
        d, s, 8.65, 3.90, 4.26, 2.83, "If the break is the flip",
        "A normal negative break\nstays under the flip.\n\nIf the close also crosses\nthe flip, a hold means\nthe regime likely changed.\nRe-read before the\nnext trade.",
        accent=AMBER, ts=16, bs=15,
    )


def slide_neg_candle(d: Deck) -> None:
    s = d.chrome("Playbook", "What the break has to look like")
    d.panel(s, ML, 1.16, 8.35, 5.60)
    d.stamp(s, 6.15, 1.32, "ILLUSTRATIVE")
    d.hline(s, 0.75, 2.55, 5.4, CYAN, 0.03)
    d.hline(s, 0.75, 5.15, 5.4, PURPLE, 0.03)
    d.text(s, 0.80, 2.18, 2.2, 0.30, "Call wall", size=13, bold=True, color=CYAN, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.80, 5.28, 2.2, 0.30, "Put wall", size=13, bold=True, color=PURPLE, ml=0, mr=0, mt=0, mb=0)
    # upside break candle closes above the call wall
    d.candle(s, 2.35, 1.55, 3.35, 1.80, 2.15, CORAL)
    d.text(s, 2.75, 1.48, 2.8, 0.70, "4h close\nthrough. Enter.", size=14, color=CORAL, ml=0, mr=0, mt=0, mb=0)
    # downside break
    d.candle(s, 5.15, 4.35, 6.25, 5.55, 5.90, CORAL)
    d.text(s, 5.50, 5.35, 2.6, 0.70, "4h close\nthrough. Enter.", size=14, color=CORAL, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.85, 3.45, 4.3, 0.70, "Inside the range:\nno trade.", size=15, color=DIM, ml=0, mr=0, mt=0, mb=0)
    block(
        d, s, 8.95, 1.16, 3.96, 5.60, "The failed break",
        "You are wrong if a\nlater 4h candle closes\nback inside the range.\n\nThat is the stop.\n\nA wick back inside\nis not the exit.\nThe close is.\n\nHard loss is still\nthe debit, if the\noption goes to zero.",
        accent=CORAL, ts=16, bs=14,
    )


def slide_poke(d: Deck) -> None:
    s = d.chrome("Breaks", "A poke is not a break")
    d.panel(s, ML, 1.18, 6.15, 4.35)
    d.stamp(s, 0.58, 1.32, "ILLUSTRATIVE")
    d.text(s, 0.64, 1.72, 5.5, 0.34, "Fails", size=20, bold=True, color=AMBER, ml=0, mr=0, mt=0, mb=0)
    d.hline(s, 0.75, 2.85, 5.4, LINE, 0.02)
    d.text(s, 0.80, 2.52, 1.5, 0.28, "Range", size=12, color=DIM, ml=0, mr=0, mt=0, mb=0)
    d.candle(s, 2.35, 2.15, 4.15, 3.15, 3.45, DIM)
    d.candle(s, 3.55, 3.05, 4.35, 3.35, 3.85, DIM)
    d.text(s, 4.15, 3.20, 2.1, 1.15, "Pushes out.\nCloses back in.\nNext bar stays in.", size=14, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.70, 4.75, 5.5, 0.50, "Old plan stands. No chase.", size=16, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)

    d.panel(s, 6.76, 1.18, 6.15, 4.35)
    d.stamp(s, 6.94, 1.32, "ILLUSTRATIVE")
    d.text(s, 7.00, 1.72, 5.5, 0.34, "Holds", size=20, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    d.hline(s, 7.05, 3.35, 5.4, LINE, 0.02)
    d.text(s, 7.10, 3.02, 1.5, 0.28, "Range", size=12, color=DIM, ml=0, mr=0, mt=0, mb=0)
    d.candle(s, 8.35, 1.95, 3.85, 2.25, 2.65, TEAL)
    d.candle(s, 9.70, 1.85, 3.15, 2.15, 2.55, TEAL)
    d.text(s, 10.15, 3.55, 2.4, 1.05, "Closes out.\nThe next close\nstays out.", size=14, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 7.05, 4.75, 5.5, 0.50, "Regime likely changed.", size=16, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)

    d.panel(s, ML, 5.70, CONTENT_W, 1.10, accent=AMBER)
    d.text(
        s, ML + 0.22, 5.84, CONTENT_W - 0.44, 0.82,
        "One close starts the idea. A hold is what changes the regime. If a later close snaps back inside, it did not hold.",
        size=16, color=BODY, anchor="middle", ml=0, mr=0, mt=0, mb=0,
    )


def slide_rebuild(d: Deck) -> None:
    s = d.chrome("Breaks", "When it holds, change the plan")
    steps = [
        ("1", "Close outside", "A 4h or daily candle finishes outside the old range."),
        ("2", "It holds", "A later candle is still closed outside. It did not come back in."),
        ("3", "Call it changed", "The regime likely changed. Stop using the old fade or the old break."),
        ("4", "Read the book", "New walls. New flip. New side of spot. Then the new playbook."),
    ]
    for i, (num, title, body) in enumerate(steps):
        x = ML + (i % 4) * 3.15
        d.panel(s, x, 1.22, 3.00, 3.15, accent=AMBER)
        d.text(s, x + 0.16, 1.40, 2.7, 0.40, num, size=20, bold=True, color=AMBER, ml=0, mr=0, mt=0, mb=0)
        d.text(s, x + 0.16, 1.90, 2.7, 0.45, title, size=16, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
        d.text(s, x + 0.16, 2.45, 2.7, 1.65, body, size=14, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.panel(s, ML, 4.58, CONTENT_W, 2.18, accent=CORAL)
    d.text(
        s, ML + 0.24, 4.78, CONTENT_W - 0.48, 1.80,
        "Already negative, and the break does not cross the flip: the first 4h close outside is the entry. That is the negative playbook.\nWas positive, or the close crosses the flip: the first close outside is a warning, not a chase. Wait to see if it holds, then re-read.\nIf it closes back inside, it was not a change. You are on the old plan.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_alerts(d: Deck) -> None:
    s = d.chrome("Entries", "Alerts fire on the close")
    d.panel(s, ML, 1.18, 6.15, 4.15)
    d.text(s, 0.64, 1.36, 5.6, 0.36, "Touch. No alert.", size=18, bold=True, color=CORAL, ml=0, mr=0, mt=0, mb=0)
    d.hline(s, 0.80, 2.55, 3.4, AMBER, 0.028)
    d.text(s, 0.85, 2.18, 1.4, 0.30, "Level", size=13, color=AMBER, ml=0, mr=0, mt=0, mb=0)
    d.candle(s, 2.35, 1.90, 4.15, 3.05, 3.45, DIM)
    d.text(s, 2.85, 2.85, 3.3, 1.15, "The wick tags\nthe level.\nThe close is back.\nYou do nothing.", size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)

    d.panel(s, 6.76, 1.18, 6.15, 4.15)
    d.text(s, 7.00, 1.36, 5.6, 0.36, "Close. Alert.", size=18, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    d.hline(s, 7.10, 3.05, 1.25, AMBER, 0.028)
    d.text(s, 7.15, 2.68, 1.2, 0.30, "Level", size=13, color=AMBER, ml=0, mr=0, mt=0, mb=0)
    d.candle(s, 7.85, 1.75, 4.05, 2.15, 2.55, TEAL)
    d.text(s, 8.55, 2.35, 3.9, 1.35, "The candle finishes\nthrough the level.\nThen you check\nthe rest.", size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)

    d.panel(s, ML, 5.52, CONTENT_W, 1.28, accent=BLUE)
    d.text(
        s, ML + 0.24, 5.68, CONTENT_W - 0.48, 0.98,
        "4h or daily. Those are the swing closes. Never an intraday touch.\nIn TradingView, fire the alert on the bar close. A crossing alert can fire mid-candle. That is a touch.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_watch(d: Deck) -> None:
    s = d.chrome("Entries", "A watch alert, then an entry alert")
    d.panel(s, ML, 1.18, CONTENT_W, 3.15)
    d.stamp(s, 0.58, 1.32, "ILLUSTRATIVE")
    d.text(s, 2.55, 1.32, 6.0, 0.30, "A level at 100. Not the SPY book.", size=14, color=DIM, ml=0, mr=0, mt=0, mb=0)
    # price line
    d.hline(s, 1.3, 2.85, 10.5, LINE, 0.02)
    # zone band
    d.rect(s, 7.55, 2.55, 1.55, 0.62, AMBER_DIM, line=AMBER, line_w=1.15)
    d.text(s, 7.55, 2.15, 1.55, 0.32, "Band", size=13, bold=True, color=AMBER, align="center", ml=0, mr=0, mt=0, mb=0)
    d.oval(s, 9.55, 2.74, 0.22, 0.22, TEAL)
    d.text(s, 8.85, 3.30, 2.3, 0.55, "Entry alert\non the close", size=14, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    d.oval(s, 4.40, 2.74, 0.22, 0.22, BLUE)
    d.text(s, 2.55, 3.30, 3.3, 0.70, "Watch alert\n1% to 2% before", size=14, color=BLUE, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 1.15, 2.15, 2.2, 0.32, "You are here", size=13, color=DIM, ml=0, mr=0, mt=0, mb=0)
    block(
        d, s, ML, 4.48, 6.15, 2.32, "Watch means look",
        "You do not buy it.\nYou open the chart.\nThe entry alert is the\n4h or daily close,\nin the direction of\nthe playbook.",
        accent=BLUE, ts=16, bs=15,
    )
    block(
        d, s, 6.76, 4.48, 6.15, 2.32, "This 1-2% is distance",
        "It is distance on the chart,\nnot a risk percent.\nOn a wide book it sits\nin front of the wall.\nOctober 16 box: 2%\nwas the whole range.",
        accent=AMBER, ts=16, bs=15,
    )


def slide_bands(d: Deck) -> None:
    s = d.chrome("Entries", "The zone is a band. Stay quiet inside it")
    d.panel(s, ML, 1.18, 6.15, 3.35)
    d.text(s, 0.64, 1.36, 5.6, 0.34, "A hairline gets wicked", size=16, bold=True, color=CORAL, ml=0, mr=0, mt=0, mb=0)
    d.hline(s, 1.4, 2.55, 4.4, CORAL, 0.02)
    d.candle(s, 3.4, 1.90, 3.55, 2.85, 3.15, DIM)
    d.text(s, 0.70, 3.35, 5.5, 0.85, "One tick through the strike looks\nlike a break. The close decides.", size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.panel(s, 6.76, 1.18, 6.15, 3.35)
    d.text(s, 7.00, 1.36, 5.6, 0.34, "A band covers the chop", size=16, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    d.rect(s, 8.15, 2.15, 2.6, 0.85, TEAL_DIM, line=TEAL, line_w=1.25)
    d.candle(s, 9.35, 2.25, 2.90, 2.40, 2.70, TEAL)
    d.text(s, 7.00, 3.20, 5.6, 1.05, "Inside the band: no entry,\nand no stop-out on a wick.", size=15, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.panel(s, ML, 4.70, CONTENT_W, 2.05, accent=AMBER)
    d.text(
        s, ML + 0.24, 4.88, CONTENT_W - 0.48, 1.70,
        "The watch alert is the tap on the shoulder, 1% to 2% before you reach the band.\nThe band is where you stay quiet. Draw it wide enough to cover a wick around the strike.\nIf you need a width, use the chop already on the 4h at that strike. Do not use a one-tick line.\nOn October 16 the walls were about 2% apart, so a 2% watch of one wall sat near the other wall.",
        size=15, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_confirm(d: Deck) -> None:
    s = d.chrome("Entries", "One close, then the other checks")
    block(
        d, s, ML, 1.18, 6.15, 2.45, "Strong 4h close",
        "The candle finishes clearly\nthrough the band. The body\nis on the break side.\n\nThat can be the entry, if\nthe other checks agree.",
        accent=TEAL, ts=18, bs=16,
    )
    block(
        d, s, 6.76, 1.18, 6.15, 2.45, "15m break",
        "Use it to time the entry\nonce the 4h idea is set.\n\nA 15m break against the\n4h plan is not a trade.\nThe 4h decides the idea.",
        accent=BLUE, ts=18, bs=16,
    )
    d.text(s, ML, 3.78, CONTENT_W, 0.36, "Convergence. These should lean the same way.", size=16, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    chips = [
        (ML, "Price action"),
        (2.85, "20 / 50 / 200"),
        (5.35, "Gamma level"),
        (8.05, "News"),
        (10.15, "Flow"),
    ]
    for x, label in chips:
        d.chip(s, x, 4.25, 2.15 if label != "20 / 50 / 200" else 2.30, 0.42, label, NEST, TEXT, size=14)
    d.panel(s, ML, 4.90, CONTENT_W, 1.85, accent=AMBER)
    d.text(
        s, ML + 0.24, 5.08, CONTENT_W - 0.48, 1.50,
        "Check all five. If one of them fights the trade, wait.\nQuiet news is fine. News that fights the trade is not.\nMissing flow is not a yes. If you have no read, say so.\nDo not pretend a blank is a yes.",
        size=15, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_mas(d: Deck) -> None:
    s = d.chrome("Averages", "The 20, the 50, and the 200")
    d.panel(s, ML, 1.18, 7.55, 5.55)
    d.stamp(s, 0.58, 1.34, "ILLUSTRATIVE")
    d.text(s, 0.62, 1.74, 6.8, 0.36, "Not a real ticker. Three averages, and one wall.", size=14, color=DIM, ml=0, mr=0, mt=0, mb=0)
    # three gently separated horizontal lines
    d.hline(s, 0.85, 2.55, 6.3, "6E7C90", 0.02)
    d.text(s, 0.90, 2.20, 1.3, 0.28, "200", size=14, bold=True, color="A8B3C2", ml=0, mr=0, mt=0, mb=0)
    d.hline(s, 0.85, 3.55, 6.3, BLUE, 0.025)
    d.text(s, 0.90, 3.20, 1.3, 0.28, "50", size=14, bold=True, color=BLUE, ml=0, mr=0, mt=0, mb=0)
    d.hline(s, 0.85, 4.55, 6.3, TEAL, 0.028)
    d.text(s, 0.90, 4.20, 1.3, 0.28, "20", size=14, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    d.hline(s, 0.85, 4.55, 6.3, CYAN, 0.012)
    d.text(s, 4.4, 4.70, 2.6, 0.40, "Wall on the 20", size=14, bold=True, color=CYAN, ml=0, mr=0, mt=0, mb=0)
    d.oval(s, 4.05, 4.46, 0.20, 0.20, CYAN)
    block(
        d, s, 8.15, 1.18, 4.76, 5.55, "What each one is",
        "200: the tide. On the\n4h it is the larger swing.\n\n50: the swing itself.\n\n20: the short push.\n\nSame three on the 15m,\nfor the entry only.\n\nBest lineup: the wall and\none average in the same\nplace, and the close agrees.\n\nAn average is not a wall.\nA wall is not an average.",
        accent=BLUE, ts=16, bs=15,
    )


def slide_side(d: Deck) -> None:
    s = d.chrome("Contract", "Call side or put side")
    block(
        d, s, ML, 1.18, 6.15, 5.55, "Call side",
        "Upside break.\n\nOr a fade of the put wall,\nin positive gamma.\n\nLong call.\nOr a call debit spread.\n\nYou are long premium.",
        accent=TEAL, ts=22, bs=20,
    )
    block(
        d, s, 6.76, 1.18, 6.15, 5.55, "Put side",
        "Downside break.\n\nOr a fade of the call wall,\nin positive gamma.\n\nLong put.\nOr a put debit spread.\n\nYou are never the\nnaked short.",
        accent=CORAL, ts=22, bs=20,
    )


def slide_fork(d: Deck) -> None:
    s = d.chrome("Contract", "Single contract, or a debit spread")
    d.panel(s, ML, 1.18, 4.00, 5.55, accent=AMBER)
    d.text(s, 0.64, 1.42, 3.6, 1.15, "Ask three\nthings", size=26, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.64, 2.85, 3.6, 3.3, "How fast is\nthe move?\n\nIs IV cheap\nor rich?\n\nCan you\nwatch it?", size=18, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.arrow(s, 4.55, 3.55, 0.40, 0.32, TEAL, "right")
    block(
        d, s, 5.15, 1.18, 7.76, 2.55, "Single long call or put",
        "Fast or large move. IV is cheap. You can manage the trade.\nRisk is the premium. The working exit is a candle close.",
        accent=TEAL, ts=20, bs=16,
    )
    block(
        d, s, 5.15, 3.95, 7.76, 2.78, "Debit spread",
        "Slower move. IV is rich. Or you cannot watch it.\nYou pay a smaller debit. You cap the gain at the short strike.\nThe short leg is covered by the long leg. Not a naked short.",
        accent=BLUE, ts=20, bs=16,
    )


def slide_single(d: Deck) -> None:
    s = d.chrome("Contract", "When the single contract fits")
    points = [
        (TEAL, "Fast or large", "You need the option to keep paying if price runs past a wall."),
        (BLUE, "IV is cheap", "You are not paying a rich premium for a move that may be slow."),
        (AMBER, "You can manage it", "You can take the candle-close exit. If you cannot watch, use the spread."),
    ]
    for i, (accent, title, body) in enumerate(points):
        y = 1.18 + i * 1.45
        d.panel(s, ML, y, CONTENT_W, 1.32, accent=accent)
        d.text(s, ML + 0.22, y + 0.14, 3.3, 1.00, title, size=18, bold=True, color=accent, anchor="middle", ml=0, mr=0, mt=0, mb=0)
        d.text(s, ML + 3.6, y + 0.22, 8.5, 0.90, body, size=16, color=BODY, anchor="middle", ml=0, mr=0, mt=0, mb=0)
    d.panel(s, ML, 5.55, CONTENT_W, 1.22, accent=CORAL)
    d.text(
        s, ML + 0.24, 5.70, CONTENT_W - 0.48, 0.95,
        "Hard risk is the premium. You cannot lose more than you paid.\nIf the candle-close stop hits first, the loss is whatever the option is worth then, up to that premium.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_spread(d: Deck) -> None:
    s = d.chrome("Contract", "When the debit spread fits")
    d.panel(s, ML, 1.18, 7.7, 5.55, accent=BLUE)
    d.text(s, 0.66, 1.38, 7.3, 0.70, "Same expiry. The short strike\nis further out, and covered.", size=18, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    # two legs diagram
    d.rect(s, 0.75, 2.30, 3.15, 1.15, TEAL_DIM, line=TEAL, line_w=1.25)
    d.text(s, 0.85, 2.42, 2.95, 0.90, "Buy the nearer\nstrike. You are long.", size=15, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    d.arrow(s, 4.05, 2.68, 0.45, 0.30, BLUE, "right")
    d.rect(s, 4.65, 2.30, 3.15, 1.15, BLUE_DIM, line=BLUE, line_w=1.25)
    d.text(s, 4.75, 2.42, 2.95, 0.90, "Sell the further\nstrike. Covered.", size=15, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    d.text(
        s, 0.70, 3.70, 7.1, 2.70,
        "Call spread: buy a call, sell a\nfurther call.\n\nPut spread: buy a put, sell a\nfurther put.\n\nMax loss is the debit.\nPast the short strike, you\ndo not get paid more.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )
    block(
        d, s, 8.30, 1.18, 4.61, 5.55, "Use it when",
        "The move is slower.\n\nIV is rich.\n\nOr you cannot watch.\n\nOne caution. These are\nAmerican options. The\nshort leg can be assigned\nearly. Know the broker\nrule before you hold a\nspread into expiry.",
        accent=AMBER, ts=18, bs=16,
    )


def slide_payoff(d: Deck) -> None:
    s = d.chrome("Example", "Payoff at expiry, single versus spread")
    d.picture(s, d.charts["payoff"], 0.35, 1.15, 7.35)
    call = money(FACTS["call_25"])
    spr = money(FACTS["spread_25"])
    gain = money(FACTS["max_gain_25"])
    block(
        d, s, 7.85, 1.20, 5.06, 4.55, "The example debits",
        f"21 days. IV 25%.\nSpot 100. Rate 4%.\nNo dividend.\n\nLong 100 call: {call}\n100/105 spread: {spr}\n\nSpread max gain:\n{gain} per share.\nAbout {float(gain)*100:.0f} dollars\na contract.",
        accent=TEAL, ts=16, bs=15,
    )
    d.text(
        s, ML, 6.55, CONTENT_W, 0.45,
        "EXAMPLE. Black-Scholes prices, then the expiry payoff of those debits. Per share. A contract is times 100. Not a forecast.",
        size=13, color=DIM, ml=0, mr=0, mt=0, mb=0,
    )


def slide_rich_iv(d: Deck) -> None:
    s = d.chrome("Example", "What rich IV does to the price")
    d.text(
        s, ML, 1.14, CONTENT_W, 0.40,
        "EXAMPLE. Same 21-day 100/105 call spread. Spot 100. Rate 4%. No dividend. Only IV changes.",
        size=14, color=DIM, ml=0, mr=0, mt=0, mb=0,
    )
    low = FACTS["rich"][0.18]
    high = FACTS["rich"][0.40]
    cols_iv = [
        ("IV 18%", low, TEAL),
        ("IV 40%", high, CORAL),
    ]
    # header row labels
    labels = [("ATM call", "call"), ("Spread debit", "spread"), ("Spread max gain", "max_gain")]
    d.text(s, ML, 1.70, 3.1, 0.40, "", size=14, color=DIM, ml=0, mr=0, mt=0, mb=0)
    for i, (name, key) in enumerate(labels):
        y = 2.25 + i * 1.35
        d.text(s, ML, y, 3.3, 1.05, name, size=18, bold=True, color=TEXT, anchor="middle", ml=0, mr=0, mt=0, mb=0)
        for j, (title, data, accent) in enumerate(cols_iv):
            x = 3.9 + j * 4.45
            if i == 0:
                d.text(s, x, 1.65, 4.1, 0.36, title, size=16, bold=True, color=accent, ml=0, mr=0, mt=0, mb=0)
            d.panel(s, x, y, 4.15, 1.15, accent=accent)
            d.text(s, x + 0.2, y, 3.75, 1.15, money(data[key]), size=28, bold=True, color=TEXT, anchor="middle", ml=0, mr=0, mt=0, mb=0)
    d.text(
        s, ML, 6.40, CONTENT_W, 0.60,
        "The single call more than doubles. The spread debit rises less. Rich IV is why the spread is the fit when the move is not a fast one you must keep open.",
        size=15, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_place(d: Deck) -> None:
    s = d.chrome("Contract", "Place the contract on the map")
    d.panel(s, ML, 1.18, CONTENT_W, 0.85, accent=AMBER)
    d.text(
        s, ML + 0.22, 1.32, CONTENT_W - 0.44, 0.58,
        "A picture of the October 16 book. Not an order. You still check IV, and you still write your own dollars.",
        size=16, color=TEXT, anchor="middle", ml=0, mr=0, mt=0, mb=0,
    )
    block(
        d, s, ML, 2.20, 6.15, 4.50, "Put side, through 760",
        "Fast, IV cheap, you can watch:\nlong put.\n\nSlow, IV rich, or you cannot\nwatch: put debit spread.\n\nLong strike near the money,\nor near the level that has to\nwork. Short strike further\nout, at a target you can name.",
        accent=CORAL, ts=18, bs=16,
    )
    block(
        d, s, 6.76, 2.20, 6.15, 4.50, "Call side, through 775",
        "That close also crosses\nthe flip. Re-read first.\n\nIf the new book is a long\ncall idea: same fork.\nSingle if it is fast and you\ncan watch. Spread if IV is\nrich or you cannot.\n\nDo not sell a strike the long\nleg does not cover.",
        accent=TEAL, ts=18, bs=16,
    )


def slide_delta_bands(d: Deck) -> None:
    s = d.chrome("Delta", "High delta, mid delta, low delta")
    d.picture(s, d.charts["delta"], 0.30, 1.10, 7.15)
    bands = FACTS["bands"]
    # bands order is 106, 100, 95. Present high, mid, low by strike descending delta.
    ordered = sorted(bands, key=lambda b: -b["delta"])
    names = ["High", "Mid", "Low"]
    gloss = [
        "Costs more. Moves like the stock.",
        "0.40 to 0.60. Reacts fast.",
        "Cheap. Needs a big move. Often expires worthless.",
    ]
    for i, (band, name, line) in enumerate(zip(ordered, names, gloss)):
        y = 1.18 + i * 1.75
        d.panel(s, 7.55, y, 5.35, 1.62)
        d.text(
            s, 7.73, y + 0.10, 5.05, 0.36,
            f"{name}    {band['delta']:.2f}    strike {band['k']:.0f}",
            size=15, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0,
        )
        d.text(
            s, 7.73, y + 0.50, 5.05, 0.95,
            f"{line}\nAbout {band['price']:.2f} a share. About {band['shares']:.0f} shares of exposure.",
            size=14, color=BODY, ml=0, mr=0, mt=0, mb=0,
        )
    d.text(
        s, ML, 6.62, CONTENT_W, 0.40,
        "EXAMPLE. 21 days, IV 25%, spot 100, rate 4%, no dividend. Exposure is delta times 100 shares, on a small move. You do not buy the shares.",
        size=12, color=DIM, ml=0, mr=0, mt=0, mb=0,
    )


def slide_itm(d: Deck) -> None:
    s = d.chrome("Delta", "Delta, ignoring the sign")
    d.panel(s, ML, 1.18, CONTENT_W, 1.35, accent=AMBER)
    d.text(
        s, ML + 0.24, 1.36, CONTENT_W - 0.48, 1.00,
        "Delta (ignoring the sign) is roughly the chance the option finishes in the money.",
        size=22, bold=True, color=TEXT, anchor="middle", ml=0, mr=0, mt=0, mb=0,
    )
    d.panel(s, ML, 2.72, 6.15, 2.35, accent=TEAL)
    d.text(s, 0.66, 2.90, 5.7, 0.40, "Call delta +0.45", size=20, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.66, 3.45, 5.7, 1.20, "Ignore the plus.\nRead it as about a 45 percent chance.", size=18, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.panel(s, 6.76, 2.72, 6.15, 2.35, accent=CORAL)
    d.text(s, 7.00, 2.90, 5.7, 0.40, "Put delta -0.45", size=20, bold=True, color=CORAL, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 7.00, 3.45, 5.7, 1.20, "Ignore the minus.\nSame read. About 45 percent.", size=18, color=BODY, ml=0, mr=0, mt=0, mb=0)
    d.panel(s, ML, 5.25, CONTENT_W, 1.52, accent=BLUE)
    d.text(
        s, ML + 0.24, 5.42, CONTENT_W - 0.48, 1.20,
        "Rough guide. Closer on short-dated options.\nIn the model, the chance of finishing in the money is a nearby number, not this one.\nUse it to plan. Do not treat it as exact.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_theta(d: Deck) -> None:
    s = d.chrome("Theta", "Theta is decay")
    d.picture(s, d.charts["decay"], 0.30, 1.12, 7.45)
    start = FACTS["decay"][0]
    end = FACTS["decay"][-1]
    block(
        d, s, 7.90, 1.18, 5.00, 5.15, "What the curves say",
        f"Spot held at 100.\nIV 25%. EXAMPLE.\n\nSingle call, 45 days\nto 1 day: {money(start[1])}\nto {money(end[1])}.\n\n100/105 spread:\n{money(start[2])} to\n{money(end[2])}.\n\nThe single gives up\nmore dollars. The curve\nsteepens into expiry.\n\nWith a day left, the 105\ncall is nearly worthless,\nso the two meet.",
        accent=BLUE, ts=16, bs=14,
    )
    d.text(
        s, ML, 6.62, 7.5, 0.40,
        "You pay theta every day you are long. Less decay is not a reason to hold a wrong idea.",
        size=13, color=DIM, ml=0, mr=0, mt=0, mb=0,
    )


def slide_crush(d: Deck) -> None:
    s = d.chrome("IV", "IV crush is a fast drop in IV")
    d.picture(s, d.charts["crush"], 0.40, 1.20, 7.15)
    a = money(FACTS["crush_start"])
    b = money(FACTS["crush_flat"])
    c = money(FACTS["crush_up"])
    block(
        d, s, 7.75, 1.20, 5.15, 5.15, "The three bars",
        f"14-day ATM call.\nEXAMPLE.\n\nStart, IV 50%:\n{a}\n\nSpot stays 100,\nIV falls to 25%:\n{b}\n\nSpot rises to 102,\nIV falls to 25%:\n{c}\n\nThe stock rose.\nThe call still fell.",
        accent=CORAL, ts=16, bs=15,
    )
    d.text(
        s, ML, 6.55, CONTENT_W, 0.48,
        "Often after an event. The option can lose value even if the stock stays flat, or rises. Black-Scholes, rate 4%, no dividend.",
        size=13, color=DIM, ml=0, mr=0, mt=0, mb=0,
    )


def slide_events(d: Deck) -> None:
    s = d.chrome("Events", "Earnings, and the rare 0DTE")
    block(
        d, s, ML, 1.18, 6.15, 5.55, "Earnings",
        "IV is commonly bid up\ninto the report, then it\ndrops. That drop is crush.\n\nCheck the actual IV.\nDo not assume it.\n\nRich IV, or you cannot\nwatch: debit spread.\n\nCheap IV, a fast move,\nand you can watch:\nsingle contract.",
        accent=AMBER, ts=22, bs=18,
    )
    block(
        d, s, 6.76, 1.18, 6.15, 5.55, "0DTE",
        "This is the 1-day spike\non the gamma chart.\n\nTheta is gone by the close.\n\nOccasional, and only when\nyou can manage that close.\n\nSame playbook. Same\ncandle close. Same cash\ndebit. No naked short.\n\nDo not use the 0DTE\ncolumn as the swing map.",
        accent=CORAL, ts=22, bs=18,
    )


def slide_stops(d: Deck) -> None:
    s = d.chrome("Risk", "The stop follows the regime")
    block(
        d, s, ML, 1.18, 6.15, 3.15, "Positive gamma fade",
        "The stop sits beyond the\nrejection high, or the low.\n\nYou exit when a candle\ncloses through that price.\nA wick through it is not\nthe exit.",
        accent=TEAL, ts=18, bs=16,
    )
    block(
        d, s, 6.76, 1.18, 6.15, 3.15, "Negative gamma break",
        "You exit when a 4h candle\ncloses back inside the range.\n\nThe break failed.\nA wick back inside is not\nthe exit. The close is.",
        accent=CORAL, ts=18, bs=16,
    )
    d.panel(s, ML, 4.52, CONTENT_W, 2.22, accent=AMBER)
    d.text(
        s, ML + 0.24, 4.70, CONTENT_W - 0.48, 1.88,
        "Both regimes: the hard ceiling on the loss is the debit you paid.\nThe candle close is how you leave when the idea is wrong, before the option is worth zero.\nDo not move the stop farther once that close has already killed the idea.\nPick the stop before you enter. Write it down. Do not switch it after you are in.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_risk(d: Deck) -> None:
    s = d.chrome("Risk", "You choose the dollars")
    d.panel(s, ML, 1.18, CONTENT_W, 1.55, accent=AMBER)
    d.text(
        s, ML + 0.24, 1.36, CONTENT_W - 0.48, 1.20,
        "Every trade, you write the dollars you are willing to lose.\nThis deck will not give you a percent of the account. It will not give you a dollar amount.",
        size=18, color=TEXT, ml=0, mr=0, mt=0, mb=0,
    )
    d.panel(s, ML, 2.90, 7.7, 2.55, accent=BLUE)
    d.text(s, 0.66, 3.08, 7.3, 0.40, "The only math", size=16, bold=True, color=BLUE, ml=0, mr=0, mt=0, mb=0)
    d.text(
        s, 0.66, 3.55, 7.3, 1.60,
        "Your dollars\n  /  (option price  x  100)\n  =  contracts",
        size=22, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0,
    )
    block(
        d, s, 8.30, 2.90, 4.61, 2.55, "EXAMPLE arithmetic",
        "You wrote 400.\nDebit is 2.00.\n2.00 x 100 = 200.\n400 / 200 = 2 contracts.\nReplace 400. It is not\na suggestion.",
        accent=AMBER, ts=16, bs=15,
    )
    d.text(
        s, ML, 5.60, CONTENT_W, 1.20,
        "At a stop before expiry the option may still have value. It may not, if the move was violent or time is gone.\nBe willing to lose the debit. In negative gamma the invalidation can sit back at the other side of the range.\nMeasure that room, then do the division. The same dollars buy fewer contracts when the debit is large.",
        size=15, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_flow(d: Deck) -> None:
    s = d.chrome("Flow", "Flow, dark pool, and the dollars")
    block(
        d, s, ML, 1.18, 4.05, 3.55, "Options flow",
        "Large prints at a wall\ncarry more weight than\nprints in the middle.\n\nWeight. Not the entry.\nThe close is the entry.",
        accent=PURPLE, ts=18, bs=16,
    )
    block(
        d, s, 4.65, 1.18, 4.05, 3.55, "Dark pool",
        "Large stock prints near\na wall add weight to\nthat wall.\n\nSame rule.\nWeight, not a trigger.",
        accent=BLUE, ts=18, bs=16,
    )
    block(
        d, s, 9.12, 1.18, 3.79, 3.55, "Not a close",
        "A print does not\nreplace the 4h close,\nthe regime, or the\nwall you already\nmarked.",
        accent=AMBER, ts=18, bs=16,
    )
    d.panel(s, ML, 4.90, CONTENT_W, 1.85, accent=TEAL)
    d.text(s, ML + 0.22, 5.05, CONTENT_W - 0.44, 0.36, "Always the dollar premium. Price x contracts x 100.", size=16, bold=True, color=TEXT, ml=0, mr=0, mt=0, mb=0)
    d.text(
        s, ML + 0.22, 5.48, CONTENT_W - 0.44, 1.05,
        "EXAMPLE.  2.00 x 500 x 100 = 100,000 dollars.    12.00 x 80 x 100 = 96,000 dollars.\nSimilar money. Very different if you only count contracts. Read the dollars.",
        size=16, color=BODY, ml=0, mr=0, mt=0, mb=0,
    )


def slide_run16(d: Deck) -> None:
    s = d.chrome("October 16, 2026", "Run that book through the list")
    rows = [
        ("Month", "Not in this example. You still write your dollars. Do not skip the step."),
        ("Levels", "Put wall 760. Call wall 775. Flip about 774.5. Spot about 763.2."),
        ("Regime", "Negative. Spot is under the flip. Do not fade the box."),
        ("4h", "The range was 760 to 775. It matched the walls."),
        ("Plan", "Wait. Close through 760: go with the put. Hold above 775: re-read."),
        ("Contract", "Fast and cheap IV and you can watch: single. Else a debit spread. Check IV. It is not given here."),
        ("Stop", "A 4h close back inside. Hard risk is the debit. Flow is weight, in dollars, at the walls."),
    ]
    for i, (label, line) in enumerate(rows):
        y = 1.16 + i * 0.78
        d.panel(s, ML, y, CONTENT_W, 0.70)
        d.rect(s, ML, y, 1.55, 0.70, NEST)
        d.text(s, ML, y, 1.55, 0.70, label, size=14, bold=True, color=AMBER, align="center", anchor="middle", ml=0.04, mr=0.04, mt=0, mb=0)
        d.text(s, ML + 1.72, y, CONTENT_W - 1.9, 0.70, line, size=14, color=TEXT, anchor="middle", ml=0.08, mr=0.08, mt=0, mb=0)


def slide_check(d: Deck) -> None:
    s = d.chrome("Checklist", "Before you enter")
    groups = [
        ("Regime", [
            "Month noted. Your dollars are written down.",
            "Flip marked. You know which side spot is on.",
            "Positive: fade only. Negative: break only.",
        ]),
        ("Levels", [
            "Put wall and call wall, from open interest.",
            "Cross-checked on a second public source.",
            "4h range drawn. You know if it matches.",
        ]),
        ("Trigger", [
            "Watch is 1-2% out. Distance, not risk.",
            "Entry alert is a 4h or daily close.",
            "The zone is a band. You are not inside it.",
            "15m break, or a strong 4h close.",
            "Price, averages, level, news, flow agree.",
        ]),
        ("Contract", [
            "Single or spread: speed, IV, and attention.",
            "Contracts = your dollars / the debit.",
            "Stop is a candle close. You can say where.",
            "Cash debit only. No naked short.",
        ]),
    ]
    for i, (title, items) in enumerate(groups):
        col = i % 2
        row = i // 2
        x = ML + col * 6.34
        y = 1.16 + row * 2.85
        d.panel(s, x, y, 6.16, 2.72, accent=TEAL)
        d.text(s, x + 0.18, y + 0.10, 5.8, 0.34, title, size=16, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
        for j, line in enumerate(items):
            yy = y + 0.50 + j * 0.40
            d.rect(s, x + 0.20, yy + 0.06, 0.16, 0.16, None, line=TEAL, line_w=1.25)
            d.text(s, x + 0.46, yy, 5.5, 0.36, line, size=13, color=BODY, anchor="middle", ml=0, mr=0, mt=0, mb=0)


def slide_mistakes(d: Deck) -> None:
    s = d.chrome("Mistakes", "Easy ways to get this wrong")
    items = [
        "Treating the flip as support.",
        "Fading a wall while spot is under the flip.",
        "Buying a breakout while spot is over the flip.",
        "Entering on a touch, or on a wick.",
        "Reading the heatmap as put gamma.",
        "Looking for a put-wall line on the by-strike chart.",
        "Looking for a flip line on the by-strike chart.",
        "Setting a swing level from Directionalized Volume.",
        "Counting contracts and skipping the dollars.",
        "Chasing a poke that closed back inside.",
        "Keeping the old plan after a close outside has held.",
        "Selling options naked, or using margin.",
        "Letting a 15m break overrule the 4h.",
        "Copying the dealer by shorting stock.",
    ]
    for i, line in enumerate(items):
        col = i // 7
        row = i % 7
        x = ML + col * 6.34
        y = 1.18 + row * 0.78
        d.panel(s, x, y, 6.16, 0.68)
        d.rect(s, x, y, 0.62, 0.68, NEST)
        d.text(s, x, y, 0.62, 0.68, f"{i+1:02d}", size=14, bold=True, color=CORAL, align="center", anchor="middle", ml=0, mr=0, mt=0, mb=0)
        d.text(s, x + 0.74, y, 5.25, 0.68, line, size=14, color=TEXT, anchor="middle", ml=0.06, mr=0.08, mt=0, mb=0)


def slide_gloss_a(d: Deck) -> None:
    s = d.chrome("Glossary", "The words")
    terms = [
        ("Delta", "Share count for the dealer. For you, how the option tracks the stock."),
        ("Gamma", "How fast delta changes as the stock price moves."),
        ("Theta", "Decay. The value time takes out of a long option."),
        ("Vega", "How much the option price changes when IV changes."),
        ("IV", "The volatility implied by the option's price."),
        ("IV crush", "A fast drop in IV, often after an event. The option can lose value anyway."),
        ("Charm", "Delta's change as time passes. Price and IV held still. Textbook only."),
        ("Vanna", "Delta's change as IV changes. Price held still. Textbook only."),
    ]
    for i, (term, line) in enumerate(terms):
        y = 1.16 + i * 0.70
        d.rect(s, ML, y, 2.15, 0.62, NEST)
        d.text(s, ML, y, 2.15, 0.62, term, size=15, bold=True, color=AMBER, align="center", anchor="middle", ml=0.06, mr=0.06, mt=0, mb=0)
        d.text(s, ML + 2.35, y, 10.0, 0.62, line, size=16, color=BODY, anchor="middle", ml=0.08, mr=0.08, mt=0, mb=0)


def slide_gloss_b(d: Deck) -> None:
    s = d.chrome("Glossary", "The levels and the orders")
    terms = [
        ("Call wall", "Heavy call open interest above spot. Resistance."),
        ("Put wall", "Heavy put open interest below spot. Support. Longest purple bar under spot."),
        ("Flip", "Where net gamma changes sign. A behavior change. Not support."),
        ("Positive gamma", "Above the flip. Dealers fade the move. Price can range and pin."),
        ("Negative gamma", "Below the flip. Dealers chase. Price can trend and accelerate."),
        ("Open interest", "Contracts still open. The swing book. Walls and regime."),
        ("Directionalized Volume", "Today's flow. The intraday view. Not the swing map."),
        ("Pin", "Price sticking near a heavy strike while the hedges lean back in."),
        ("OPEX", "Expiration. A large expiry resets the walls. Read the book again."),
        ("Debit spread", "Long one option, short a further strike, same expiry. Max loss is the debit."),
        ("Premium", "The price you pay. The hard risk on a long call, long put, or debit spread."),
        ("0DTE", "Expires the same day. Extreme gamma. Extreme theta. Occasional only."),
        ("Candle close", "The bar has finished. The only alert that counts in this deck."),
    ]
    for i, (term, line) in enumerate(terms):
        col = 0 if i < 7 else 1
        row = i if i < 7 else i - 7
        x = ML + col * 6.30
        y = 1.14 + row * 0.78
        d.rect(s, x, y, 6.14, 0.70, CARD, line=LINE, line_w=1.0)
        d.text(s, x + 0.12, y + 0.04, 5.9, 0.28, term, size=13, bold=True, color=AMBER, ml=0, mr=0, mt=0, mb=0)
        d.text(s, x + 0.12, y + 0.32, 5.9, 0.34, line, size=12, color=BODY, ml=0, mr=0, mt=0, mb=0)


def slide_one(d: Deck) -> None:
    s = d.chrome("Wrap-up", "The whole swing on one page")
    left = [
        "1  Note the month. Write your dollars.",
        "2  Mark put wall, call wall, flip, spot.",
        "3  Cross-check the three levels.",
        "4  Draw the 4h range on the walls.",
        "5  Above the flip: fade a rejection close.",
        "6  Below the flip: trade the 4h break.",
        "7  Fast, cheap IV, you can watch: single.",
        "8  Otherwise: a debit spread.",
        "9  Stop on a candle close. Risk is the debit.",
    ]
    right = [
        "Flip: behavior change. Not support.",
        "Walls: call resistance, put support.",
        "Heatmap color: net gamma.",
        "Put wall: longest purple bar below spot.",
        "By-strike draws call wall and spot only.",
        "Open interest: swing. Volume: today.",
        "Alert on the close. Never a touch.",
        "1-2% watch is distance, not risk.",
        "Inside the band, stay quiet.",
        "15m times the entry. 4h decides.",
        "Cash only. No naked short.",
    ]
    d.panel(s, ML, 1.14, 6.15, 5.20, accent=TEAL)
    d.text(s, 0.62, 1.26, 5.7, 0.34, "Do it in this order", size=16, bold=True, color=TEAL, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 0.62, 1.68, 5.75, 4.45, "\n".join(left), size=15, color=BODY, ml=0, mr=0, mt=0, mb=0, spacing=1.18)
    d.panel(s, 6.76, 1.14, 6.15, 5.20, accent=AMBER)
    d.text(s, 6.96, 1.26, 5.7, 0.34, "Keep these straight", size=16, bold=True, color=AMBER, ml=0, mr=0, mt=0, mb=0)
    d.text(s, 6.96, 1.68, 5.75, 4.45, "\n".join(right), size=15, color=BODY, ml=0, mr=0, mt=0, mb=0, spacing=1.15)
    d.panel(s, ML, 6.48, CONTENT_W, 0.50, accent=None)
    d.text(
        s, ML, 6.48, CONTENT_W, 0.50,
        "Dealers hedge. Gamma shows the push. You act on the close. You choose the risk.",
        size=15, bold=True, color=TEXT, align="center", anchor="middle", ml=0.1, mr=0.1, mt=0, mb=0,
    )


def finalize_package(path: Path) -> None:
    """Mark the slide size as 16:9 and embed Liberation Sans so the layout holds."""
    import zipfile
    from io import BytesIO

    regular = Path(FONT_REG).read_bytes()
    bold = Path(FONT_BOLD).read_bytes()
    buf = BytesIO()
    with zipfile.ZipFile(path, "r") as zin, zipfile.ZipFile(buf, "w") as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "ppt/presentation.xml":
                text = data.decode("utf-8")
                text = text.replace('saveSubsetFonts="1"', 'embedTrueTypeFonts="1" saveSubsetFonts="0"', 1)
                text = text.replace('type="screen4x3"', 'type="screen16x9"', 1)
                font_xml = (
                    '<p:embeddedFontLst><p:embeddedFont>'
                    '<p:font typeface="Liberation Sans" pitchFamily="34" charset="0"/>'
                    '<p:regular r:id="rId71"/>'
                    '<p:bold r:id="rId72"/>'
                    "</p:embeddedFont></p:embeddedFontLst>"
                )
                text = text.replace("<p:defaultTextStyle>", font_xml + "<p:defaultTextStyle>", 1)
                data = text.encode("utf-8")
            elif item.filename == "ppt/_rels/presentation.xml.rels":
                text = data.decode("utf-8")
                extra = (
                    '<Relationship Id="rId71" '
                    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" '
                    'Target="fonts/font1.fntdata"/>'
                    '<Relationship Id="rId72" '
                    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" '
                    'Target="fonts/font2.fntdata"/>'
                )
                text = text.replace("</Relationships>", extra + "</Relationships>", 1)
                data = text.encode("utf-8")
            elif item.filename == "[Content_Types].xml":
                text = data.decode("utf-8")
                if "fntdata" not in text:
                    text = text.replace(
                        "<Types ",
                        '<Types ',
                    )
                    text = text.replace(
                        "</Types>",
                        '<Default Extension="fntdata" ContentType="application/x-fontdata"/></Types>',
                        1,
                    )
                data = text.encode("utf-8")
            zout.writestr(item, data)
        zout.writestr("ppt/fonts/font1.fntdata", regular)
        zout.writestr("ppt/fonts/font2.fntdata", bold)
    path.write_bytes(buf.getvalue())


def render_previews(pptx_path: Path) -> None:
    out = ROOT / "previews"
    out.mkdir(parents=True, exist_ok=True)
    work = Path("/tmp/gamma-preview")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    profile = Path("/tmp/lo-profile")
    profile.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [
            "soffice",
            "-env:UserInstallation=file:///tmp/lo-profile",
            "--headless",
            "--nolockcheck",
            "--nologo",
            "--nofirststartwizard",
            "--convert-to",
            "pdf",
            "--outdir",
            str(work),
            str(pptx_path),
        ]
    )
    pdf = work / "gamma_swing.pdf"
    subprocess.check_call(["pdftoppm", "-png", "-r", "130", str(pdf), str(work / "slide")])
    pngs = sorted(work.glob("slide-*.png"), key=lambda p: int(p.stem.split("-")[1]))
    for old in out.glob("slide_*.png"):
        old.unlink()
    for i, src in enumerate(pngs, start=1):
        shutil.copy(src, out / f"slide_{i:02d}.png")
    print(f"previews {len(pngs)} -> {out}")


def build() -> Deck:
    charts = build_charts()
    d = Deck()
    d.charts = charts
    slide_cover(d)
    slide_map(d)
    slide_tools(d)
    slide_core(d)
    slide_dealers(d)
    slide_delta(d)
    slide_gamma_def(d)
    slide_gamma_chart(d)
    slide_hedge_chart(d)
    slide_regimes(d)
    slide_positive(d)
    slide_negative(d)
    slide_hedge_sign(d)
    slide_flip(d)
    slide_flip_quiet(d)
    slide_flip_close(d)
    slide_walls(d)
    slide_walls_regime(d)
    slide_opex(d)
    slide_charm(d)
    slide_uw_rules(d)
    slide_heatmap(d)
    slide_bystrike(d)
    slide_oi_volume(d)
    slide_crosscheck(d)
    slide_month(d)
    slide_clocks(d)
    slide_align(d)
    slide_disagree(d)
    slide_spy_numbers(d)
    slide_spy_box(d)
    slide_spy_plan(d)
    slide_pos_play(d)
    slide_pos_candle(d)
    slide_neg_play(d)
    slide_neg_candle(d)
    slide_poke(d)
    slide_rebuild(d)
    slide_alerts(d)
    slide_watch(d)
    slide_bands(d)
    slide_confirm(d)
    slide_mas(d)
    slide_side(d)
    slide_fork(d)
    slide_single(d)
    slide_spread(d)
    slide_payoff(d)
    slide_rich_iv(d)
    slide_place(d)
    slide_delta_bands(d)
    slide_itm(d)
    slide_theta(d)
    slide_crush(d)
    slide_events(d)
    slide_stops(d)
    slide_risk(d)
    slide_flow(d)
    slide_run16(d)
    slide_check(d)
    slide_mistakes(d)
    slide_gloss_a(d)
    slide_gloss_b(d)
    slide_one(d)
    out = ROOT / "gamma_swing.pptx"
    d.save(out)
    finalize_package(out)
    copy_path = Path("/tmp/gamma_copy.txt")
    with copy_path.open("w", encoding="utf-8") as handle:
        current = None
        for rec in d.records:
            if rec["slide"] != current:
                current = rec["slide"]
                title = d.titles[current - 1]
                handle.write(f"\n===== {current:02d}  {title} =====\n")
            handle.write(rec["text"].replace("\n", " / ") + "\n")
    print(f"slides {d.n}")
    for i, title in enumerate(d.titles, start=1):
        print(f"{i:02d}  {title}")
    print(f"warnings {len(d.warnings)}")
    for warning in d.warnings:
        print("WARN", warning)
    print(f"wrote {out}")
    if "--preview" in sys.argv:
        render_previews(out)
    return d


if __name__ == "__main__":
    build()
