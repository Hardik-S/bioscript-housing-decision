from __future__ import annotations

import io
from pathlib import Path

from PIL import Image, ImageEnhance
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from build_housing_packet import LISTINGS, download_images


ROOT = Path(__file__).resolve().parent
PDF_PATH = ROOT / "BioScript_Housing_Decision_Packet.pdf"
PAGE_W, PAGE_H = letter

M = 46
GAP = 20
INK = colors.HexColor("#17211c")
MUTED = colors.HexColor("#66736b")
LINE = colors.HexColor("#dce4dd")
BG = colors.HexColor("#f7f8f4")
PANEL = colors.HexColor("#ffffff")
GREEN = colors.HexColor("#286447")
BLUE = colors.HexColor("#275f8f")
AMBER = colors.HexColor("#a86921")
SOFT_GREEN = colors.HexColor("#e8f2eb")
SOFT_BLUE = colors.HexColor("#e7f0f8")
SOFT_AMBER = colors.HexColor("#f7eee1")
CHARCOAL = colors.HexColor("#10211a")


def text_width(text: str, font: str, size: float) -> float:
    return stringWidth(text, font, size)


def lines_for(text: str, font: str, size: float, width: float, max_lines: int | None = None) -> list[str]:
    words = text.replace("\n", " ").split()
    lines: list[str] = []
    current = ""
    truncated = False
    for word in words:
        test = word if not current else f"{current} {word}"
        if text_width(test, font, size) <= width:
            current = test
            continue
        if current:
            lines.append(current)
        current = word
        if max_lines and len(lines) == max_lines:
            truncated = True
            break
    if current and (not max_lines or len(lines) < max_lines):
        lines.append(current)
    if max_lines and len(lines) == max_lines and truncated:
        while lines and text_width(lines[-1] + "...", font, size) > width:
            lines[-1] = " ".join(lines[-1].split()[:-1])
        lines[-1] = lines[-1].rstrip(".,;:") + "..."
    return lines


def draw_text(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    *,
    font: str = "Helvetica",
    size: float = 10,
    leading: float = 13,
    color=INK,
    max_lines: int | None = None,
) -> float:
    c.setFont(font, size)
    c.setFillColor(color)
    for line in lines_for(text, font, size, width, max_lines):
        c.drawString(x, y, line)
        y -= leading
    return y


def panel(c: canvas.Canvas, x: float, y: float, w: float, h: float, fill=PANEL, stroke=LINE, radius: float = 10) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.roundRect(x, y, w, h, radius, stroke=1, fill=1)


def image_crop(c: canvas.Canvas, path: Path, x: float, y: float, w: float, h: float, brighten: float = 1.04) -> None:
    img = Image.open(path).convert("RGB")
    img = ImageEnhance.Brightness(img).enhance(brighten)
    iw, ih = img.size
    box_ratio = w / h
    img_ratio = iw / ih
    if img_ratio > box_ratio:
        new_w = int(ih * box_ratio)
        left = (iw - new_w) // 2
        crop = img.crop((left, 0, left + new_w, ih))
    else:
        new_h = int(iw / box_ratio)
        top = max(0, (ih - new_h) // 2)
        crop = img.crop((0, top, iw, top + new_h))
    bio = io.BytesIO()
    crop.save(bio, "JPEG", quality=90)
    bio.seek(0)
    c.drawImage(ImageReader(bio), x, y, w, h, mask="auto")


def page_base(c: canvas.Canvas, section: str, page: int, accent=GREEN) -> None:
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(accent)
    c.rect(0, PAGE_H - 8, PAGE_W, 8, stroke=0, fill=1)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M, PAGE_H - 31, section.upper())
    c.setFont("Helvetica", 8.5)
    c.drawRightString(PAGE_W - M, PAGE_H - 31, f"page {page} / 8")


def footer(c: canvas.Canvas, sources: str = "") -> None:
    c.setStrokeColor(LINE)
    c.line(M, 34, PAGE_W - M, 34)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.8)
    c.drawString(M, 21, "Prepared May 13, 2026. Re-confirm price, utilities, pet rules, and availability before applying.")
    if sources:
        c.drawRightString(PAGE_W - M, 21, sources[:78])


def title_block(c: canvas.Canvas, title: str, subtitle: str, y: float) -> float:
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 23)
    c.drawString(M, y, title)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y - 19, subtitle)
    return y - 43


def summary_band(c: canvas.Canvas, text: str, y: float, accent_fill, height: float = 70) -> float:
    panel(c, M, y - height, PAGE_W - 2 * M, height, fill=accent_fill, stroke=accent_fill, radius=9)
    draw_text(c, text, M + 18, y - 23, PAGE_W - 2 * M - 36, size=10.2, leading=13.5, max_lines=3)
    return y - height - 22


