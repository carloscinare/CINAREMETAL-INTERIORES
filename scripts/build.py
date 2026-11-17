"""Build the static CINARÉ pages from approved product data."""
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://carloscinare.github.io/CINAREMETAL-INTERIORES/"
VERSION = "20261117-2"
PRODUCTS = json.loads((ROOT / "produtos.json").read_text())
IMAGES = json.loads((ROOT / "imagens/manifest.json").read_text())
BY_ID = {p["id"]: p for p in PRODUCTS}
GENERAL = "https://wa.me/351913591464?text=" + quote("Olá! Gostaria de pedir um orçamento para um projeto por medida.")
PATHS = {
    "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z"/>',
    "share": '<path d="M12 15V3m-4 4 4-4 4 4M5 12v8h14v-8"/>',
    "zoom": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5M10.5 7.5v6m-3-3h6"/>',
    "arrow": '<path d="M5 19 19 5M5 5h14v14"/>',
    "right": '<path d="M4 12h16m-6-6 6 6-6 6"/>',
    "chat": '<path d="M21 11.5a8.5 8.5 0 0 1-12.6 7.4L3 21l1.8-5.7A8.5 8.5 0 1 1 21 11.5Z"/><path d="M8 9.5h8M8 13h5"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
}


def icon(name):
    return '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + PATHS[name] + '</svg>'


def image(ident, prefix="./", sizes="(max-width: 560px) calc(100vw - 36px), (max-width: 800px) 46vw, 380px", eager=False, alt=None):
    item = IMAGES[ident]
    variant = next((v for v in item["variants"] if v["width"] >= 640), item["variants"][-1])
    srcset = ", ".join(prefix + v["path"] + " " + str(v["width"]) + "w" for v in item["variants"])
    title = BY_ID.get(ident, {}).get("name", "Portão em metal e madeira")
    priority = ' fetchpriority="high"' if eager else ''
    return f'<img src="{prefix + variant["path"]}" srcset="{srcset}" sizes="{escape(sizes, quote=True)}" width="{item["width"]}" height="{item["height"]}" alt="{escape(alt or title + " — visualização ilustrativa", quote=True)}" loading="{"eager" if eager else "lazy"}" decoding="async"{priority}>'


def product_url(p, prefix="./"):
    return prefix + "modelos/" + p["id"] + ".html"


def request_url(ident="", prefix="./"):
    return prefix + "orcamento.html" + ("?modelo=" + quote(ident) if ident else "")


def direct_whatsapp(p):
    return "https://wa.me/351913591464?text=" + quote("Olá! Gostaria de pedir um orçamento para: " + p["name"] + ".")


def head(title, description, path, prefix="./", image_id="mesa-centro", noindex=False):
    social = IMAGES[image_id]["social"]
    canonical = BASE + path
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ''
    return f'''<!doctype html>
<html lang="pt-PT"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#10191c"><title>{escape(title)}</title>
<meta name="description" content="{escape(description, quote=True)}">{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_PT">
<meta property="og:site_name" content="CINARÉ Metal &amp; Interiores">
<meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE + social['path']}">
<meta property="og:image:width" content="{social['width']}"><meta property="og:image:height" content="{social['height']}">
<meta property="og:image:alt" content="{escape(BY_ID.get(image_id, {}).get('name', 'Portão em metal e madeira') + ' — visualização ilustrativa', quote=True)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title, quote=True)}"><meta name="twitter:image" content="{BASE + social['path']}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}site.css?v={VERSION}"><link rel="stylesheet" href="{prefix}features.css?v={VERSION}">
<script src="{prefix}catalogo.js?v={VERSION}" defer></script><script src="{prefix}app.js?v={VERSION}" defer></script>
</head>'''


