from pathlib import Path
from PIL import Image

pairs = [
    ('galeria/consola-industrial-nova.webp', 'galeria/consola-industrial-nova.jpg'),
    ('galeria/estante-industrial.webp', 'galeria/estante-industrial.jpg'),
    ('galeria/mesa-apoio-nova.webp', 'galeria/mesa-apoio-nova.jpg'),
    ('galeria/suporte-planta.webp', 'galeria/suporte-planta.jpg'),
    ('galeria/prateleira-parede-nova.webp', 'galeria/prateleira-parede-nova.jpg'),
    ('galeria/porta-revistas.webp', 'galeria/porta-revistas.jpg'),
    ('galeria/banco-sapateira-novo.webp', 'galeria/banco-sapateira-novo.jpg'),
    ('galeria/banco-alto-novo.webp', 'galeria/banco-alto-novo.jpg'),
]

for src_name, dst_name in pairs:
    img = Image.open(src_name).convert('RGB')
    img.save(dst_name, 'JPEG', quality=92, optimize=True, progressive=True)

page = Path('mobiliario-industrial.html')
html = page.read_text(encoding='utf-8')
for src_name, dst_name in pairs:
    html = html.replace('./' + src_name + '?v=1', './' + dst_name + '?v=2')
    html = html.replace('./' + src_name, './' + dst_name)
page.write_text(html, encoding='utf-8')
