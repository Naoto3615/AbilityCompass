from django import template
from functools import lru_cache

register = template.Library()


@lru_cache(maxsize=2048)
def to_hiragana(text: str) -> str:
    """漢字テキストをひらがなに変換する（結果はLRUキャッシュで保持）。

    pykakasi を使って変換し、単語間にスペースを入れて読みやすくする。
    """
    try:
        import pykakasi
        kks = pykakasi.kakasi()
        result = kks.convert(text)
        parts = []
        for item in result:
            hira = item.get('hira') or item.get('orig', '')
            parts.append(hira)
        return ''.join(parts)
    except Exception:
        return text


@register.simple_tag(takes_context=True)
def t(context, kanji_text, hiragana_text=None):
    """テキストモードに応じて漢字またはひらがなを返す。

    第2引数を省略すると pykakasi で自動変換する。

    Usage in templates:
        {% load text_mode %}
        {% t "診断を受ける" %}                          ← 自動変換
        {% t "診断を受ける" "しんだんを うける" %}        ← 手動指定（優先）
    """
    request = context.get('request')
    mode = 'hiragana'
    if request:
        mode = request.session.get('text_mode', 'hiragana')

    if mode == 'kanji':
        return kanji_text

    # ひらがなモード: 手動指定があればそちらを優先
    if hiragana_text is not None:
        return hiragana_text

    return to_hiragana(kanji_text)


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
