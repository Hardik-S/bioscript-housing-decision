from __future__ import annotations

import io
import os
import re
import textwrap
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
ASSET_DIR = ROOT / "assets"
PDF_PATH = ROOT / "BioScript_Housing_Decision_Packet.pdf"

PAGE_W, PAGE_H = letter
M = 42

INK = colors.HexColor("#17211c")
MUTED = colors.HexColor("#5d6c64")
LINE = colors.HexColor("#d8e2dc")
GREEN = colors.HexColor("#2f6b4f")
GREEN_DARK = colors.HexColor("#194230")
BLUE = colors.HexColor("#255d8d")
AMBER = colors.HexColor("#b46b24")
BG = colors.HexColor("#f6f8f4")
PANEL = colors.HexColor("#ffffff")
SOFT_GREEN = colors.HexColor("#e8f1ea")
SOFT_BLUE = colors.HexColor("#e8f0f7")
SOFT_AMBER = colors.HexColor("#f6eee2")


@dataclass
class Listing:
    slug: str
    name: str
    scenario: str
    price: str
    per_person: str
    area: str
    fit: str
    risk: str
    image_url: str
    source: str
    badge: str


LISTINGS = [
    Listing(
        "daniels-annex",
        "Daniels Gateway - Annex",
        "3-person",
        "$3,050 est.",
        "~$1,017 each",
        "5625 Glen Erin Dr, Central Erin Mills",
        "Townhouse-style rental, pet-friendly operator, close to parks and errands. Strong shared-home baseline.",
        "Confirm exact unit, utilities, parking, and cat rules before applying.",
        "https://danielsgateway.com/wp-content/uploads/2022/12/26-5625GlenErinDr-9-1620x1080.jpg",
        "danielsgateway.com",
        "Best shared value",
    ),
    Listing(
        "daniels-rio",
        "Daniels Erin Centre",
        "3-person",
        "$3,050-$3,275",
        "~$1,017-$1,092 each",
        "2900 Rio Ct, Central Erin Mills",
        "3-bed rental community near Erin Mills Town Centre. Better space, predictable management, easy commute.",
        "Ask which units are cat-friendly and whether outdoor space is private or shared.",
        "https://danielsgateway.com/wp-content/uploads/2021/06/01.-Front-Exterior-810x1080.jpg",
        "danielsgateway.com",
        "Reliable operator",
    ),
    Listing(
        "creditview-argentia",
        "Creditview / Argentia Townhouse",
        "3-person",
        "$2,950",
        "~$983 each",
        "Streetsville / Meadowvale edge",
        "3 bed, 3 bath, around 1,800 sq ft. Listing marks cats/dogs OK and mentions garden/outdoor space.",
        "Photo has listing text overlay. Verify current availability and exact address before touring.",
        "https://img.zumpercdn.com/609326995/1280x960?dpr=1&fit=crop&h=542&q=76&w=991",
        "zumper.com",
        "Cat-friendly",
    ),
    Listing(
        "valcourt",
        "3211 Valcourt Crescent",
        "3-person",
        "$3,600",
        "$1,200 each",
        "Erin Mills, near Ridgeway/McMaster",
        "Detached 4-bed main house with garage and a very short BioScript commute. Strong space-for-money option.",
        "Pet status not visible. Basement excluded; confirm what storage and yard access are included.",
        "https://cdn.thecanadianhome.com/property/PhotoW12628258-1.jpeg?aspect_ratio=10%3A7&quality=100&width=960",
        "thecanadianhome.com",
        "Closest house feel",
    ),
    Listing(
        "bidwell",
        "6035 Bidwell Trail",
        "3-person",
        "$3,200",
        "~$1,067 each",
        "East Credit",
        "3-bed townhouse with private deck and backyard access, close to parks and daily errands.",
        "Dogs allowed but cats listed as not allowed; only keep if cat rules can be solved.",
        "https://img.zumpercdn.com/894012619/1280x960?fit=crop&h=360&w=392",
        "padmapper.com",
        "Backyard",
    ),
    Listing(
        "lakeshore",
        "200 Lakeshore Rd W Townhouse",
        "3-person",
        "$2,900",
        "~$967 each",
        "Southwest Oakville",
        "3-bed townhouse community with outdoor space and large basement, near lake/park amenities.",
        "No pets listed and commute is longer; use as price benchmark or backup only.",
        "https://img.zumpercdn.com/882555983/1280x960?dpr=1&fit=crop&h=542&q=76&w=991",
        "zumper.com",
        "Price benchmark",
    ),
    Listing(
        "kimbermount",
        "4600 Kimbermount Ave #89",
        "3-person",
        "$3,000",
        "$1,000 each",
        "Central Erin Mills",
        "3-bed townhouse near Erin Mills Town Centre, parks, schools, parking, and major routes.",
        "Zillow lists no pets; use only if cat rules can be solved or as a location benchmark.",
        "https://photos.zillowstatic.com/fp/635f80bcab45c7706018d4ca0261a0ae-cc_ft_960.jpg",
        "zillow.com",
        "Location benchmark",
    ),
    Listing(
        "ridgeway-411",
        "3401 Ridgeway Dr Unit 411",
        "2-person",
        "$2,199",
        "~$1,100 each",
        "Ridgeway / Erin Mills",
        "2-bed condo near the office cluster. Best commute, cleanest simple two-person option.",
        "Less backyard/greenery. Confirm pet restrictions and real utility total.",
        "https://photos.zolo.ca/411-3401-ridgeway-drive-mississauga-W13022574-1-p.jpg?20260513103100",
        "zolo.ca",
        "Best commute",
    ),
    Listing(
        "skyview",
        "3896 Skyview St Basement",
        "2-person",
        "$1,850",
        "~$925 each",
        "Churchill Meadows",
        "2-bed basement, park-facing street, very strong price for sharing with brother.",
        "Apartments.com says no pets. Treat as a price anchor unless the landlord confirms a cat exception.",
        "https://images1.apartments.com/i2/g-kQ_Mj7elPRGY92y9LI6V2oobXU8TLBxpKngPO28rg/116/3896-skyview-st-unit-2-bed-1-bath-basement-mississauga-on-primary-photo.jpg?p=1",
        "apartments.com",
        "Best price",
    ),
    Listing(
        "wheat-boom",
        "482 Wheat Boom Dr Basement",
        "2-person",
        "$1,750",
        "~$875 each",
        "Oakville, Dundas / Trafalgar",
        "2-bed basement with listing page marking cats OK and dogs OK. Good price if the longer commute is acceptable.",
        "Text later says no pets, so treat this as a must-confirm contradiction before spending time.",
        "https://img.zumpercdn.com/871335082/1280x960?dpr=1&fit=crop&h=542&q=76&w=991",
        "zumper.com",
        "Pet note conflict",
    ),
    Listing(
        "sir-johns",
        "3061 Sir John's Homestead",
        "2-person",
        "$2,549-$3,391",
        "~$1,275-$1,696 each",
        "Erin Mills / Sheridan",
        "Townhouse-style rental community with large floor plans and 2-3 bed availability.",
        "Above the clean budget line. Still useful as a comparison for space and professionalism.",
        "https://images1.apartments.com/i2/6JDfNB0QiLDJkYeT-SAo3cInywF9GRX9aIwTQLHOhPw/116/3061-sir-johns-homestead-mississauga-on-primary-photo.jpg?p=1",
        "apartments.com",
        "Stretch quality",
    ),
    Listing(
        "kellandy",
        "5644 Kellandy Run Basement",
        "2-person",
        "$1,700",
        "~$850 each",
        "Churchill Meadows",
        "2-bed basement in a detached home near Ridgeway Plaza, highways, transit, parks, and schools.",
        "Pets are contact-manager; confirm cat acceptance and basement light/dampness in person.",
        "https://assets-listings.rew.ca/listing/treb_dla/W12738138/00_W12738138_c62ba5b1c682e0132870893b4cc35415.jpeg?auto=format&fit=crop&h=392&trim=auto&w=753",
        "rew.ca",
        "Cheapest 2-bed",
    ),
    Listing(
        "stardust",
        "3914 Stardust Drive Basement",
        "2-person",
        "$1,800",
        "~$900 each",
        "Churchill Meadows",
        "Nearby 2-bed basement backup from the same REW search cluster.",
        "Confirm listing status, cat rules, utilities, and whether the layout works for two adults.",
        "https://assets-listings.rew.ca/listing/treb_dla/W12401462/00_W12401462_fa10c830235e3fbb94a608c2f645f856.jpeg?auto=format&fit=crop&h=287&sharp=25&trim=auto&w=480",
        "rew.ca",
        "Backup",
    ),
    Listing(
        "tresca",
        "5257 Tresca Trail Basement",
        "2-person",
        "$1,850",
        "~$925 each",
        "Churchill Meadows",
        "2-bed, 2-bath basement backup in the Churchill Meadows cluster.",
        "Confirm current availability, cat rules, utilities, and whether the room split is fair.",
        "https://assets-listings.rew.ca/listing/treb_dla/W12443791/00_W12443791_c1f226341654a312a4c2dc57097dccd3.jpeg?auto=format&fit=crop&h=287&sharp=25&trim=auto&w=480",
        "rew.ca",
        "Backup",
    ),
    Listing(
        "council-ring",
        "2475 Council Ring Rd",
        "solo",
        "$1,100",
        "Solo",
        "Erin Mills",
        "Best solo fit: green front/back lawn, perennial garden, utilities included, close enough to BioScript.",
        "Shared kitchen. Ask directly if one quiet indoor cat is accepted and whether yard access is real.",
        "https://fwd.blob.core.windows.net/full/W12945776-15203806-1.jpeg",
        "forestwood.ca",
        "Best solo lead",
    ),
    Listing(
        "cider-mill",
        "3371 Cider Mill Place Room C",
        "solo",
        "$1,000",
        "Solo",
        "Erin Mills, near UTM / Credit River",
        "Separate-entry basement room, utilities included, green neighbourhood, useful backup under budget.",
        "Shared kitchen/laundry. Confirm cat rules and whether the room has enough light.",
        "https://cdngeneral.rentcafe.com/dmslivecafe/3/2377872/2377872-1-3.jpg?height=450&mode=crop&quality=80&width=550",
        "rentcafe.com",
        "Budget fit",
    ),
    Listing(
        "trellis",
        "4253 Trellis Crescent Upper",
        "solo",
        "$900 / room",
        "Solo",
        "Erin Mills / Folkway",
        "Furnished room in a house with parks nearby. Useful if the goal is cheap, stable, and close.",
        "Shared bathroom/kitchen. Cat access to common areas must be agreed in writing.",
        "https://cdngeneral.rentcafe.com/dmslivecafe/3/2238711/2238711-1-2.jpg?height=450&mode=crop&quality=80&width=550",
        "rentcafe.com",
        "Cheapest real lead",
    ),
    Listing(
        "strabane",
        "3366 Strabane Drive",
        "solo",
        "$1,200",
        "Solo",
        "Erindale",
        "1-bed lead under the solo cap with a cleaner interior look than many basement-room options.",
        "Confirm cat acceptance, total utilities, commute, and whether it is private or shared.",
        "https://cdngeneral.rentcafe.com/dmslivecafe/3/2397416/2397416-1-3.jpg?quality=90&width=480",
        "rentcafe.com",
        "At cap",
    ),
    Listing(
        "harman",
        "2518 Harman Court Basement",
        "solo",
        "$1,200",
        "Solo",
        "Clarkson",
        "1-bed basement lead at the cap; a possible solo backup if commute and cat rules work.",
        "Confirm cat rules, window/light quality, dampness, and whether the location is too far south.",
        "https://cdngeneral.rentcafe.com/dmslivecafe/3/2399005/2399005-1-2.jpg?quality=90&width=480",
        "rentcafe.com",
        "Backup solo",
    ),
    Listing(
        "sanderling",
        "3441 Sanderling Cres Bsmt #2",
        "solo",
        "$900",
        "Solo",
        "Erin Mills",
        "Lower-cost Erin Mills basement-room lead, useful if keeping monthly burn low matters most.",
        "Confirm privacy, shared spaces, cat acceptance, and whether the room is livable long-term.",
        "https://cdngeneral.rentcafe.com/dmslivecafe/3/2346094/2346094-1-6.jpg?quality=90&width=480",
        "rentcafe.com",
        "Low cost",
    ),
    Listing(
        "princelea",
        "1722 Princelea Place Room B",
        "solo",
        "$850",
        "Solo",
        "East Credit",
        "Lowest-cost RentCafe lead; useful as a burn-rate fallback if commute and shared setup work.",
        "Confirm exact sharing setup, cat acceptance, and whether the room is suitable beyond short-term.",
        "https://cdngeneral.rentcafe.com/dmslivecafe/3/2397416/2397416-1-3.jpg?quality=90&width=480",
        "rentcafe.com",
        "Lowest cost",
    ),
    Listing(
        "collegeway",
        "2079 The Collegeway Unit 6",
        "solo",
        "$900",
        "Solo",
        "Erin Mills",
        "Erin Mills lead under budget and close to the target search area.",
        "Confirm cat acceptance, privacy, utilities, and whether the rental is a room or full unit.",
        "https://cdngeneral.rentcafe.com/dmslivecafe/3/2412503/2412503-1-2.jpg?quality=90&width=480",
        "rentcafe.com",
        "Erin Mills",
    ),
]