def header(prefix="./", page=""):
    home = "#" if page == "home" else prefix + "index.html#"
    current = ' aria-current="page"' if page in ("catalog", "product") else ''
    return f'''<a class="skip-link" href="#conteudo">Saltar para o conteúdo</a>
<header class="site-header"><div class="wrap nav">
<a class="brand" href="{home}inicio" aria-label="CINARÉ Metal e Interiores — início"><strong>CINARÉ</strong><span>Metal &amp; Interiores</span></a>
<button class="menu-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="site-menu" aria-label="Abrir menu">{icon('menu')}Menu</button>
<nav class="site-menu" id="site-menu" aria-label="Navegação principal">
<a href="{prefix}mobiliario-industrial.html"{current}>Mobiliário</a><a href="{home}servicos">Por medida</a><a href="{home}processo">Como encomendar</a>
<a href="{home}perguntas">Perguntas</a><a class="favorites-nav" href="{prefix}favoritos.html">{icon('heart')}Favoritos <span class="favorite-count" data-favorite-count hidden>0</span></a>
<a class="mobile-quote btn btn-gold" href="{request_url(prefix=prefix)}">Pedir orçamento {icon('arrow')}</a></nav>
<a class="header-quote btn btn-gold" href="{request_url(prefix=prefix)}">Pedir orçamento {icon('arrow')}</a>
</div></header>'''


def footer(prefix="./"):
    return f'''<footer class="site-footer"><div class="wrap footer-grid">
<div><span class="footer-title">CINARÉ Metal &amp; Interiores</span>Barcelos · Portugal</div>
<nav class="footer-links" aria-label="Navegação do rodapé"><a href="{prefix}mobiliario-industrial.html">Mobiliário</a><a href="{prefix}favoritos.html">Favoritos</a><a href="{request_url(prefix=prefix)}">Pedir orçamento</a><a href="{GENERAL}">WhatsApp</a></nav><div>© 2026 CINARÉ</div>
</div></footer><a class="whatsapp-float" href="{GENERAL}" aria-label="Falar com a CINARÉ pelo WhatsApp">{icon('chat')}<span>WhatsApp</span></a>'''


def tools(p, text=False):
    name = escape(p["name"], quote=True)
    css = "btn btn-outline" if text else "icon-button"
    label = '<span data-favorite-label>Guardar favorito</span>' if text else ''
    share = '<span>Partilhar</span>' if text else ''
    return f'''<button class="{css} favorite-toggle" type="button" data-favorite="{p['id']}" aria-pressed="false" aria-label="Guardar {name} nos favoritos" hidden>{icon('heart')}{label}</button>
<button class="{css}" type="button" data-share="{p['id']}" aria-label="Partilhar {name}" hidden>{icon('share')}{share}</button>'''


def card(p, prefix="./", ident_prefix="", eager=False):
    return f'''<article class="product-card" id="{ident_prefix + p['id']}" data-product="{p['id']}" data-category="{p['category']}">
<div class="product-media"><a class="product-photo" href="{product_url(p, prefix)}" aria-label="Ver {escape(p['name'], quote=True)}">{image(p['id'], prefix, eager=eager)}</a><div class="product-tools">{tools(p)}</div></div>
<div class="product-copy"><span class="product-category">{escape(p['categoryLabel'])}</span><h3><a href="{product_url(p, prefix)}">{escape(p['name'])}</a></h3>
<p class="product-description">{escape(p['description'])}</p><p class="product-material">{escape(p['material'])} · Por medida</p>
<div class="product-actions"><a class="btn btn-dark" href="{request_url(p['id'], prefix)}">Pedir orçamento {icon('arrow')}</a><a class="text-link" href="{product_url(p, prefix)}">Ver peça {icon('right')}</a></div></div></article>'''


