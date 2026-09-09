from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(r"G:\Mi unidad\Fabrica_DB\Maquinas\KDT KD610HZ")
OUT = Path(r"G:\Mi unidad\Fabrica_DB\Maquinas\KDT KD610HZ\11_Revision_Interna\_photo_review_sheets")
OUT.mkdir(exist_ok=True)

try:
    font = ImageFont.truetype("arial.ttf", 22)
except OSError:
    font = ImageFont.load_default()

def make_sheets(folder_name: str, per_sheet: int) -> None:
    files = sorted((BASE / folder_name).glob("*"))
    for sheet_no, start in enumerate(range(0, len(files), per_sheet), 1):
        group = files[start:start + per_sheet]
        cell_w, cell_h = 420, 330
        sheet = Image.new("RGB", (cell_w * 2, cell_h * ((len(group) + 1) // 2)), "white")
        draw = ImageDraw.Draw(sheet)
        for idx, path in enumerate(group):
            try:
                img = Image.open(path).convert("RGB")
                img.thumbnail((cell_w - 20, cell_h - 55))
                x = (idx % 2) * cell_w + (cell_w - img.width) // 2
                y = (idx // 2) * cell_h + 8
                sheet.paste(img, (x, y))
                label = f"{start + idx + 1}: {path.name}"
                draw.text(((idx % 2) * cell_w + 8, (idx // 2) * cell_h + cell_h - 38), label[:52], fill="black", font=font)
            except Exception as exc:
                draw.text(((idx % 2) * cell_w + 8, (idx // 2) * cell_h + 8), f"ERROR {path.name}: {exc}", fill="red", font=font)
        sheet.save(OUT / f"{folder_name.lower()}_{sheet_no:02d}.jpg", quality=90)

make_sheets("09_Fotos_Software", 8)
make_sheets("10_Fotos_Maquina", 8)
print(f"Created {len(list(OUT.glob('*.jpg')))} review sheets in {OUT}")