def download_images() -> dict[str, Path]:
    ASSET_DIR.mkdir(exist_ok=True)
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"),
        ("Accept", "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"),
    ]
    paths: dict[str, Path] = {}
    for item in LISTINGS:
        out = ASSET_DIR / f"{item.slug}.jpg"
        if not out.exists() or out.stat().st_size < 1024:
            try:
                with opener.open(item.image_url, timeout=30) as resp:
                    data = resp.read()
                img = Image.open(io.BytesIO(data)).convert("RGB")
                img.thumbnail((1800, 1400))
                img.save(out, "JPEG", quality=88, optimize=True)
            except Exception as exc:
                print(f"IMAGE_DOWNLOAD_FAILED {item.slug}: {exc}")
                continue
        paths[item.slug] = out
    return paths


def wrap_lines(text: str, font: str, size: int, max_width: float) -> list[str]:
    words = re.sub(r"\s+", " ", text.strip()).split(" ")
    lines: list[str] = []
    current = ""
    for word in words:
        test = word if not current else f"{current} {word}"
        if stringWidth(test, font, size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, width: float, font="Helvetica", size=9.5, leading=13, color=INK) -> float:
    c.setFont(font, size)
    c.setFillColor(color)
    for para in text.split("\n"):
        for line in wrap_lines(para, font, size, width):
            c.drawString(x, y, line)
            y -= leading
        y -= leading * 0.35
    return y