def dialogs():
    return '''<div class="site-announcement" role="status" aria-live="polite" aria-atomic="true" data-announcement></div>
<dialog class="share-dialog" id="share-dialog" aria-labelledby="share-title"><div class="dialog-top"><h2 id="share-title">Partilhar peça</h2><button class="dialog-close" type="button" data-close-share aria-label="Fechar partilha">×</button></div>
<p>Envia esta peça a alguém ou guarda a ligação para mais tarde.</p><label for="share-url">Ligação da peça</label><div class="copy-row"><input id="share-url" readonly type="url" spellcheck="false"><button class="btn btn-dark" type="button" data-copy-share>Copiar</button></div>
<div class="share-actions"><button class="btn btn-outline" type="button" data-native-share hidden>Partilhar no dispositivo</button><a class="btn btn-outline" id="share-whatsapp" target="_blank" rel="noopener noreferrer">Partilhar no WhatsApp</a></div><p class="share-status" role="status" data-share-status></p></dialog>
<dialog class="zoom-dialog" id="zoom-dialog" aria-labelledby="zoom-title" aria-describedby="zoom-help"><div class="zoom-toolbar"><h2 id="zoom-title">Imagem da peça</h2><div class="zoom-controls"><button type="button" data-zoom-out aria-label="Reduzir imagem">−</button><output data-zoom-level aria-live="polite">100%</output><button type="button" data-zoom-in aria-label="Ampliar imagem">+</button><button type="button" data-zoom-reset>Repor</button><button type="button" data-close-zoom aria-label="Fechar ampliação">×</button></div></div>
<div class="zoom-stage" data-zoom-stage><img id="zoom-image" alt="" draggable="false"><p class="zoom-loading" role="status" data-zoom-loading>A carregar imagem…</p></div>
<div class="zoom-footer"><p id="zoom-help">Usa + e −, a roda do rato ou dois dedos para ampliar. Arrasta a imagem para explorar os detalhes.</p><a class="text-link" id="zoom-original" target="_blank" rel="noopener">Ver imagem original</a></div></dialog>'''


def page(title, description, path, body, prefix="./", kind="", image_id="mesa-centro", noindex=False):
    return head(title, description, path, prefix, image_id, noindex) + f'<body data-page="{kind}" data-root="{prefix}">' + header(prefix, kind) + body + footer(prefix) + dialogs() + '</body></html>\n'


def home():
    template = (ROOT / "templates/inicio.html").read_text()
    body = re.search(r'<main\b[\s\S]*?</main>', template).group(0)
    featured = ['mesa-centro', 'consola-industrial', 'estante-industrial', 'banco-sapateira']
    replacement = '<div class="featured-grid">' + ''.join(card(BY_ID[i], ident_prefix='destaque-') for i in featured) + '</div>\n      '
    body = re.sub(r'<div class="featured-grid">[\s\S]*?(?=<div class="section-bottom">)', lambda _: replacement, body)
    body = re.sub(r'<img\b[^>]*src="\./mesa-centro\.png"[^>]*>', lambda _: image('mesa-centro', eager=True, sizes='(max-width: 800px) 90vw, 600px'), body)
    body = re.sub(r'<img\b[^>]*src="\./portao-metal-madeira-77cf45df\.png"[^>]*>', lambda _: image('portao-metal-madeira', sizes='(max-width: 800px) 90vw, 600px'), body)
    def request_anchor(match):
        label = match.group(2)
        ident = 'portao-metal-madeira' if 'portão' in label else ''
        return '<a ' + match.group(1) + 'href="' + request_url(ident) + '">' + label.replace(' pelo WhatsApp', '') + '</a>'
    body = re.sub(r'<a ([^>]*?)href="https://wa\.me/351913591464[^"<>]*">([^<]*Pedir orçamento[^<]*)</a>', request_anchor, body)
    body = body.replace('↗', icon('arrow')).replace('→', icon('right'))
    return page('CINARÉ — Mobiliário industrial e projetos por medida', 'Mobiliário industrial e soluções em metal e madeira à tua medida. Descobre os modelos e prepara o pedido de orçamento pelo WhatsApp.', '', body, kind='home')


