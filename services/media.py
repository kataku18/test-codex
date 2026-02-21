from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


def build_post_image(topic: str, audience: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    width, height = 1080, 1080
    image = Image.new('RGB', (width, height), '#f5f3ff')
    draw = ImageDraw.Draw(image)

    draw.rectangle([(70, 70), (width - 70, height - 70)], outline='#7c3aed', width=8)
    draw.text((120, 170), 'AI Auto Post', fill='#4c1d95')
    draw.text((120, 280), f'Topic: {topic[:60]}', fill='#1f2937')
    draw.text((120, 360), f'Audience: {audience[:60]}', fill='#374151')

    image.save(output_path)