def draw_header(c: canvas.Canvas, section: str, page_num: int) -> None:
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 8.8)
    c.drawString(M, PAGE_H - 28, section.upper())
    c.setFont("Helvetica", 8.4)
    c.drawRightString(PAGE_W - M, PAGE_H - 28, f"BioScript Mississauga housing packet  |  page {page_num}")
    c.setStrokeColor(LINE)
    c.line(M, PAGE_H - 36, PAGE_W - M, PAGE_H - 36)


def draw_footer(c: canvas.Canvas, source_text: str = "") -> None:
    c.setStrokeColor(LINE)
    c.line(M, 32, PAGE_W - M, 32)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.8)
    footer = "Prepared May 13, 2026. Confirm price, utilities, availability, and pet rules before applying."
    c.drawString(M, 20, footer)
    if source_text:
        c.drawRightString(PAGE_W - M, 20, source_text[:95])


def draw_title(c: canvas.Canvas, title: str, subtitle: str, y: float) -> float:
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(M, y, title)
    y -= 24
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(M, y, subtitle)
    return y - 22


def draw_cover_image(c: canvas.Canvas, image_path: Path, x: float, y: float, w: float, h: float) -> None:
    c.saveState()
    c.roundRect(x, y, w, h, 12, stroke=0, fill=0)
    c.clipPath(c.beginPath(), stroke=0, fill=0)
    c.restoreState()
    draw_image_crop(c, image_path, x, y, w, h)