def catalog():
    filters = [('todos', 'Todos os modelos'), ('mesas', 'Mesas e consolas'), ('bancos', 'Bancos'), ('arrumacao', 'Arrumação'), ('decoracao', 'Decoração')]
    controls = ''.join(f'<button class="filter-btn" type="button" data-filter="{ident}" aria-pressed="{str(ident == "todos").lower()}" aria-controls="catalog-grid">{label}</button>' for ident, label in filters)
    body = f'''<main id="conteudo"><section class="catalog-hero dark"><div class="wrap"><nav class="breadcrumb" aria-label="Localização na página"><a href="./index.html">Início</a><span aria-hidden="true">/</span><span aria-current="page">Mobiliário</span></nav><span class="eyebrow">A coleção CINARÉ</span><h1>Escolhe a ideia.<br>Faz dela a tua peça.</h1><p class="lead">Descobre os detalhes de cada modelo, guarda os teus favoritos e prepara o teu pedido de orçamento. As imagens são visualizações ilustrativas para personalizar contigo.</p></div></section>
<section class="catalog-section" aria-label="Modelos de mobiliário"><div class="wrap"><div class="catalog-toolbar"><div class="filters" role="group" aria-label="Filtrar modelos por categoria" data-js hidden>{controls}</div><p class="catalog-count" aria-live="polite" aria-atomic="true"><span data-count>9</span> <span data-count-label>modelos</span></p></div>
<div class="catalog-grid" id="catalog-grid">{''.join(card(p, eager=i < 3) for i, p in enumerate(PRODUCTS))}</div><p class="catalog-note">Imagens ilustrativas. Os materiais, as dimensões, os acabamentos e a viabilidade de cada proposta são confirmados no orçamento. <a class="text-link" href="./orcamento.html">Conta-nos a tua ideia {icon('right')}</a></p></div></section></main>'''
    return page('Mobiliário industrial por medida — CINARÉ', 'Explora nove modelos em metal e madeira, guarda favoritos e prepara o pedido de orçamento para a tua peça CINARÉ.', 'mobiliario-industrial.html', body, kind='catalog')


def model(p):
    prefix = '../'
    related = ''.join(card(BY_ID[i], prefix, 'relacionado-') for i in p['related'])
    body = f'''<main id="conteudo"><section class="product-section"><div class="wrap"><nav class="breadcrumb light-breadcrumb" aria-label="Localização na página"><a href="../index.html">Início</a><span aria-hidden="true">/</span><a href="../mobiliario-industrial.html">Mobiliário</a><span aria-hidden="true">/</span><span aria-current="page">{escape(p['name'])}</span></nav>
<div class="product-detail-grid"><figure class="product-detail-visual"><a class="detail-image" href="{prefix + p['source']}" data-zoom="{p['id']}" aria-label="Ampliar imagem: {escape(p['name'], quote=True)}">{image(p['id'], prefix, sizes='(max-width: 800px) 94vw, 650px', eager=True)}</a><figcaption><span>Visualização ilustrativa · Projeto por medida</span><a class="text-link" href="{prefix + p['source']}" data-zoom="{p['id']}">{icon('zoom')}Ampliar imagem</a></figcaption></figure>
<div class="product-detail-copy"><span class="eyebrow">{escape(p['categoryLabel'])}</span><h1>{escape(p['name'])}</h1><p class="detail-lead">{escape(p['description'])}</p><p>{escape(p['details'])}</p>
<dl class="product-specs"><div><dt>Materiais da proposta</dt><dd>{escape(p['material'])}</dd></div><div><dt>Personalização</dt><dd>Medidas, cor e acabamento a combinar.</dd></div><div><dt>Preço e prazo</dt><dd>Definidos no orçamento para a tua peça.</dd></div></dl>
<a class="btn btn-dark product-request" href="{request_url(p['id'], prefix)}">Pedir orçamento desta peça {icon('arrow')}</a><p class="request-hint">Indica as tuas preferências e revê a mensagem antes de continuar no WhatsApp.</p><div class="detail-tools">{tools(p, True)}</div><a class="text-link direct-contact" href="{direct_whatsapp(p)}">Falar diretamente pelo WhatsApp {icon('arrow')}</a></div></div></div></section>
<section class="section related-section" aria-labelledby="related-title"><div class="wrap"><div class="section-heading"><div><span class="eyebrow">Mais ideias para o teu espaço</span><h2 id="related-title">Também pode interessar-te.</h2></div><a class="text-link" href="../mobiliario-industrial.html">Ver todos os modelos {icon('right')}</a></div><div class="catalog-grid related-grid">{related}</div></div></section></main>'''
    return page(p['name'] + ' por medida — CINARÉ', p['description'] + ' Descobre os detalhes e pede orçamento com as medidas e o acabamento que procuras.', 'modelos/' + p['id'] + '.html', body, prefix, 'product', p['id'])


