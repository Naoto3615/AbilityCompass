from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def t(context, kanji_text, hiragana_text):
    """Return kanji_text or hiragana_text based on the session's text_mode.

    Usage in templates:
        {% load text_mode %}
        {% t "漢字テキスト" "ひらがなてきすと" %}
    """
    request = context.get('request')
    mode = 'hiragana'
    if request:
        mode = request.session.get('text_mode', 'hiragana')
    return kanji_text if mode == 'kanji' else hiragana_text


# ─── アバター レンダリング ────────────────────────────────────────────────────

SKIN_COLORS = {
    'light': '#FFDAB9',
    'medium': '#D2956C',
    'dark': '#8B4513',
}

HAIR_COLORS = {
    'black': '#1a1a1a',
    'brown': '#8B4513',
    'blonde': '#FFD700',
    'gray': '#808080',
}

DEFAULT_AVATAR_CONFIG = {
    'skin': 'light',
    'hair_style': 'short',
    'hair_color': 'black',
    'eye_type': 'normal',
    'accessory': 'none',
    'job_outfit': 'none',
    'expression': 'happy',
    'badge_count': 0,
    'rosy_cheeks': False,
}


@register.inclusion_tag('components/avatar.html')
def render_avatar(config, size=120):
    """SVGアバターを描画するインクルージョンタグ。

    Usage:
        {% load text_mode %}
        {% render_avatar profile.avatar_config %}
        {% render_avatar profile.avatar_config size=80 %}
    """
    cfg = dict(DEFAULT_AVATAR_CONFIG)
    if isinstance(config, dict):
        cfg.update(config)

    return {
        'cfg': cfg,
        'size': size,
        'skin_color': SKIN_COLORS.get(cfg['skin'], SKIN_COLORS['light']),
        'hair_color': HAIR_COLORS.get(cfg['hair_color'], HAIR_COLORS['black']),
    }