def draw_image_crop(c: canvas.Canvas, image_path: Path, x: float, y: float, w: float, h: float) -> None:
    img = Image.open(image_path)
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
    crop.convert("RGB").save(bio, "JPEG", quality=90)
    bio.seek(0)
    c.drawImage(ImageReader(bio), x, y, w, h, mask="auto")


def draw_round_panel(c: canvas.Canvas, x: float, y: float, w: float, h: float, fill=PANEL, stroke=LINE, radius=10) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.roundRect(x, y, w, h, radius, stroke=1, fill=1)


def draw_pill(c: canvas.Canvas, text: str, x: float, y: float, fill, color=INK) -> None:
    width = stringWidth(text, "Helvetica-Bold", 8) + 16
    c.setFillColor(fill)
    c.roundRect(x, y, width, 17, 8, stroke=0, fill=1)
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 8, y + 5, text)


def card(c: canvas.Canvas, item: Listing, image_path: Path, x: float, y: float, w: float, h: float, accent=GREEN) -> None:
    draw_round_panel(c, x, y, w, h)
    img_h = h * 0.43
    draw_image_crop(c, image_path, x + 9, y + h - img_h - 9, w - 18, img_h)
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.white)
    c.rect(x + 9, y + h - img_h - 9, w - 18, 0.1, stroke=0, fill=1)
    draw_pill(c, item.badge, x + 16, y + h - 30, SOFT_GREEN if accent == GREEN else SOFT_BLUE)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(x + 16, y + h - img_h - 28, item.name)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(accent)
    c.drawString(x + 16, y + h - img_h - 45, f"{item.price}  |  {item.per_person}")
    c.setFont("Helvetica", 8.5)
    c.setFillColor(MUTED)
    c.drawString(x + 16, y + h - img_h - 59, item.area)
    yy = y + h - img_h - 80
    yy = draw_wrapped(c, item.fit, x + 16, yy, w - 32, size=9.2, leading=11.7, color=INK)
    c.setFillColor(SOFT_AMBER)
    c.roundRect(x + 14, y + 28, w - 28, 42, 7, stroke=0, fill=1)
    draw_wrapped(c, f"Check: {item.risk}", x + 22, y + 56, w - 44, size=8.1, leading=9.6, color=INK)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.1)
    c.drawRightString(x + w - 16, y + 10, f"Image/source: {item.source}")


