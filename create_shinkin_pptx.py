#!/usr/bin/env python3
"""東濃信用金庫 提案資料 PPTX生成スクリプト"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Pt
import copy

# ──────────────────────────────────────────────
# カラー定義
# ──────────────────────────────────────────────
C_NAVY   = RGBColor(0x0f, 0x17, 0x2a)   # 背景
C_GREEN  = RGBColor(0x10, 0xb9, 0x81)   # アクセント1
C_BLUE   = RGBColor(0x3b, 0x82, 0xf6)   # アクセント2
C_WHITE  = RGBColor(0xf8, 0xfa, 0xfc)   # テキスト
C_GRAY   = RGBColor(0x94, 0xa3, 0xb8)   # サブテキスト
C_CARD   = RGBColor(0x1e, 0x29, 0x3b)   # カード背景
C_RED    = RGBColor(0xef, 0x44, 0x44)   # 強調赤
C_DARK   = RGBColor(0x07, 0x0c, 0x17)   # 深いネイビー

# スライドサイズ (16:9 ワイドスクリーン)
SLIDE_W = Cm(33.867)
SLIDE_H = Cm(19.05)


def new_prs():
    prs = Presentation()
    prs.slide_width  = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def add_notes(slide, notes_text):
    """プレゼンターノート（ナレーション原稿）をスライドに追加する"""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text


def add_blank_slide(prs):
    blank_layout = prs.slide_layouts[6]  # 完全空白
    return prs.slides.add_slide(blank_layout)


def set_bg(slide, color=C_NAVY):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, left, top, width, height, fill_color=None, line_color=None, line_width=Pt(0)):
    from pptx.util import Pt
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        left, top, width, height
    )
    shape.line.width = line_width
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
    else:
        shape.line.fill.background()
    return shape


def add_textbox(slide, left, top, width, height, text, font_size=Pt(14),
                bold=False, color=C_WHITE, align=PP_ALIGN.LEFT,
                wrap=True, font_name=None):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = font_size
    run.font.bold = bold
    run.font.color.rgb = color
    if font_name:
        run.font.name = font_name
    return txBox


def add_para(tf, text, font_size=Pt(13), bold=False, color=C_WHITE,
             align=PP_ALIGN.LEFT, space_before=Pt(4), font_name=None):
    p = tf.add_paragraph()
    p.alignment = align
    p.space_before = space_before
    run = p.add_run()
    run.text = text
    run.font.size = font_size
    run.font.bold = bold
    run.font.color.rgb = color
    if font_name:
        run.font.name = font_name
    return p


def badge(slide, left, top, text, bg_color=C_GREEN):
    w, h = Cm(10), Cm(0.7)
    rect = add_rect(slide, left, top, w, h, fill_color=bg_color)
    tf = rect.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = text
    run.font.size = Pt(10)
    run.font.bold = True
    run.font.color.rgb = C_WHITE


def accent_bar(slide, top, color=C_GREEN):
    add_rect(slide, Cm(0), top, SLIDE_W, Cm(0.08), fill_color=color)


# ──────────────────────────────────────────────
# スライド1：表紙
# ──────────────────────────────────────────────
def slide1(prs):
    sl = add_blank_slide(prs)
    set_bg(sl)

    # グラデーション風の装飾帯（上）
    add_rect(sl, Cm(0), Cm(0), SLIDE_W, Cm(0.5), fill_color=C_GREEN)

    # バッジ
    badge(sl, Cm(2), Cm(1.2), "東濃信用金庫様 ご提案資料", bg_color=C_GREEN)

    # メインタイトル
    add_textbox(sl, Cm(2), Cm(3.0), Cm(29), Cm(3.5),
                "AI × 福祉 × 教育",
                font_size=Pt(54), bold=True, color=C_WHITE, align=PP_ALIGN.LEFT)

    # アクセントライン
    add_rect(sl, Cm(2), Cm(7.0), Cm(6), Cm(0.12), fill_color=C_GREEN)

    # サブタイトル
    add_textbox(sl, Cm(2), Cm(7.4), Cm(29), Cm(1.5),
                "多治見から始まる、地域共生社会のイノベーション",
                font_size=Pt(18), bold=False, color=C_GRAY, align=PP_ALIGN.LEFT)

    # 組織名
    add_textbox(sl, Cm(2), Cm(9.4), Cm(29), Cm(1.2),
                "特定非営利活動法人 思いやりの糸 / HIローズ",
                font_size=Pt(13), bold=False, color=C_GRAY, align=PP_ALIGN.LEFT)

    # 装飾：右側グリッド風
    for i in range(5):
        x = Cm(24) + Cm(i * 1.8)
        add_rect(sl, x, Cm(11), Cm(1.4), Cm(7.5),
                 fill_color=RGBColor(0x1e, 0x29, 0x3b))

    # 底部帯
    add_rect(sl, Cm(0), Cm(18.4), SLIDE_W, Cm(0.65), fill_color=C_DARK)

    add_notes(sl,
        "本日はお時間をいただきありがとうございます。\n"
        "私は「ステップアップナビ」というAIを活用した福祉支援アプリを開発しております、廣瀬と申します。\n"
        "多治見から、地域の課題をテクノロジーで解決する取り組みを始めております。\n"
        "本日は東濃信用金庫様にご支援のご相談にまいりました。どうぞよろしくお願いいたします。"
    )


# ──────────────────────────────────────────────
# スライド2：開発の背景とビジョン
# ──────────────────────────────────────────────
def slide2(prs):
    sl = add_blank_slide(prs)
    set_bg(sl)
    add_rect(sl, Cm(0), Cm(0), SLIDE_W, Cm(0.5), fill_color=C_GREEN)

    # スライドタイトル
    add_textbox(sl, Cm(2), Cm(0.8), Cm(29), Cm(1.2),
                "開発の背景とビジョン",
                font_size=Pt(28), bold=True, color=C_WHITE)
    accent_bar(sl, Cm(2.1))

    # 見出し
    add_textbox(sl, Cm(2), Cm(2.5), Cm(29), Cm(1.0),
                "「愛」と「現場」から生まれた技術",
                font_size=Pt(20), bold=True, color=C_GREEN)

    # 本文カード
    card = add_rect(sl, Cm(2), Cm(3.8), Cm(21), Cm(8.5), fill_color=C_CARD)
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = (
        "既存のシステムにはない、障がいを持つ当事者の家族（お父さんエンジニア）が\n"
        "開発するからこそ到達できる、究極の使いやすさと自立支援を目指します。\n\n"
        "7月〜9月の3ヶ月間、失業保険を活用しながらフルコミットし、\n"
        "娘のため、そして地域のために命がけで形にします。"
    )
    run.font.size = Pt(14)
    run.font.color.rgb = C_WHITE

    # 強調バッジ
    add_rect(sl, Cm(24.5), Cm(5), Cm(7), Cm(4.5), fill_color=C_GREEN)
    add_textbox(sl, Cm(24.5), Cm(5.5), Cm(7), Cm(1.5),
                "60%", font_size=Pt(42), bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_textbox(sl, Cm(24.5), Cm(7.5), Cm(7), Cm(1.5),
                "コアプログラム\n完成済み",
                font_size=Pt(13), bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

    add_rect(sl, Cm(0), Cm(18.4), SLIDE_W, Cm(0.65), fill_color=C_DARK)

    add_notes(sl,
        "このアプリを作ろうと思ったのは、私自身が障がいを持つ娘の父親だからです。\n"
        "既存の支援ツールは、現場の当事者目線が欠けていることが多い。\n"
        "だからこそ、「使う人の気持ちが分かるエンジニア」が作るべきだと感じました。\n"
        "7月から9月の3ヶ月間、失業給付を活用しながら、この開発にフルコミットする覚悟です。\n"
        "コアとなるプログラムはすでに60%完成しており、残りの仕上げに向けて資金が必要な状況です。"
    )


# ──────────────────────────────────────────────
# スライド3：AIプログラムの区分
# ──────────────────────────────────────────────
def slide3(prs):
    sl = add_blank_slide(prs)
    set_bg(sl)
    add_rect(sl, Cm(0), Cm(0), SLIDE_W, Cm(0.5), fill_color=C_GREEN)

    add_textbox(sl, Cm(2), Cm(0.8), Cm(29), Cm(1.2),
                "目的・対象に応じたAIプログラムの区分分け",
                font_size=Pt(24), bold=True, color=C_WHITE)
    accent_bar(sl, Cm(2.1))

    cards = [
        ("①", "本人・家族", "QOLの向上と将来への安心"),
        ("②", "福祉事業所", "現場DXによる支援の質向上"),
        ("③", "児童・保護者", "遊びを通じた早期の自己成長"),
        ("④", "教育・行政", "地域モデル確立と政策的な連携"),
    ]

    card_w = Cm(7.3)
    for i, (num, title, desc) in enumerate(cards):
        x = Cm(2) + i * Cm(7.8)
        y = Cm(3.2)

        card = add_rect(sl, x, y, card_w, Cm(10), fill_color=C_CARD)

        # 番号バッジ
        nb = add_rect(sl, x + Cm(0.3), y + Cm(0.4), Cm(1.2), Cm(1.2), fill_color=C_GREEN)
        tf = nb.text_frame
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = num
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = C_WHITE

        add_textbox(sl, x + Cm(0.3), y + Cm(1.9), card_w - Cm(0.6), Cm(1.4),
                    title, font_size=Pt(17), bold=True, color=C_WHITE)
        add_textbox(sl, x + Cm(0.3), y + Cm(3.5), card_w - Cm(0.6), Cm(3.0),
                    desc, font_size=Pt(13), color=C_GRAY, wrap=True)

    add_rect(sl, Cm(0), Cm(18.4), SLIDE_W, Cm(0.65), fill_color=C_DARK)

    add_notes(sl,
        "このアプリは、大きく4つの対象に向けたプログラムで構成されています。\n"
        "一つ目は障がいを持つ本人とそのご家族。二つ目は福祉事業所の支援員・職員の方々。\n"
        "三つ目は発達に課題のあるお子さんとその保護者。四つ目は学校や行政機関です。\n"
        "それぞれの立場に合わせたAI機能を提供することで、地域全体の支援力を高めることを目指しています。"
    )


# ──────────────────────────────────────────────
# スライド4：区分①大人向け
# ──────────────────────────────────────────────
def slide4(prs):
    sl = add_blank_slide(prs)
    set_bg(sl)
    add_rect(sl, Cm(0), Cm(0), SLIDE_W, Cm(0.5), fill_color=C_GREEN)

    badge(sl, Cm(2), Cm(0.9), "区分① 大人向け", bg_color=C_GREEN)

    add_textbox(sl, Cm(2), Cm(2.0), Cm(29), Cm(1.2),
                "障がい者本人・ご家族向けプログラム",
                font_size=Pt(26), bold=True, color=C_WHITE)
    accent_bar(sl, Cm(3.3))

    add_textbox(sl, Cm(2), Cm(3.7), Cm(29), Cm(1.0),
                "「我慢する毎日から、自分で未来を選ぶ毎日へ」",
                font_size=Pt(16), bold=True, color=C_GREEN)

    items = [
        ("自律的な学習支援",
         "AIがその日の体調や気分を察知し、最適な「自己トレーニングメニュー」を提案。\n成功体験を積み重ね、自信を育みます。"),
        ("家族の不安を安心に",
         "本人の「できた！」をリアルタイムに視覚化。\n「親がいなくなってもこの子は大丈夫」と思える未来のお守りに。"),
    ]
    for i, (head, body) in enumerate(items):
        y = Cm(5.2) + i * Cm(5.5)
        card = add_rect(sl, Cm(2), y, Cm(29), Cm(4.8), fill_color=C_CARD)
        add_rect(sl, Cm(2), y, Cm(0.2), Cm(4.8), fill_color=C_GREEN)

        add_textbox(sl, Cm(2.6), y + Cm(0.4), Cm(28), Cm(1.0),
                    "● " + head, font_size=Pt(16), bold=True, color=C_GREEN)
        add_textbox(sl, Cm(2.6), y + Cm(1.5), Cm(28), Cm(2.8),
                    body, font_size=Pt(13), color=C_WHITE, wrap=True)

    add_rect(sl, Cm(0), Cm(18.4), SLIDE_W, Cm(0.65), fill_color=C_DARK)

    add_notes(sl,
        "区分①は、軽度知的障害などを持つ大人の方とそのご家族向けです。\n"
        "AIがその日の体調や気分を察知し、無理のない自己トレーニングメニューを提案します。\n"
        "小さな成功体験を積み重ねることで自信を育み、就労への第一歩を後押しします。\n"
        "また、本人の「できた！」という記録をリアルタイムで可視化することで、\n"
        "ご家族の「この子は大丈夫だろうか」という不安を安心に変えます。"
    )


# ──────────────────────────────────────────────
# スライド5：区分②福祉事業所向け
# ──────────────────────────────────────────────
def slide5(prs):
    sl = add_blank_slide(prs)
    set_bg(sl)
    add_rect(sl, Cm(0), Cm(0), SLIDE_W, Cm(0.5), fill_color=C_GREEN)

    badge(sl, Cm(2), Cm(0.9), "区分② 福祉事業所向け", bg_color=C_BLUE)

    add_textbox(sl, Cm(2), Cm(2.0), Cm(29), Cm(1.2),
                "福祉事業所・職員向けプログラム",
                font_size=Pt(26), bold=True, color=C_WHITE)
    accent_bar(sl, Cm(3.3), color=C_BLUE)

    add_textbox(sl, Cm(2), Cm(3.7), Cm(29), Cm(1.0),
                "「事務作業をゼロにして、100%の愛を子どもたちへ」",
                font_size=Pt(16), bold=True, color=C_BLUE)

    items = [
        ("現場の書類仕事を自動化",
         "音声入力や日々のデータから、AIがプロ仕様の支援記録や報告書を秒速で自動作成。\n残業を大幅削減。"),
        ("データ駆動型の支援",
         "経験則だけに頼らず、AIによる客観的な行動データ分析に基づいた、\nより質の高い個別支援計画の策定をサポート。"),
    ]
    for i, (head, body) in enumerate(items):
        y = Cm(5.2) + i * Cm(5.5)
        card = add_rect(sl, Cm(2), y, Cm(29), Cm(4.8), fill_color=C_CARD)
        add_rect(sl, Cm(2), y, Cm(0.2), Cm(4.8), fill_color=C_BLUE)

        add_textbox(sl, Cm(2.6), y + Cm(0.4), Cm(28), Cm(1.0),
                    "● " + head, font_size=Pt(16), bold=True, color=C_BLUE)
        add_textbox(sl, Cm(2.6), y + Cm(1.5), Cm(28), Cm(2.8),
                    body, font_size=Pt(13), color=C_WHITE, wrap=True)

    add_rect(sl, Cm(0), Cm(18.4), SLIDE_W, Cm(0.65), fill_color=C_DARK)

    add_notes(sl,
        "区分②は、福祉事業所で働く支援員・職員の方々向けです。\n"
        "現場では日々の支援記録や報告書作成に多くの時間が取られています。\n"
        "AIが音声入力や日々のデータをもとに、これらの書類を自動作成します。\n"
        "残業を大幅に減らし、職員が子どもたちと向き合う時間を最大化することが目標です。\n"
        "また、AIによる行動データ分析で、経験則だけに頼らない質の高い支援計画の策定をサポートします。"
    )


# ──────────────────────────────────────────────
# スライド6：区分③ 児童・保護者向け
# ──────────────────────────────────────────────
def slide_b(prs):
    sl = add_blank_slide(prs)
    set_bg(sl)
    add_rect(sl, Cm(0), Cm(0), SLIDE_W, Cm(0.5), fill_color=C_GREEN)

    badge(sl, Cm(2), Cm(0.9), "区分③ 児童・保護者向け", bg_color=C_GREEN)

    add_textbox(sl, Cm(2), Cm(2.0), Cm(29), Cm(1.2),
                "児童・保護者向けプログラム",
                font_size=Pt(26), bold=True, color=C_WHITE)
    accent_bar(sl, Cm(3.3))

    add_textbox(sl, Cm(2), Cm(3.7), Cm(29), Cm(1.0),
                "「遊びながら、自分の「好き」と「得意」を見つける旅へ」",
                font_size=Pt(16), bold=True, color=C_GREEN)

    items = [
        ("ゲーム感覚の自己発見",
         "AIとの対話や楽しいミッションを通じて、子ども自身が自分の興味・強みを自然に言語化。\n親が気づけなかった才能の発見にも。"),
        ("保護者の「一人で抱え込まない」を実現",
         "AIが日々の記録から学習し、「今日試してみてほしいこと」を保護者にそっとアドバイス。\n孤独な子育てを、チームでのサポートに。"),
    ]
    for i, (head, body) in enumerate(items):
        y = Cm(5.2) + i * Cm(5.5)
        card = add_rect(sl, Cm(2), y, Cm(29), Cm(4.8), fill_color=C_CARD)
        add_rect(sl, Cm(2), y, Cm(0.2), Cm(4.8), fill_color=C_GREEN)

        add_textbox(sl, Cm(2.6), y + Cm(0.4), Cm(28), Cm(1.0),
                    "● " + head, font_size=Pt(16), bold=True, color=C_GREEN)
        add_textbox(sl, Cm(2.6), y + Cm(1.5), Cm(28), Cm(2.8),
                    body, font_size=Pt(13), color=C_WHITE, wrap=True)

    add_rect(sl, Cm(0), Cm(18.4), SLIDE_W, Cm(0.65), fill_color=C_DARK)

    add_notes(sl,
        "区分③は、発達に特性のあるお子さんとその保護者向けです。\n"
        "ゲーム感覚のミッションや対話を通じて、子ども自身が自分の「好き」と「得意」を自然に見つけていきます。\n"
        "親御さんが気づいていなかった才能が見つかることもあります。\n"
        "また、AIが日々の記録から学習し、保護者に「今日試してみてほしいこと」をそっとアドバイスします。\n"
        "一人で抱え込みがちな子育ての不安を、チームでのサポートに変えていきます。"
    )


# ──────────────────────────────────────────────
# スライド7：区分④ 教育・行政向け
# ──────────────────────────────────────────────
def slide_c(prs):
    sl = add_blank_slide(prs)
    set_bg(sl)
    add_rect(sl, Cm(0), Cm(0), SLIDE_W, Cm(0.5), fill_color=C_GREEN)

    badge(sl, Cm(2), Cm(0.9), "区分④ 教育・行政向け", bg_color=C_GREEN)

    add_textbox(sl, Cm(2), Cm(2.0), Cm(29), Cm(1.2),
                "教育機関・行政向けプログラム",
                font_size=Pt(26), bold=True, color=C_WHITE)
    accent_bar(sl, Cm(3.3))

    add_textbox(sl, Cm(2), Cm(3.7), Cm(29), Cm(1.0),
                "「データで語る、多治見モデルを全国へ」",
                font_size=Pt(16), bold=True, color=C_GREEN)

    items = [
        ("地域全体の支援データを可視化",
         "匿名化された支援実績・就労データをダッシュボードで一元管理。\n福祉政策の立案に活用できる「エビデンス」を提供。"),
        ("全国展開への橋渡し",
         "多治見で実証されたモデルをパッケージ化し、他自治体へのライセンス展開を目指します。\n東濃信用金庫様との連携実績が全国への説得力に。"),
    ]
    for i, (head, body) in enumerate(items):
        y = Cm(5.2) + i * Cm(5.5)
        card = add_rect(sl, Cm(2), y, Cm(29), Cm(4.8), fill_color=C_CARD)
        add_rect(sl, Cm(2), y, Cm(0.2), Cm(4.8), fill_color=C_GREEN)

        add_textbox(sl, Cm(2.6), y + Cm(0.4), Cm(28), Cm(1.0),
                    "● " + head, font_size=Pt(16), bold=True, color=C_GREEN)
        add_textbox(sl, Cm(2.6), y + Cm(1.5), Cm(28), Cm(2.8),
                    body, font_size=Pt(13), color=C_WHITE, wrap=True)

    add_rect(sl, Cm(0), Cm(18.4), SLIDE_W, Cm(0.65), fill_color=C_DARK)

    add_notes(sl,
        "区分④は、学校や行政機関向けです。\n"
        "個々の支援データを匿名化してダッシュボードで一元管理し、地域全体の支援状況を可視化します。\n"
        "これにより、「感覚」ではなく「データ」で語れる福祉政策の立案が可能になります。\n"
        "そして、多治見で実証されたモデルをパッケージ化し、全国の他自治体へ展開することを目指します。\n"
        "東濃信用金庫様との連携実績は、他自治体への展開における大きな説得力になると考えています。"
    )


# ──────────────────────────────────────────────
# スライド（新）：東濃信用金庫様へのご提案
# ──────────────────────────────────────────────
def slide6(prs):
    sl = add_blank_slide(prs)
    set_bg(sl)
    add_rect(sl, Cm(0), Cm(0), SLIDE_W, Cm(0.5), fill_color=C_BLUE)

    badge(sl, Cm(2), Cm(0.9), "東濃信用金庫様へのご提案", bg_color=C_BLUE)

    add_textbox(sl, Cm(2), Cm(2.0), Cm(29), Cm(1.2),
                "地域の未来を、一緒に作りませんか",
                font_size=Pt(28), bold=True, color=C_WHITE)
    accent_bar(sl, Cm(3.3), color=C_BLUE)

    add_textbox(sl, Cm(2), Cm(3.7), Cm(20), Cm(0.9),
                "スポンサーとしてご参画いただくと",
                font_size=Pt(16), bold=True, color=C_BLUE)

    bullets = [
        "Readyforクラウドファンディングの手数料（通常8%）が無料に",
        "300万円の目標なら約24万円のコスト削減",
        "多治見発・地域貢献の先進事例として信金の名前を全国に発信",
        "地元企業・住民・福祉事業所との信頼関係構築",
    ]
    for i, b in enumerate(bullets):
        y = Cm(4.9) + i * Cm(1.55)
        add_rect(sl, Cm(2), y + Cm(0.3), Cm(0.35), Cm(0.35), fill_color=C_GREEN)
        add_textbox(sl, Cm(2.7), y, Cm(20), Cm(1.4),
                    b, font_size=Pt(14), color=C_WHITE)

    # 強調カード
    card = add_rect(sl, Cm(24), Cm(4.5), Cm(8), Cm(7), fill_color=C_BLUE)
    add_textbox(sl, Cm(24), Cm(5.5), Cm(8), Cm(1.5),
                "¥240,000", font_size=Pt(32), bold=True,
                color=C_WHITE, align=PP_ALIGN.CENTER)
    add_textbox(sl, Cm(24), Cm(7.5), Cm(8), Cm(1.5),
                "削減できる手数料", font_size=Pt(14), bold=True,
                color=C_WHITE, align=PP_ALIGN.CENTER)

    add_rect(sl, Cm(0), Cm(18.4), SLIDE_W, Cm(0.65), fill_color=C_DARK)

    add_notes(sl,
        "ここで、東濃信用金庫様への具体的なご提案です。\n"
        "Readyforには、信用金庫がパートナーとして参画することで、クラウドファンディングの手数料が無料になる制度があります。\n"
        "通常、目標金額の8%が手数料としてかかります。300万円の目標であれば、約24万円です。\n"
        "東濃信用金庫様にパートナーとしてご参画いただければ、この24万円が丸ごとプロジェクトに活きることになります。\n"
        "地域の信用金庫として福祉DXを支援するという、社会貢献とPRを兼ねた取り組みになります。"
    )


# ──────────────────────────────────────────────
# スライド7：スポンサー参画のメリット
# ──────────────────────────────────────────────
def slide7(prs):
    sl = add_blank_slide(prs)
    set_bg(sl)
    add_rect(sl, Cm(0), Cm(0), SLIDE_W, Cm(0.5), fill_color=C_BLUE)

    badge(sl, Cm(2), Cm(0.9), "東濃信用金庫様限定", bg_color=C_BLUE)

    add_textbox(sl, Cm(2), Cm(2.0), Cm(29), Cm(1.2),
                "スポンサー参画のメリット",
                font_size=Pt(28), bold=True, color=C_WHITE)
    accent_bar(sl, Cm(3.3), color=C_BLUE)

    merits = [
        ("ブランド価値", "地域福祉DXのパイオニアとして\nメディア・SNSで発信"),
        ("地域連携", "福祉事業所・保護者・行政との\nネットワーク強化"),
        ("PR効果", "アプリ内・クラファンページ・\n広報資料への信金名掲載"),
        ("社会貢献", "軽度知的障害者の就労支援という\nESG・CSRへの貢献"),
    ]

    card_w = Cm(7.3)
    for i, (title, desc) in enumerate(merits):
        x = Cm(2) + i * Cm(7.8)
        y = Cm(4.0)
        card = add_rect(sl, x, y, card_w, Cm(9.5), fill_color=C_CARD)
        add_rect(sl, x, y, card_w, Cm(0.3), fill_color=C_BLUE)

        add_textbox(sl, x + Cm(0.4), y + Cm(0.7), card_w - Cm(0.8), Cm(1.2),
                    title, font_size=Pt(17), bold=True, color=C_BLUE)
        add_textbox(sl, x + Cm(0.4), y + Cm(2.2), card_w - Cm(0.8), Cm(5.0),
                    desc, font_size=Pt(13), color=C_WHITE, wrap=True)

    add_rect(sl, Cm(0), Cm(18.4), SLIDE_W, Cm(0.65), fill_color=C_DARK)

    add_notes(sl,
        "スポンサーとしてご参画いただくことで、ブランド価値・地域連携・PR効果・社会貢献という4つのメリットがあります。\n"
        "福祉DXのパイオニアとして、東濃信用金庫様のお名前をメディアやSNSで広く発信いたします。\n"
        "また、福祉事業所・保護者・行政機関との新たなネットワーク構築にもつながります。\n"
        "ESG・CSRの観点からも、地域社会への貢献として高く評価されるご取り組みになると考えています。"
    )


# ──────────────────────────────────────────────
# スライド8：Readyforパートナーシップ
# ──────────────────────────────────────────────
def slide8(prs):
    sl = add_blank_slide(prs)
    set_bg(sl)
    add_rect(sl, Cm(0), Cm(0), SLIDE_W, Cm(0.5), fill_color=C_BLUE)

    badge(sl, Cm(2), Cm(0.9), "制度のご説明", bg_color=C_BLUE)

    add_textbox(sl, Cm(2), Cm(2.0), Cm(29), Cm(1.2),
                "Readyfor × 信用金庫パートナープログラム",
                font_size=Pt(26), bold=True, color=C_WHITE)
    accent_bar(sl, Cm(3.3), color=C_BLUE)

    # 左ブロック（赤）
    left = add_rect(sl, Cm(2), Cm(4.5), Cm(13.5), Cm(9), fill_color=C_CARD)
    add_rect(sl, Cm(2), Cm(4.5), Cm(13.5), Cm(0.35), fill_color=C_RED)

    add_textbox(sl, Cm(2.5), Cm(5.1), Cm(12.5), Cm(1.0),
                "通常のクラウドファンディング",
                font_size=Pt(16), bold=True, color=C_RED)
    add_textbox(sl, Cm(2.5), Cm(6.4), Cm(12.5), Cm(0.9),
                "手数料：目標金額の 8%",
                font_size=Pt(14), color=C_WHITE)
    add_textbox(sl, Cm(2.5), Cm(7.6), Cm(12.5), Cm(0.9),
                "300万円達成で 約24万円",
                font_size=Pt(14), color=C_WHITE)

    # 右ブロック（青）
    right = add_rect(sl, Cm(18), Cm(4.5), Cm(13.5), Cm(9), fill_color=C_CARD)
    add_rect(sl, Cm(18), Cm(4.5), Cm(13.5), Cm(0.35), fill_color=C_BLUE)

    add_textbox(sl, Cm(18.5), Cm(5.1), Cm(12.5), Cm(1.0),
                "信用金庫パートナー参画後",
                font_size=Pt(16), bold=True, color=C_BLUE)
    add_textbox(sl, Cm(18.5), Cm(6.4), Cm(12.5), Cm(0.9),
                "手数料：0円（無料）",
                font_size=Pt(14), color=C_WHITE)
    add_textbox(sl, Cm(18.5), Cm(7.6), Cm(12.5), Cm(0.9),
                "支援者から集まった全額がプロジェクトに",
                font_size=Pt(14), color=C_WHITE)

    # 矢印
    add_textbox(sl, Cm(15.2), Cm(7.5), Cm(3), Cm(2.0),
                "→", font_size=Pt(42), bold=True, color=C_GREEN, align=PP_ALIGN.CENTER)

    add_rect(sl, Cm(0), Cm(18.4), SLIDE_W, Cm(0.65), fill_color=C_DARK)

    add_notes(sl,
        "こちらが制度の概要です。\n"
        "左側が通常のクラウドファンディングで、目標金額の8%が手数料としてかかります。\n"
        "一方、右側のように東濃信用金庫様にパートナーとしてご参画いただくと、手数料が0円になります。\n"
        "支援者から集まった全額がそのままプロジェクトに活かされる仕組みです。\n"
        "この制度はReadyforと信用金庫が連携することで成立する、大変有利な制度です。"
    )


# ──────────────────────────────────────────────
# スライドA：クラウドファンディング 300万円の根拠
# ──────────────────────────────────────────────
def slide_a(prs):
    sl = add_blank_slide(prs)
    set_bg(sl)
    add_rect(sl, Cm(0), Cm(0), SLIDE_W, Cm(0.5), fill_color=C_GREEN)

    badge(sl, Cm(2), Cm(0.9), "資金使途", bg_color=C_GREEN)

    add_textbox(sl, Cm(2), Cm(2.0), Cm(29), Cm(1.2),
                "クラウドファンディング 300万円の根拠",
                font_size=Pt(26), bold=True, color=C_WHITE)
    accent_bar(sl, Cm(3.3))

    # メインメッセージ（大きく・エメラルドグリーン）
    add_textbox(sl, Cm(2), Cm(3.7), Cm(29), Cm(1.5),
                "エンジニア単価 80万円/月 × 3ヶ月 = 240万円 ＋ 運営費60万円 = 合計300万円",
                font_size=Pt(30), bold=True, color=C_GREEN, align=PP_ALIGN.CENTER)

    # 説明文
    add_textbox(sl, Cm(2), Cm(5.4), Cm(29), Cm(1.1),
                "AI×福祉領域の専門エンジニアとして3ヶ月間フルコミット。失業給付期間を活用し、娘のため・地域のために命がけで開発します。",
                font_size=Pt(12), bold=False, color=C_GRAY, align=PP_ALIGN.CENTER, wrap=True)

    # テーブルデータ（項目・金額・内容）
    rows = [
        ("開発人件費（80万×3ヶ月）",         "240万円", "設計・実装・テスト・リリース・保守"),
        ("広報・PR費",                        " 18万円", "SNS広告、プレスリリース、チラシ制作"),
        ("サーバー・インフラ費（3年分）",      " 15万円", "Railway, PostgreSQL, ドメイン等"),
        ("デザイン・UX制作費",                " 12万円", "UI改善、アイコン、動画制作"),
        ("イベント・説明会開催費",             "  9万円", "福祉事業所向け説明会、デモ展示"),
        ("福祉事業所導入サポート費",           "  6万円", "初期研修・マニュアル・問い合わせ対応"),
    ]

    table_x = Cm(2)
    row_h   = Cm(1.35)
    row_top = Cm(6.9)

    # ヘッダー行
    header_bg = add_rect(sl, table_x, row_top - Cm(0.55), Cm(29.5), Cm(0.55), fill_color=C_GREEN)
    tf = header_bg.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = "  項目                               金額            内容"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = C_WHITE

    for idx, (label, amount, detail) in enumerate(rows):
        y = row_top + idx * row_h
        bg_color = C_CARD if idx % 2 == 0 else RGBColor(0x16, 0x21, 0x32)
        add_rect(sl, table_x, y, Cm(29.5), row_h - Cm(0.05), fill_color=bg_color)
        add_rect(sl, table_x, y, Cm(0.18), row_h - Cm(0.05), fill_color=C_GREEN)

        add_textbox(sl, table_x + Cm(0.5), y + Cm(0.15), Cm(12), Cm(1.0),
                    label, font_size=Pt(12), color=C_WHITE)
        add_textbox(sl, table_x + Cm(12.8), y + Cm(0.15), Cm(3.5), Cm(1.0),
                    amount, font_size=Pt(12), bold=True, color=C_GREEN, align=PP_ALIGN.RIGHT)
        add_textbox(sl, table_x + Cm(17.0), y + Cm(0.15), Cm(12), Cm(1.0),
                    detail, font_size=Pt(11), color=C_GRAY)

    # 合計行
    total_y = row_top + len(rows) * row_h + Cm(0.1)
    add_rect(sl, table_x, total_y, Cm(29.5), row_h - Cm(0.05), fill_color=C_GREEN)
    add_textbox(sl, table_x + Cm(0.5), total_y + Cm(0.15), Cm(12), Cm(1.0),
                "合計", font_size=Pt(13), bold=True, color=C_WHITE)
    add_textbox(sl, table_x + Cm(12.8), total_y + Cm(0.15), Cm(3.5), Cm(1.0),
                "300万円", font_size=Pt(13), bold=True, color=C_WHITE, align=PP_ALIGN.RIGHT)

    # 補足テキスト（小さく）
    footnote_y = total_y + row_h + Cm(0.15)
    add_textbox(sl, Cm(2), footnote_y, Cm(29.5), Cm(0.7),
                "※フリーランスエンジニアの市場単価：月60〜120万円が相場。AI×福祉の専門性を持つエンジニアは希少。",
                font_size=Pt(10), bold=False, color=C_GRAY, align=PP_ALIGN.LEFT, wrap=True)
    add_textbox(sl, Cm(2), footnote_y + Cm(0.75), Cm(29.5), Cm(0.7),
                "※広報費はクラウドファンディング達成後の認知拡大・事業者向け展開に活用。",
                font_size=Pt(10), bold=False, color=C_GRAY, align=PP_ALIGN.LEFT, wrap=True)

    add_rect(sl, Cm(0), Cm(18.4), SLIDE_W, Cm(0.65), fill_color=C_DARK)

    add_notes(sl,
        "こちらが資金の使い道です。\n"
        "エンジニア単価80万円×3ヶ月の開発人件費が240万円、サーバーや広報などの運営費が60万円、合計300万円が必要な資金です。\n"
        "AI×福祉領域の専門エンジニアとして、3ヶ月間フルコミットでこのプロジェクトに取り組みます。\n"
        "失業給付期間を最大限に活用し、娘のため、そして地域の皆さんのために開発に専念する計画です。"
    )


# ──────────────────────────────────────────────
# スライド12：締めくくり
# ──────────────────────────────────────────────
def slide9(prs):
    sl = add_blank_slide(prs)
    set_bg(sl)
    add_rect(sl, Cm(0), Cm(0), SLIDE_W, Cm(0.5), fill_color=C_GREEN)

    # タイトル
    add_textbox(sl, Cm(2), Cm(1.5), Cm(29), Cm(2.0),
                "「共犯者」になってくれませんか？",
                font_size=Pt(34), bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

    # アクセントライン
    add_rect(sl, Cm(12), Cm(4.0), Cm(10), Cm(0.12), fill_color=C_GREEN)

    # 本文カード
    card = add_rect(sl, Cm(3), Cm(4.6), Cm(27.5), Cm(7.5), fill_color=C_CARD)
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = (
        "一人の父の愛が、何万人の「自立」を支えるインフラに変わる。\n\n"
        "まず一度、お話しを聞いていただけますか。\n\n"
        "多治見の子どもたちと、はたらく大人のために。"
    )
    run.font.size = Pt(16)
    run.font.color.rgb = C_WHITE

    # 組織情報
    add_textbox(sl, Cm(2), Cm(13.5), Cm(29), Cm(1.0),
                "特定非営利活動法人 思いやりの糸 / HIローズ",
                font_size=Pt(13), color=C_GRAY, align=PP_ALIGN.CENTER)
    add_textbox(sl, Cm(2), Cm(14.5), Cm(29), Cm(1.0),
                "代表 廣瀬 豊",
                font_size=Pt(13), color=C_GRAY, align=PP_ALIGN.CENTER)

    add_rect(sl, Cm(0), Cm(18.4), SLIDE_W, Cm(0.65), fill_color=C_DARK)

    add_notes(sl,
        "最後に、一言お伝えさせてください。\n"
        "これは一人の父が、娘のために始めたプロジェクトです。\n"
        "しかし、このアプリが完成すれば、多治見だけでなく全国の何万人もの方の自立を支えるインフラになり得ます。\n"
        "東濃信用金庫様にも、この「共犯者」になっていただけませんか。\n"
        "ぜひ一度、詳しいお話しを聞いていただけますと幸いです。本日はありがとうございました。"
    )


# ──────────────────────────────────────────────
# メイン
# ──────────────────────────────────────────────
def main():
    prs = new_prs()

    slide1(prs)   # 1. 表紙
    slide2(prs)   # 2. 開発の背景とビジョン
    slide3(prs)   # 3. AIプログラム区分
    slide4(prs)   # 4. 区分① 大人向け
    slide5(prs)   # 5. 区分② 福祉事業所向け
    slide_b(prs)  # 6. 区分③ 児童・保護者向け（新規）
    slide_c(prs)  # 7. 区分④ 教育・行政向け（新規）
    slide6(prs)   # 8. 東濃信用金庫様へのご提案
    slide7(prs)   # 9. スポンサー参画のメリット
    slide8(prs)   # 10. Readyforパートナーシップ
    slide_a(prs)  # 11. 300万円の使途内訳（新規）
    slide9(prs)   # 12. 締めくくり

    output = "/Users/matsunaganaoto/Desktop/projects/App/東濃信用金庫_提案資料.pptx"
    prs.save(output)
    print(f"✅ 生成完了: {output}")


if __name__ == "__main__":
    main()