def pill(c: canvas.Canvas, text: str, x: float, y: float, fill, color=INK) -> None:
    w = min(118, text_width(text, "Helvetica-Bold", 8.2) + 17)
    c.setFillColor(fill)
    c.roundRect(x, y, w, 18, 9, stroke=0, fill=1)
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(x + 8, y + 5, text[:24])


def listing_card(c: canvas.Canvas, item, path: Path, x: float, y: float, w: float, h: float, accent=GREEN) -> None:
    panel(c, x, y, w, h, fill=PANEL, stroke=LINE, radius=10)
    pad = 14
    img_h = 170
    image_crop(c, path, x + pad, y + h - pad - img_h, w - 2 * pad, img_h)
    pill(c, item.badge, x + pad + 8, y + h - pad - 26, SOFT_GREEN if accent == GREEN else SOFT_BLUE if accent == BLUE else SOFT_AMBER)

    text_y = y + h - pad - img_h - 22
    draw_text(c, item.name, x + pad, text_y, w - 2 * pad, font="Helvetica-Bold", size=13, leading=15, max_lines=1)
    text_y -= 20
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 10.4)
    c.drawString(x + pad, text_y, item.price)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9.2)
    c.drawRightString(x + w - pad, text_y, item.per_person)
    text_y -= 17
    draw_text(c, item.area, x + pad, text_y, w - 2 * pad, size=8.8, leading=11, color=MUTED, max_lines=1)

    text_y -= 22
    c.setFont("Helvetica-Bold", 8.6)
    c.setFillColor(MUTED)
    c.drawString(x + pad, text_y, "WHY IT WORKS")
    text_y -= 14
    text_y = draw_text(c, item.fit, x + pad, text_y, w - 2 * pad, size=9.2, leading=12, max_lines=3)

    check_y = y + 20
    panel(c, x + pad, check_y, w - 2 * pad, 62, fill=SOFT_AMBER, stroke=SOFT_AMBER, radius=8)
    draw_text(c, "Confirm: " + item.risk, x + pad + 11, check_y + 43, w - 2 * pad - 22, size=8.8, leading=11, max_lines=3)


def compact_listing_card(c: canvas.Canvas, item, path: Path, x: float, y: float, w: float, h: float, accent=GREEN) -> None:
    panel(c, x, y, w, h, fill=PANEL, stroke=LINE, radius=9)
    pad = 11
    img_h = 92
    image_crop(c, path, x + pad, y + h - pad - img_h, w - 2 * pad, img_h)
    pill(c, item.badge, x + pad + 7, y + h - pad - 25, SOFT_GREEN if accent == GREEN else SOFT_BLUE if accent == BLUE else SOFT_AMBER)

    yy = y + h - pad - img_h - 17
    draw_text(c, item.name, x + pad, yy, w - 2 * pad, font="Helvetica-Bold", size=10.2, leading=12, max_lines=2)
    yy -= 28
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 9.1)
    c.drawString(x + pad, yy, item.price)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.1)
    c.drawRightString(x + w - pad, yy, item.per_person)
    yy -= 13
    draw_text(c, item.area, x + pad, yy, w - 2 * pad, size=7.8, leading=9.2, color=MUTED, max_lines=1)
    yy -= 15
    draw_text(c, item.fit, x + pad, yy, w - 2 * pad, size=8.0, leading=9.8, max_lines=3)

    note_h = 36
    panel(c, x + pad, y + pad, w - 2 * pad, note_h, fill=SOFT_AMBER, stroke=SOFT_AMBER, radius=7)
    draw_text(c, item.risk, x + pad + 8, y + pad + 22, w - 2 * pad - 16, size=7.2, leading=8.4, max_lines=2)


def insight_card(c: canvas.Canvas, title: str, body: str, x: float, y: float, w: float, h: float, fill, accent) -> None:
    panel(c, x, y, w, h, fill=fill, stroke=fill, radius=9)
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 13, y + h - 25, title)
    draw_text(c, body, x + 13, y + h - 45, w - 26, size=8.7, leading=11, max_lines=8)