def page_cover(c: canvas.Canvas, imgs: dict[str, Path]) -> None:
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#eef4ec"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(M, PAGE_H - 48, "DECISION PACKET")
    c.setFont("Helvetica-Bold", 33)
    c.drawString(M, PAGE_H - 92, "Where We Should Live")
    c.drawString(M, PAGE_H - 130, "for BioScript Mississauga")
    c.setFont("Helvetica", 13)
    c.setFillColor(colors.HexColor("#cfe2d3"))
    c.drawString(M, PAGE_H - 158, "Solo vs. sharing with brother vs. sharing with brother + cousin")
    c.drawString(M, PAGE_H - 178, "Priorities: commute, cat, greenery, backyard access, and sane rent.")

    draw_image_crop(c, imgs["valcourt"], M, 250, 250, 260)
    draw_image_crop(c, imgs["ridgeway-411"], M + 268, 330, 260, 180)
    draw_image_crop(c, imgs["council-ring"], M + 268, 250, 260, 68)

    c.setFillColor(colors.HexColor("#eef5ef"))
    c.roundRect(M, 82, PAGE_W - 2 * M, 110, 14, stroke=0, fill=1)
    c.setFillColor(GREEN_DARK)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(M + 22, 158, "Short answer")
    c.setFont("Helvetica", 11)
    cover_copy = (
        "Solo at $1,200 is mostly room/shared-house territory. "
        "Two people makes a decent basement or condo realistic. "
        "Three people gives the best shot at a house feel with space for the cat."
    )
    draw_wrapped(c, cover_copy, M + 22, 137, PAGE_W - 2 * M - 44, size=10.5, leading=14, color=GREEN_DARK)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#b8cdbd"))
    c.drawString(M, 42, "Office target: 3330 Ridgeway Dr / 2180 Dunwin Dr, Mississauga")
    c.showPage()


