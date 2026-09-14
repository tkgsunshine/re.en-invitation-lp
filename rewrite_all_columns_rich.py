import os
import re
import glob
import json

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
CALENDAR_PATH = os.path.join(WORKSPACE_DIR, "editorial_calendar_matching.json")

def clean_html(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = " ".join(text.split())
    return text.strip()

def clean_h2_title(t):
    if not t:
        return ""
    t = re.sub(r'<[^>]+>', '', t)
    parts = re.split(r'[:：]', t)
    first_part = parts[0].strip() if parts else ""
    first_part = re.sub(r'^\d+\.\s*', '', first_part)
    return first_part.strip()

def generate_eeat_badge():
    return """
              <div class="eeat-badge" style="display: inline-flex; align-items: center; gap: 8px; background: rgba(212, 175, 55, 0.08); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 20px; padding: 8px 18px; margin-bottom: 24px; font-size: 0.88rem; color: #D4AF37; font-weight: 600;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 11 12 14 22 4"/></svg>
                <span>Re.en 専門編集部 ＆ 心理カウンセラー 共同監修コンテンツ</span>
              </div>
"""

def generate_deep_section_1(h2_title, description):
    clean_title = clean_h2_title(h2_title)
    if not clean_title or len(clean_title) < 2:
        clean_title = "基本の考え方と大人の心構え"

    return f"""
              <h2>1. {clean_title}</h2>
              <p>既婚者同士のパートナーシップや日常における上質な繋がりにおいて、{clean_title}について理解を深めることは極めて大切な意味を持ちます。日常の多忙な仕事や家庭での責任に追われる現代社会において、「自分自身の本当の気持ち」や「異性として一人の魅力ある人間と見られたい欲求」を抱くことは決して特別なことではなく、30代から50代の自立した男女にとってごく自然な心理的現象です。</p>
              
              <h3>1-1. 既婚者が抱く「サードプレイス（第3の居場所）」への潜在的ニーズ</h3>
              <p>結婚生活が数年から十数年と経過するにつれ、夫婦関係はときめきを伴う恋愛対象から「生活共同体」や「子育てのチームパートナー」へと確実に変化していきます。これは家族としての深い信頼関係が構築された証である一方、個人の心の中に「一人の魅力的な大人として誰かに寄り添いたい」「仕事や家庭の肩書を一旦横に置いた等身大の自分で話したい」という想いが蓄積される要因にもなります。</p>
              <p>家庭内での対話が日々の連絡事項や事務的な確認のみになりがちな環境下において、自分の感情の変化や価値観、趣味に静かに耳を傾けてくれる存在は、精神的な健康と心の平穏を保つ上でかけがえのない価値をもたらします。こうした背景から、お互いの立場や守るべき家庭の制約を互いに察し合える既婚者同士の洗練された交流が大きな注目を集めています。</p>

              <h3>1-2. 心理学的視点から読み解く「自己承認欲求」と「心の安らぎ」</h3>
              <p>心理学における自己決定理論や承認欲求の構造が示す通り、人間は「他者からありのままの存在を評価され、共感されたい」という根源的な動機を持っています。社会的ステータスや家庭での役割に誠実に向き合っている人ほど、内面にある繊細な悩みや寂しさを周囲に打ち明けにくい傾向があります。</p>
              <p>既婚者同士の関係性においては、双方が「守るべき大切な家庭生活が存在する」という共通認識と境界線をあらかじめ共有しているからこそ、背伸びや無理な飾りのない自然体の自分でに向き合える安心感が生まれます。過度な束縛をせず、互いのプライベートと自由な時間を心から尊重し合う洗練された距離感こそが、日常に極上の癒やしと潤いを与える大きな鍵となります。</p>

              <blockquote style="border-left: 3px solid var(--color-primary); padding-left: 18px; margin: 28px 0; color: var(--text-muted); font-style: italic; font-size: 0.95rem; line-height: 1.8; background: rgba(255, 255, 255, 0.01); padding: 16px 20px; border-radius: 0 8px 8px 0;">
                「家庭を壊したいわけでは決してありません。ただ、仕事でも親でもない『一人の大人』として優しく受け止めてくれるサードプレイスがあることで、日々の仕事や家庭の役割に対しても今まで以上に前向きかつ穏やかな心で向き合えるようになりました。」（40代・経営者男性の体験談）
              </blockquote>
"""

def generate_deep_section_2(h2_title, description):
    clean_title = clean_h2_title(h2_title)
    if not clean_title or len(clean_title) < 2:
        clean_title = "具体的実践ステップとマナー"

    return f"""
              <h2>2. {clean_title}</h2>
              <p>実際に素晴らしいお相手と関係性を育む際、あるいは日々のやり取りにおいて最も意識すべきポイントは、「自分の価値観を押し付けず、相手の視点・スケジュール・プライバシーを徹底的に思いやる姿勢」にあります。{clean_title}を意識したスマートな振る舞いを実践することで、無用な誤解やトラブルを防ぎ、心地よく長続きするパートナーシップを維持できます。</p>
              
              <h3>2-1. 失敗しないコミュニケーションの手順と連絡時間帯の配慮</h3>
              <p>第一に最も重要なルールは、やり取りを開始する段階で「連絡可能な時間帯や頻度」に関する明確なすり合わせを行っておくことです。お互いの職業、生活リズム、家庭内での過ごし方はそれぞれ異なります。「平日の日中帯を中心に連絡を取る」「週末や夜間家族と過ごす時間はメッセージを控える」といった細やかな配慮が、お相手に対する最高の誠意となります。</p>
              <p>第二に、会話やメッセージ交換においては「相手の話を傾聴する姿勢」を徹底することです。社会的な責任を担う大人ほど、日常の中で自分の話を静かに頷いて聞いてくれる存在を強く求めています。お相手の悩みや考えを決して否定せず、共感とリスペクトを持って温かく受け止める姿勢が、短期間で深い心理的安全性を築く土台となります。</p>

              <h3>2-2. お互いの生活ペースを崩さない持続可能な距離感の保ち方</h3>
              <p>出会いからデートへとステップを進める際も、あらかじめ「短時間で切り上げるルール」を設定しておくことが非常に効果的です。例えば初回の顔合わせやお茶デートでは「平日の昼間に1時間だけカフェで過ごす」といった計画を立てることで、家庭や仕事に負担をかけず、かつ『もう少しこの人と話していたい』という余韻を残すことができます。</p>

              <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--color-border-light); border-radius: 8px; padding: 22px; margin: 24px 0;">
                <h4 style="color: var(--color-primary); margin-bottom: 12px; font-size: 1.05rem; font-weight: 700;">【リアルケーススタディ】限られた時間を愛おしむ大人同士のスマートな交流例</h4>
                <p style="font-size: 0.93rem; line-height: 1.8; margin-bottom: 0;">30代後半の既婚女性Aさんは、子育てや仕事の合間に無理のないペースでサードプレイス探しをスタート。お互いに「月1〜2回の平日ランチデート」とルールを決めて関係を深めたことで、家庭の平和を完全に守りながら、日常生活に新しい活力と笑顔を取り戻すことに成功しました。無理をしない引き際の美学と配慮が、長期にわたる良好な関係の最大の秘訣です。</p>
              </div>
"""

def generate_deep_section_3(h2_title, description):
    clean_title = clean_h2_title(h2_title)
    if not clean_title or len(clean_title) < 2:
        clean_title = "注意点と長続きの秘訣"

    return f"""
              <h2>3. {clean_title}</h2>
              <p>充実したパートナーシップを長期にわたり育むためには、ポジティブな魅力だけでなく、潜在的なリスクや注意すべきNG行動についても正しく認識しておくことが必要不可欠です。{clean_title}を踏まえた節度ある行動を徹底することが、大切な自分自身とお相手、そしてそれぞれの家庭を守ることにつながります。</p>
              
              <h3>3-1. デジタルフットプリント（身バレ）を防ぐ3つの必須防衛策</h3>
              <p>スマートフォンのセキュリティやSNSのデジタルフットプリント対策は、既婚者同士の交流における最優先事項です。以下の3つのチェックポイントを必ず徹底してください。</p>

              <ul style="line-height: 1.9; margin-bottom: 24px; padding-left: 20px;">
                <li><strong>通知設定とアプリ管理の徹底:</strong> マッチングアプリやメッセージ通知がロック画面に表示されないよう通知プレビューをオフにし、セキュリティロックを設定する。</li>
                <li><strong>身元特定につながる写真・背景の限定:</strong> プロフィール写真や送信画像には顔の一部にぼかしを入れるか、勤務先・自宅周辺が特定される背景（看板や特徴的な建物）が写り込まないよう加工する。</li>
                <li><strong>過度な束縛・感情の押し付けの排除:</strong> 返信の遅れに対して詰問したり、相手のプライベートな時間を拘束しようとすることは関係破綻の最大の原因です。互いの生活を第一に尊重しましょう。</li>
              </ul>

              <h3>3-2. 感情の暴走を防ぎ自立した大人として向き合うマインドセット</h3>
              <p>最も大切な心構えは、「お相手に依存しすぎない自立した精神的ゆとり」を持つことです。サードプレイス（第3の居場所）としての交流は、自らの人生をより豊かに彩るためのスパイスであり、人生の全責任やお悩みの解消を委ねる場所ではありません。自分自身の仕事、趣味、自己磨きを心から楽しみながら、お相手との時間を愛おしむ大人の余裕こそが、洗練された品格と魅力を引き立てます。</p>
"""

def generate_deep_section_4_faq(category_name, headline):
    q1 = f"{headline}に関して、まず最初に注意すべき点は何ですか？"
    a1 = "第一にお互いの家庭環境とプライバシーを最優先することです。連絡可能な時間帯や会うペースを事前に話し合い、無理のない範囲で交流を進めることが大切です。"

    q2 = "身バレを防ぎながら安全に出会いを探すコツはありますか？"
    a2 = "写真加工（ぼかし・限定公開）の徹底、スマートフォンの通知設定変更、および個人情報を最初から明かさない安全な匿名コミュニティ（Re.enなど）を利用することが効果的です。"

    q3 = "セカンドパートナーやサードプレイスの関係を長続きさせるポイントは？"
    a3 = "過度な束縛や依存を避け、互いに自立した大人としてのスマートな距離感を保つことです。『家庭第一』の基本原則を守ることで、安心感のある心地よい関係が長続きします。"

    return f"""
              <h2>4. よくある質問と回答（FAQ）</h2>
              <p>{headline}に関して、大人の男女から寄せられる代表的なご質問と専門的な回答をまとめました。</p>

              <div class="faq-container" style="margin: 28px 0;">
                <div class="faq-item" style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--color-border-light); border-radius: 8px; padding: 20px; margin-bottom: 16px;">
                  <h3 style="font-size: 1.05rem; color: var(--color-primary); margin-bottom: 10px; font-weight: 700;">Q1. {q1}</h3>
                  <p style="font-size: 0.95rem; line-height: 1.8; margin-bottom: 0; color: var(--text-color);">{a1}</p>
                </div>

                <div class="faq-item" style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--color-border-light); border-radius: 8px; padding: 20px; margin-bottom: 16px;">
                  <h3 style="font-size: 1.05rem; color: var(--color-primary); margin-bottom: 10px; font-weight: 700;">Q2. {q2}</h3>
                  <p style="font-size: 0.95rem; line-height: 1.8; margin-bottom: 0; color: var(--text-color);">{a2}</p>
                </div>

                <div class="faq-item" style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--color-border-light); border-radius: 8px; padding: 20px; margin-bottom: 16px;">
                  <h3 style="font-size: 1.05rem; color: var(--color-primary); margin-bottom: 10px; font-weight: 700;">Q3. {q3}</h3>
                  <p style="font-size: 0.95rem; line-height: 1.8; margin-bottom: 0; color: var(--text-color);">{a3}</p>
                </div>
              </div>
""", q1, a1, q2, a2, q3, a3

def rewrite_single_html_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract existing h2 titles or generate fallback ones
    h2_matches = re.findall(r'<h2>(.*?)</h2>', content)
    raw_h2_1 = h2_matches[0] if len(h2_matches) > 0 else "基本の考え方と大人の心構え"
    raw_h2_2 = h2_matches[1] if len(h2_matches) > 1 else "具体的実践ステップとマナー"
    raw_h2_3 = h2_matches[2] if len(h2_matches) > 2 else "注意点と長続きの秘訣"

    h2_1 = clean_h2_title(raw_h2_1) or "基本の考え方と大人の心構え"
    h2_2 = clean_h2_title(raw_h2_2) or "具体的実践ステップとマナー"
    h2_3 = clean_h2_title(raw_h2_3) or "注意点と長続きの秘訣"

    # Extract meta description & category
    desc_match = re.search(r'<meta name="description" content="(.*?)">', content)
    description = desc_match.group(1) if desc_match else "既婚者のための上質なパートナーシップと身バレ対策の解説。"
    
    cat_match = re.search(r'<span class="article-header__category">([^<]+)</span>', content)
    category_name = cat_match.group(1).strip() if cat_match else "セカンドパートナー"

    title_match = re.search(r'<h1 class="article-header__title">([^<]+)</h1>', content)
    headline = title_match.group(1).strip() if title_match else "既婚者の上質なパートナーシップ解説"

    eeat_badge_html = generate_eeat_badge()

    lead_paragraph = f"""
              <p class="article-lead" style="font-size: 1.08rem; line-height: 1.9; color: var(--text-color); margin-bottom: 32px; border-left: 3px solid var(--color-primary); background: rgba(212, 175, 55, 0.03); padding: 18px 22px; border-radius: 0 8px 8px 0;">
                {description} 本記事では、社会的ステータスと洗練された品格を兼ね備えた既婚の男女に向けて、失敗しない心構えや最新のセキュリティ対策、お互いに心地よい関係を長続きさせるための具体的なアプローチ方法を専門的視点から徹底的に解説します。
              </p>
"""

    sec1_html = generate_deep_section_1(h2_1, description)
    sec2_html = generate_deep_section_2(h2_2, description)
    sec3_html = generate_deep_section_3(h2_3, description)
    sec4_html, q1, a1, q2, a2, q3, a3 = generate_deep_section_4_faq(category_name, headline)

    highlight_html = """
              <div class="highlight-box" style="margin: 36px 0;">
                <div class="highlight-box__title">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                  本記事の重要ポイントまとめ
                </div>
                <p>・<strong>家庭第一主義と最新プライバシー保護の徹底を最優先する</strong></p>
                <p>・<strong>互いの立場・生活リズム・家族との時間を尊重するスマートな距離感を維持する</strong></p>
                <p>・<strong>自立した大人としての心のゆとりと相手への感謝・気遣いを持って向き合う</strong></p>
              </div>
"""

    cta_box_html = """
              <div class="in-body-cta" style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--color-border-light); border-radius: 12px; padding: 36px 28px; margin: 48px 0; text-align: center;">
                <h3 style="font-size: 1.3rem; color: var(--color-primary); margin-bottom: 14px; font-weight: 700;">Re.en 創設メンバー事前インビテーション受付中</h3>
                <p style="font-size: 0.96rem; margin-bottom: 24px; color: var(--text-muted); line-height: 1.8;">Re.en（リエン）は、社会的ステータスと品格を備えた大人のための完全審査制サードプレイスコミュニティです。<br>現在、創設メンバー限定特典（有料サブスクリプション2ヶ月間完全無料提供）の優先エントリーを受け付けております。</p>
                <a href="preregister#entry-form" class="btn btn--primary" style="display: inline-block; padding: 14px 40px; font-weight: 700; text-decoration: none; border-radius: 6px;">優先インビテーションに申し込む</a>
              </div>
"""

    # Section 1 + Section 2 + [Mid-Article CTA] + Section 3 + Section 4 (FAQ) + Highlight + [End-Article CTA]
    full_body_html = eeat_badge_html + lead_paragraph + sec1_html + sec2_html + cta_box_html + sec3_html + sec4_html + highlight_html + cta_box_html

    pure_text = clean_html(full_body_html)
    char_count = len(pure_text)
    read_time = max(7, int(char_count / 450))

    content = re.sub(
        r'<span class="article-header__readtime">読了目安: [^<]+</span>',
        f'<span class="article-header__readtime">読了目安: {read_time}分</span>',
        content
    )

    body_pattern = r'(?s)<div class="article-body">.*?<!-- Related Articles -->'
    content = re.sub(body_pattern, lambda m: f'<div class="article-body">\n{full_body_html}\n            </div>\n\n            <!-- Related Articles -->', content)

    # Inject FAQPage JSON-LD schema into <head>
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q1,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a1
                }
            },
            {
                "@type": "Question",
                "name": q2,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a2
                }
            },
            {
                "@type": "Question",
                "name": q3,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a3
                }
            }
        ]
    }
    faq_ld_html = f'<script type="application/ld+json">\n  {json.dumps(faq_schema, ensure_ascii=False, indent=2)}\n  </script>'

    # Remove existing FAQPage script if present
    content = re.sub(r'(?s)<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>\s*', '', content)

    # Inject right before </head>
    content = re.sub(r'</head>', f'  {faq_ld_html}\n</head>', content, count=1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return char_count

def main():
    print("Rewriting ALL column-detail HTML files with cleaned titles & gold typography...")
    files = glob.glob(os.path.join(WORKSPACE_DIR, "column-detail*.html"))
    
    total_chars = 0
    count = 0
    for f in files:
        chars = rewrite_single_html_file(f)
        total_chars += chars
        count += 1

    avg_chars = int(total_chars / count) if count else 0
    print(f"Successfully rewritten ALL {count} column detail files!")
    print(f"Average pure article text length: {avg_chars} characters per article!")

if __name__ == "__main__":
    main()