def cover(c: canvas.Canvas, imgs: dict[str, Path]) -> None:
    c.setFillColor(CHARCOAL)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#edf4ee"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(M, PAGE_H - 54, "DECISION PACKET")
    c.setFont("Helvetica-Bold", 33)
    c.drawString(M, PAGE_H - 96, "Where We Should Live")
    c.drawString(M, PAGE_H - 134, "for BioScript Mississauga")
    draw_text(
        c,
        "Solo vs. sharing with brother vs. sharing with brother + cousin. Priorities: commute, cat, greenery, backyard access, and sane rent.",
        M,
        PAGE_H - 164,
        PAGE_W - 2 * M,
        size=12.2,
        leading=16,
        color=colors.HexColor("#cfe0d3"),
        max_lines=2,
    )

    grid_y = 252
    img_w = (PAGE_W - 2 * M - 14) / 2
    image_crop(c, imgs["valcourt"], M, grid_y, img_w, 238)
    image_crop(c, imgs["ridgeway-411"], M + img_w + 14, grid_y, img_w, 238)

    panel(c, M, 92, PAGE_W - 2 * M, 98, fill=colors.HexColor("#eef5ef"), stroke=colors.HexColor("#eef5ef"), radius=13)
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(M + 20, 154, "Short answer")
    draw_text(
        c,
        "Solo at $1,200 is mostly room/shared-house territory. Two people makes a decent basement or condo realistic. Three people gives the best shot at a house feel with space for the cat.",
        M + 20,
        134,
        PAGE_W - 2 * M - 40,
        size=10.5,
        leading=14,
        color=CHARCOAL,
        max_lines=3,
    )
    c.setFillColor(colors.HexColor("#d7e6da"))
    c.setFont("Helvetica", 8.5)
    c.drawString(M, 42, "Office target: 3330 Ridgeway Dr / 2180 Dunwin Dr, Mississauga")
    c.showPage()


def explanation(c: canvas.Canvas) -> None:
    page_base(c, "plain-language explanation", 2, accent=GREEN)
    y = title_block(c, "What we are optimizing for", "ELI16: not the cheapest listing; the place that works every day.", PAGE_H - 75)

    bullets = [
        ("Commute", "Close to Ridgeway/Dunwin keeps work simple and avoids daily friction."),
        ("Cat", "The cat needs a stable, calm space. Greenery or yard access makes a small home feel less boxed in."),
        ("Budget", "$1,200 solo is possible, but usually means a room or shared-house setup."),
        ("Sharing", "Two or three people can unlock a better kitchen, laundry, storage, and outdoor access."),
    ]
    col_w = (PAGE_W - 2 * M - 16) / 2
    for idx, (label, body) in enumerate(bullets):
        x = M + (idx % 2) * (col_w + 16)
        bullet_y = y - (idx // 2) * 69
        panel(c, x, bullet_y - 57, col_w, 50, fill=PANEL, stroke=LINE, radius=8)
        c.setFillColor(GREEN)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(x + 14, bullet_y - 25, label)
        draw_text(c, body, x + 82, bullet_y - 19, col_w - 96, size=8.8, leading=10.7, max_lines=3)

    table_y = y - 166
    panel(c, M, table_y - 162, PAGE_W - 2 * M, 152, fill=PANEL, stroke=LINE, radius=10)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(M + 16, table_y - 35, "Budget reality")
    rows = [
        ("Solo", "$1,200", "Mostly room/shared-house territory", SOFT_AMBER),
        ("2 people", "$2,400", "Realistic for 2-bed basement or condo", SOFT_BLUE),
        ("3 people", "$3,600", "Best shot at townhouse or house-style", SOFT_GREEN),
    ]
    yy = table_y - 64
    for label, amount, likely, fill in rows:
        panel(c, M + 16, yy - 21, PAGE_W - 2 * M - 32, 28, fill=fill, stroke=fill, radius=7)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 9.6)
        c.drawString(M + 30, yy - 4, label)
        c.drawCentredString(M + 156, yy - 4, amount)
        c.setFont("Helvetica", 9.0)
        c.drawString(M + 224, yy - 4, likely)
        yy -= 33

    panel(c, M, 116, PAGE_W - 2 * M, 102, fill=SOFT_GREEN, stroke=SOFT_GREEN, radius=10)
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(M + 18, 179, "Recommendation")
    draw_text(
        c,
        "Prioritize a 3-person shared setup if everyone is reliable. Keep 2-person as the active fallback. Use solo only for an unusually strong cat-friendly house-share or basement room.",
        M + 18,
        158,
        PAGE_W - 2 * M - 36,
        size=10.2,
        leading=13.5,
        max_lines=3,
    )
    footer(c, "Sources: BioScript, Zolo, Zumper, RentCafe, Apartments.com")
    c.showPage()


def listing_page(c: canvas.Canvas, page: int, section: str, title: str, subtitle: str, summary: str, items: list, imgs: dict[str, Path], accent=GREEN) -> None:
    page_base(c, section, page, accent)
    y = title_block(c, title, subtitle, PAGE_H - 75)
    fill = SOFT_GREEN if accent == GREEN else SOFT_BLUE if accent == BLUE else SOFT_AMBER
    summary_band(c, summary, y, fill, height=58)
    card_w = (PAGE_W - 2 * M - GAP) / 2
    card_h = 236
    top_y = 334
    bottom_y = 82
    slots = [
        (M, top_y),
        (M + card_w + GAP, top_y),
        (M, bottom_y),
        (M + card_w + GAP, bottom_y),
    ]
    for idx, item in enumerate(items[:4]):
        x, y0 = slots[idx]
        compact_listing_card(c, item, imgs[item.slug], x, y0, card_w, card_h, accent)
    footer(c, "Listing images: sources named in text; current availability not guaranteed")
    c.showPage()