def page_explanation(c: canvas.Canvas) -> None:
    draw_header(c, "Plain-language explanation for brother and cousin", 2)
    y = draw_title(c, "What we are actually optimizing for", "ELI16: the goal is not the cheapest listing; it is the place that works every day.", PAGE_H - 78)
    left = M
    right = PAGE_W / 2 + 12
    copy = (
        "This search is mainly about finding a place that works in real life, not just on paper.\n"
        "The strongest options are shared houses or larger apartments with outdoor access, greenery nearby, and enough room for everyone to live comfortably. A backyard or green space matters because it makes the home feel less cramped, gives the cat more stimulation, and creates a better day-to-day setup than being boxed into a small unit.\n"
        "A solo place around $1,200 is possible in theory, but it is hard to make it good. At that price, the tradeoffs usually show up quickly: smaller space, weaker location, older finishes, limited outdoor access, or a place that feels temporary.\n"
        "A 2-person or 3-person share improves the fit because the same total budget can support a better home: more space, a usable kitchen, laundry, storage, and ideally outdoor access."
    )
    draw_wrapped(c, copy, left, y, PAGE_W / 2 - M - 18, size=10.2, leading=14.2)

    draw_round_panel(c, right, y - 210, PAGE_W - M - right, 210, fill=PANEL)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(INK)
    c.drawString(right + 18, y - 32, "Budget reality")
    rows = [("Solo", "$1,200", "room / shared house"), ("2 people", "$2,400", "2-bed basement or condo"), ("3 people", "$3,600", "townhouse / house-style")]
    yy = y - 65
    for label, total, likely in rows:
        c.setFillColor(SOFT_GREEN if label == "3 people" else SOFT_BLUE if label == "2 people" else SOFT_AMBER)
        c.roundRect(right + 18, yy - 8, PAGE_W - M - right - 36, 34, 8, stroke=0, fill=1)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(right + 30, yy + 8, label)
        c.drawCentredString(right + 135, yy + 8, total)
        c.setFont("Helvetica", 9)
        c.drawString(right + 195, yy + 8, likely)
        yy -= 44

    draw_round_panel(c, M, 145, PAGE_W - 2 * M, 140, fill=colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(GREEN_DARK)
    c.drawString(M + 18, 250, "Recommendation")
    rec = (
        "Prioritize 3-person if everyone is reliable. Keep 2-person as the active fallback. "
        "Use solo only for an unusually strong cat-friendly house-share or basement room. "
        "Reject places that fail commute, pet clarity, damp/safety checks, or basic roommate agreement."
    )
    draw_wrapped(c, rec, M + 18, 226, PAGE_W - 2 * M - 36, size=11, leading=15)
    draw_footer(c, "sources: BioScript, Zolo, Zumper, RentCafe, Apartments.com, The Canadian Home")
    c.showPage()


def scenario_intro(c: canvas.Canvas, page_num: int, title: str, subtitle: str, body: str, score: list[tuple[str, int]], accent) -> float:
    draw_header(c, title, page_num)
    y = draw_title(c, title, subtitle, PAGE_H - 78)
    draw_round_panel(c, M, y - 96, PAGE_W - 2 * M, 92, fill=PANEL)
    draw_wrapped(c, body, M + 18, y - 24, PAGE_W - 2 * M - 36, size=10, leading=13.2)
    y -= 124
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(MUTED)
    c.drawString(M, y, "FAST SCORE")
    y -= 15
    x = M
    for label, val in score:
        c.setFillColor(colors.white)
        c.roundRect(x, y - 20, 118, 38, 8, stroke=1, fill=1)
        c.setFillColor(accent)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x + 12, y - 6, str(val))
        c.setFillColor(INK)
        c.setFont("Helvetica", 8)
        c.drawString(x + 42, y - 2, label)
        x += 128
    return y - 50


def page_cards(c: canvas.Canvas, page_num: int, title: str, subtitle: str, body: str, items: list[Listing], imgs: dict[str, Path], accent=GREEN) -> None:
    y = scenario_intro(c, page_num, title, subtitle, body, [("budget fit", 8), ("cat/green fit", 8), ("commute", 8), ("privacy", 6)], accent)
    gap = 18
    card_w = (PAGE_W - 2 * M - gap) / 2
    card_h = 385
    for i, item in enumerate(items[:2]):
        x = M + i * (card_w + gap)
        card(c, item, imgs[item.slug], x, 70, card_w, card_h, accent=accent)
    draw_footer(c, "image sources listed on each card")
    c.showPage()