def favorites():
    body = '''<main id="conteudo"><section class="catalog-hero dark"><div class="wrap"><span class="eyebrow">A tua seleção</span><h1>As peças que guardaste.</h1><p class="lead">Volta às tuas ideias favoritas e escolhe a peça para o teu próximo pedido. A seleção fica guardada neste navegador.</p></div></section>
<section class="section"><div class="wrap"><h2 class="sr-only" tabindex="-1" id="favorites-title">Os teus favoritos</h2><p class="small" data-favorites-count aria-live="polite"></p><div class="catalog-grid" data-favorites-grid></div><div class="empty-favorites" data-favorites-empty><span class="empty-mark" aria-hidden="true"><svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z"/></svg></span><h2>A tua próxima ideia está na coleção.</h2><p>Usa o coração nas peças de que gostas para as encontrares aqui.</p><a class="btn btn-dark" href="./mobiliario-industrial.html">Explorar os modelos</a></div><noscript><p>Para guardar favoritos neste navegador, ativa o JavaScript. Podes continuar a consultar todas as peças no catálogo.</p></noscript></div></section></main>'''
    return page('Os teus favoritos — CINARÉ', 'A tua seleção de modelos de mobiliário industrial CINARÉ, guardada neste navegador.', 'favoritos.html', body, kind='favorites', noindex=True)


def quotation():
    options = ''.join(f'<option value="{p["id"]}">{escape(p["name"])}</option>' for p in PRODUCTS)
    dimensions = ''.join(f'''<div class="form-field"><label for="quote-{ident}">{label} <span>(cm)</span></label><input id="quote-{ident}" name="{ident}" type="text" inputmode="decimal" maxlength="8" placeholder="Opcional" aria-describedby="{ident}-error"><span class="field-error" id="{ident}-error" hidden>Indica um número positivo, por exemplo 80 ou 80,5.</span></div>''' for ident, label in [('width', 'Largura'), ('depth', 'Profundidade'), ('height', 'Altura')])
    body = f'''<main id="conteudo"><section class="quote-intro dark"><div class="wrap"><span class="eyebrow">O primeiro passo para a tua peça</span><h1>Conta-nos o que tens em mente.</h1><p class="lead">Escolhe uma peça, indica as preferências que já tens e revê o pedido. Depois, continua a conversa no WhatsApp.</p></div></section>
<section class="quote-section"><div class="wrap quote-layout"><div class="quote-panel"><noscript><h2>Vamos falar da tua ideia?</h2><p>O pedido guiado precisa de JavaScript. Podes pedir orçamento diretamente pelo WhatsApp.</p><a class="btn btn-dark" href="{GENERAL}">Abrir WhatsApp</a></noscript>
<form id="quote-form" novalidate hidden><ol class="quote-progress" aria-label="Etapas do pedido"><li data-step-label="0" aria-current="step"><span>1</span>A peça</li><li data-step-label="1"><span>2</span>Preferências</li><li data-step-label="2"><span>3</span>Rever e enviar</li></ol><p class="sr-only" role="status" aria-live="polite" data-step-status>Passo 1 de 3</p>
<fieldset data-quote-step="0"><legend tabindex="-1">Qual é a tua ideia?</legend><p>Podes partir de um modelo da coleção ou de um projeto por medida.</p><div class="form-field"><label for="quote-model">Modelo ou projeto</label><select id="quote-model" name="model"><option value="projeto-por-medida">Ainda estou a definir a minha ideia</option><optgroup label="Mobiliário da coleção">{options}</optgroup><optgroup label="Outros projetos"><option value="portao-metal-madeira">Portão em metal e madeira</option><option value="projeto-personalizado">Outro projeto por medida</option></optgroup></select></div><p class="form-note">Não precisas de ter tudo decidido para começar.</p></fieldset>
<fieldset data-quote-step="1"><legend tabindex="-1">À medida do teu espaço.</legend><p>Estas informações são opcionais. Indica apenas o que já souberes.</p><div class="dimensions-grid">{dimensions}</div><label class="checkbox-label"><input type="checkbox" id="quote-help" name="needsHelp">Preciso de ajuda para definir as medidas</label><div class="form-field"><label for="quote-finish">Acabamento pretendido <span>(opcional)</span></label><input type="text" id="quote-finish" name="finish" maxlength="160" placeholder="Ex.: metal preto e madeira em tom natural"></div><p class="form-note">As medidas finais, os materiais e os acabamentos são confirmados na proposta.</p></fieldset>
<fieldset data-quote-step="2"><legend tabindex="-1">Revê o teu pedido.</legend><div class="form-field"><label for="quote-city">Localidade <span>(opcional)</span></label><input id="quote-city" name="city" type="text" maxlength="100" autocomplete="address-level2" placeholder="Para combinar levantamento ou entrega"></div><div class="form-field"><label for="quote-notes">O que mais devemos saber? <span>(opcional)</span></label><textarea id="quote-notes" name="notes" rows="3" maxlength="1000" placeholder="Fala-nos do espaço, da utilização ou da tua ideia."></textarea></div><details class="quote-preview" open><summary>Mensagem que vais levar para o WhatsApp</summary><textarea id="quote-message" readonly rows="8" aria-label="Resumo do pedido para o WhatsApp"></textarea></details><a class="btn btn-dark quote-send" id="quote-whatsapp" href="{GENERAL}" target="_blank" rel="noopener noreferrer">Continuar no WhatsApp {icon('arrow')}</a><p class="form-note" id="quote-send-note">Ao continuar, os dados que preencheste abrem numa mensagem no WhatsApp. Confirma o envio nessa aplicação.</p></fieldset>
<div class="quote-navigation"><button class="btn btn-outline" type="button" data-quote-back hidden>Voltar</button><button class="btn btn-dark" type="button" data-quote-next>Continuar {icon('right')}</button></div></form>
<div class="quote-direct"><span>Preferes começar por uma conversa?</span><a class="text-link" id="quote-direct" href="{GENERAL}">Falar diretamente pelo WhatsApp {icon('arrow')}</a></div></div>
<aside class="quote-aside" aria-labelledby="quote-aside-title"><span class="eyebrow">O teu ponto de partida</span><figure class="quote-model-visual" data-quote-product hidden><img id="quote-model-image" alt="" width="640" height="480"></figure><h2 id="quote-aside-title" data-quote-model>Um projeto teu.</h2><p data-quote-model-description>Partilha a tua ideia. A solução, o preço e o prazo são definidos contigo no orçamento.</p><ul><li>Medidas e acabamentos a combinar</li><li>Pedido direto para a CINARÉ</li><li>WhatsApp: +351 913 591 464</li></ul><a class="text-link" data-quote-model-link href="./mobiliario-industrial.html">Explorar os modelos {icon('right')}</a></aside></div></section></main>'''
    return page('Pedir orçamento por medida — CINARÉ', 'Prepara o teu pedido de orçamento CINARÉ: modelo, medidas opcionais, acabamento e localidade. Revê a mensagem e continua pelo WhatsApp.', 'orcamento.html', body, kind='quote')


