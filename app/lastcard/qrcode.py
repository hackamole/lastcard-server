import os
from urllib.parse import urljoin
import qrcode
import qrcode.image.svg


def generate(base_url, base_path, card_id):
    # url = urljoin(base_url, '/'.join(['card', card_id]))
    url = urljoin(base_url, '/'.join(['card'])) # MAJOR HACK
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgImage)

    img.save(os.path.join(base_path, card_id + ".svg"))