def page_solo_action(c: canvas.Canvas, imgs: dict[str, Path]) -> None:
    draw_header(c, "Solo housing", 8)
    y = draw_title(c, "Solo backup: strict rules", "A good solo option exists, but the search rules need to be strict.", PAGE_H - 78)
    item = next(i for i in LISTINGS if i.slug == "trellis")
    card(c, item, imgs[item.slug], M, 224, 250, 372, accent=AMBER)
    x = M + 278
    draw_round_panel(c, x, 224, PAGE_W - M - x, 372, fill=PANEL)
    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(INK)
    c.drawString(x + 18, 558, "Solo search rules")
    rules = [
        "Ask about one quiet indoor cat before viewing.",
        "Do not accept a dark/damp basement just to stay near $1,200.",
        "Prefer house-share with real yard or park access over tiny isolated units.",
        "Confirm total rent: utilities, internet, parking, laundry, deposits.",
        "If sharing kitchen/bathroom, ask who lives there and what the house rules are.",
    ]
    yy = 528
    for n, rule in enumerate(rules, 1):
        c.setFillColor(SOFT_AMBER if n in (2, 4) else SOFT_GREEN)
        c.circle(x + 25, yy + 2, 9, stroke=0, fill=1)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + 25, yy - 1, str(n))
        yy = draw_wrapped(c, rule, x + 44, yy + 5, PAGE_W - M - x - 62, size=9.3, leading=12)
        yy -= 8
    c.setFillColor(GREEN_DARK)
    c.roundRect(x + 18, 254, PAGE_W - M - x - 36, 72, 10, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 34, 300, "Message line to use")
    msg = "I have one quiet indoor cat. Is the room/unit suitable for that, and is any backyard or green access included?"
    draw_wrapped(c, msg, x + 34, 282, PAGE_W - M - x - 68, size=8.8, leading=11, color=colors.white)
    draw_footer(c, "image source: rentcafe.com")
    c.showPage()


def build_pdf() -> None:
    imgs = download_images()
    missing = [item.slug for item in LISTINGS if item.slug not in imgs]
    if missing:
        raise RuntimeError(f"Missing images for: {', '.join(missing)}")

    c = canvas.Canvas(str(PDF_PATH), pagesize=letter)
    c.setTitle("BioScript Mississauga Housing Decision Packet")

    page_cover(c, imgs)
    page_explanation(c)

    three = [i for i in LISTINGS if i.scenario == "3-person"]
    two = [i for i in LISTINGS if i.scenario == "2-person"]
    solo = [i for i in LISTINGS if i.scenario == "solo"]

    page_cards(
        c,
        3,
        "3-person housing: best target",
        "Brother + cousin unlocks the house-style search.",
        "This is the strongest setup if everyone can align on lease responsibility, chores, parking, guest rules, and cat boundaries. It turns the search from finding a cheap unit into finding the right home.",
        three[:2],
        imgs,
        accent=GREEN,
    )
    page_cards(
        c,
        4,
        "3-person housing: house-style alternatives",
        "Use these if the Daniels options are unavailable or too managed-community-heavy.",
        "The house-style alternatives have the best chance of backyard access. They also need the most careful application check: lease names, pet permission, utilities, snow/lawn duties, and basement exclusions.",
        three[2:],
        imgs,
        accent=GREEN,
    )
    page_cards(
        c,
        5,
        "2-person housing: safest fallback",
        "Brother-share keeps privacy simpler while improving the budget.",
        "Two people is the clean middle option. It is quieter than a three-person setup and still makes better space possible than solo. Backyard access is possible, but it has to be confirmed listing by listing.",
        two[:2],
        imgs,
        accent=BLUE,
    )
    page_cards(
        c,
        6,
        "2-person housing: cheaper vs. better tradeoff",
        "These show the practical range: cheap basement to professionally managed townhome-style.",
        "The right two-person choice depends on what matters more: lowest monthly cost, shortest commute, or a cleaner managed-property experience. Cat clarity is still a first-contact question.",
        two[2:],
        imgs,
        accent=BLUE,
    )
    page_cards(
        c,
        7,
        "Solo housing: realistic, but narrow",
        "$1,200 works best as a house-share budget, not a private-apartment budget.",
        "Solo should stay alive as a backup only if the listing is unusually strong: close to BioScript, green, cat-compatible, and not a damp basement. The first two leads are the most worth contacting.",
        solo[:2],
        imgs,
        accent=AMBER,
    )
    page_solo_action(c, imgs)
    c.save()
    print(PDF_PATH)


if __name__ == "__main__":
    build_pdf()