def write(path, content):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')


client_products = []
for p in PRODUCTS:
    item = dict(p)
    item['image'] = IMAGES[p['id']]
    item['url'] = BASE + 'modelos/' + p['id'] + '.html'
    client_products.append(item)
project = {'id': 'portao-metal-madeira', 'name': 'Portão em metal e madeira', 'description': 'Uma proposta para a entrada da tua casa, com dimensões e acabamentos a combinar.', 'image': IMAGES['portao-metal-madeira'], 'url': BASE + '#servicos'}
write('catalogo.js', 'window.CinareProducts = ' + json.dumps(client_products, ensure_ascii=False) + ';\nwindow.CinareProjects = ' + json.dumps([project], ensure_ascii=False) + ';\n')
write('index.html', home())
write('mobiliario-industrial.html', catalog())
write('favoritos.html', favorites())
write('orcamento.html', quotation())
for p in PRODUCTS:
    write('modelos/' + p['id'] + '.html', model(p))
urls = ['', 'mobiliario-industrial.html', 'orcamento.html'] + ['modelos/' + p['id'] + '.html' for p in PRODUCTS]
write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>' + BASE + url + '</loc></url>' for url in urls) + '</urlset>\n')
write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: ' + BASE + 'sitemap.xml\n')
print('Built homepage, catalog, favorites, guided quotation and nine product pages')