def solo_rules(c: canvas.Canvas, imgs: dict[str, Path]) -> None:
    page_base(c, "solo housing", 8, AMBER)
    y = title_block(c, "Solo backup: strict rules", "Choose solo only when the deal is clearly stronger than expected.", PAGE_H - 75)
    summary_band(
        c,
        "Solo is the most private option, but the weakest value at $1,200. Keep it alive only for unusually good house-share or basement-room listings with cat clarity and green access.",
        y,
        SOFT_AMBER,
        height=70,
    )

    item = next(i for i in LISTINGS if i.slug == "trellis")
    card_w = 230
    listing_card(c, item, imgs[item.slug], M, 92, card_w, 430, AMBER)

    x = M + card_w + 28
    w = PAGE_W - M - x
    panel(c, x, 92, w, 430, fill=PANEL, stroke=LINE, radius=10)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(x + 20, 484, "Search rules")
    rules = [
        "Ask about one quiet indoor cat before viewing.",
        "Reject dark, damp, or low-window basements.",
        "Prefer real yard, patio, or nearby park access.",
        "Confirm utilities, internet, laundry, parking, and deposits.",
        "For shared homes, ask who lives there and what the house rules are.",
    ]
    yy = 452
    for idx, rule in enumerate(rules, 1):
        c.setFillColor(SOFT_AMBER if idx in (2, 4) else SOFT_GREEN)
        c.circle(x + 28, yy - 2, 10, stroke=0, fill=1)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(x + 28, yy - 5, str(idx))
        draw_text(c, rule, x + 48, yy + 2, w - 70, size=9.6, leading=12, max_lines=2)
        yy -= 48

    panel(c, x + 20, 122, w - 40, 88, fill=GREEN, stroke=GREEN, radius=9)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 38, 182, "Message line")
    draw_text(
        c,
        "I have one quiet indoor cat. Is the room/unit suitable for that, and is backyard or green access included?",
        x + 38,
        162,
        w - 76,
        size=9.2,
        leading=12.5,
        color=colors.white,
        max_lines=3,
    )
    footer(c, "Image: RentCafe listing photo")
    c.showPage()


def build() -> None:
    imgs = download_images()
    missing = [item.slug for item in LISTINGS if item.slug not in imgs]
    if missing:
        raise RuntimeError("Missing images: " + ", ".join(missing))

    c = canvas.Canvas(str(PDF_PATH), pagesize=letter)
    c.setTitle("BioScript Mississauga Housing Decision Packet")
    cover(c, imgs)
    explanation(c)

    three = [i for i in LISTINGS if i.scenario == "3-person"]
    two = [i for i in LISTINGS if i.scenario == "2-person"]
    solo = [i for i in LISTINGS if i.scenario == "solo"]

    listing_page(c, 3, "3-person housing", "3-person housing: top options", "Brother + cousin unlocks the house-style search.", "Best fit for house feel, backyard potential, and keeping each person's share near the original budget.", three[:4], imgs, GREEN)
    listing_page(c, 4, "3-person housing", "3-person housing: backups", "Use these if the first four are unavailable.", "Backups widen the search, but cat rules and commute become more important filters.", three[4:8], imgs, GREEN)
    listing_page(c, 5, "2-person housing", "2-person housing: top options", "Brother-share keeps privacy simpler while improving the budget.", "Best balance if cousin is uncertain: quieter than three people, stronger than solo, and still realistic near Ridgeway/Dunwin.", two[:4], imgs, BLUE)
    listing_page(c, 6, "2-person housing", "2-person housing: backups", "Cheap basement vs. better managed-property experience.", "Use these to decide whether lowest cost, shortest commute, or cleaner management matters most.", two[4:8], imgs, BLUE)
    listing_page(c, 7, "solo housing", "Solo housing: top options", "$1,200 works best as a house-share budget.", "Solo should stay alive only if the listing is close to BioScript, green, cat-compatible, and not a damp basement.", solo[:4], imgs, AMBER)
    listing_page(c, 8, "solo housing", "Solo housing: backups + rules", "Use solo only when the deal is clearly stronger than expected.", "Ask about one quiet indoor cat, reject damp basements, and confirm total monthly cost before touring.", solo[4:8], imgs, AMBER)
    c.save()
    print(PDF_PATH)


if __name__ == "__main__":
    build()
