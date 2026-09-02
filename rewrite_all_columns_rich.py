import os
import re
import glob
import json

WORKSPACE_DIR = "/Users/user/.gemini/antigravity/scratch/married-matching-lp"
CALENDAR_PATH = os.path.join(WORKSPACE_DIR, "editorial_calendar_matching.json")

def clean_html(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = " ".join(text.split())
    return text.strip()

def generate_deep_section_1(h2_title, description):
    return f"""
              <h2>{h2_title}</h2>
              <p>既婚者同士のパートナーシップや日常の繋がりにおいて、{h2_title}を理解することは極めて重要な意味を持ちます。日常の忙しさや家庭での役割に追われる中で、「自分自身の本音」や「異性としての承認」を求めるお気持ちは、決して特別なものではなく、多くの紳士淑女が抱く自然な感情です。</p>
              
              <h3>1-1. なぜ今この課題やテーマが注目されているのか</h3>
              <p>結婚生活が数年から十数年と経過するにつれ、夫婦関係は恋愛対象から「生活共同体」あるいは「子育てのパートナー」へと変化していきます。これは家族としての信頼が深まった証である一方、個人としてのときめきや、一人の魅力的で自立した人間として見られたいという欲求が満たされにくくなる側面を持っています。</p>
              <p>特に30代から50代の落ち着いた世代において、社会的ステータスや家庭の責任を果たしながらも、心の中に生まれた「小さな孤独感」や「誰かと深く共感し合いたいという想い」を大切にしたいと考える方が増えています。このような背景から、お互いの立場や制約を深く理解し合える既婚者同士の上質なコミュニケーションが注目を集めているのです。</p>

              <h3>1-2. 心理学的視点から見るお互いの期待と心の動き</h3>
              <p>人間には「他者に理解されたい」「自分の価値を承認されたい」という根源的な欲求（承認欲求・自己実現欲求）が存在します。家庭内での会話が日常の連絡事項のみになりがちな環境では、自分の内面や趣味、細やかな感情の変化に気づいてくれる存在が貴重になります。</p>
              <p>既婚者同士の関係性においては、お互いに「守るべき大切な家庭がある」という前提を共有しているからこそ、背伸びをしない等身大の自分で向き合える安心感があります。相手に依存しすぎず、かといって冷淡にもならず、互いの自由とプライベートを尊重し合える大人としての距離感が、心地よい癒しを生み出す大きな要因となっています。</p>

              <blockquote style="border-left: 3px solid var(--color-primary); padding-left: 16px; margin: 24px 0; color: var(--text-muted); font-style: italic; font-size: 0.95rem; line-height: 1.7;">
                「家庭を壊したいわけではないけれど、自分を一人の大人・異性として優しく受け止めてくれる『もう一つの居場所』があることで、日々の仕事や家庭生活にもかえって穏やかな心で向き合えるようになりました。」（40代・会社経営男性の声）
              </blockquote>
"""

def generate_deep_section_2(h2_title, description):
    return f"""
              <h2>{h2_title}</h2>
              <p>具体的に行動を起こす際、あるいは関係性を育む上で意識すべきポイントは、無理な主張をせず「相手の視点とプライバシーを徹底的に尊重する」姿勢にあります。{h2_title}を実践することで、無用なトラブルを防ぎ、長く心地よい関係を維持することができます。</p>
              
              <h3>2-1. 実践で活かせる具体的なステップとマナー</h3>
              <p>第一に大切なのは、連絡の頻度や時間帯に関する事前のすり合わせです。お互いの生活リズムや家庭での過ごし方は異なります。平日の日中を中心としたやり取りに留める、週末や夜間は連絡を控えるといったスマートな配慮が、お相手に対する最高の誠実さとなります。</p>
              <p>第二に、会話やメッセージにおいては「聞き手に回る意識」を持つことが効果的です。日頃、仕事や家庭で責任ある立場にいる方ほど、自分の話を静かに頷いて聞いてくれる存在を求めています。相手の考えや悩みを否定せず、共感を持って受け止める姿勢が、深い信頼関係を築く鍵となります。</p>

              <h3>2-2. 実際のケーススタディ（よくある成功例と気づき）</h3>
              <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--color-border-light); border-radius: 8px; padding: 20px; margin: 20px 0;">
                <h4 style="color: var(--color-primary); margin-bottom: 10px; font-size: 1.05rem; font-weight: 700;">【ケーススタディ】時間を大切にする大人同士のスマートな交流</h4>
                <p style="font-size: 0.92rem; line-height: 1.7; margin-bottom: 0;">30代後半の既婚女性Bさんは、子育てが落ち着いた時期にお茶デートから交流を開始しました。お互いに「初回は平日のカフェで45分間だけ」とルールを決めて会ったことで、家庭に影響を与えず、かつ『もう少し話してみたい』という最高の余韻を残すことができました。無理のない計画と引き際の爽やかさが、長続きする秘訣となっています。</p>
              </div>
"""

def generate_deep_section_3(h2_title, description):
    return f"""
              <h2>{h2_title}</h2>
              <p>良好なパートナーシップを育む上では、ポジティブな側面だけでなく、避けるべきリスクやNG行動についても正確に把握しておく必要があります。{h2_title}を踏まえた行動を心がけることが、自分自身と大切なお相手の未来を守ることにつながります。</p>
              
              <h3>3-1. 犯しがちな注意点とNG行動のチェックリスト</h3>
              <ul style="line-height: 1.8; margin-bottom: 24px; padding-left: 20px;">
                <li><strong>過度な束縛や感情の押し付け:</strong> 相手の返信が遅れた際に理由を詰問したり、行動を制限しようとすることは関係破綻の最大の原因となります。</li>
                <li><strong>家庭や配偶者に対する度を超えた愚痴:</strong> 相手の配偶者や家庭環境に対するネガティブな発言は避けましょう。互いに大人の節度を保つことが大切です。</li>
                <li><strong>身バレ・セキュリティ対策の怠り:</strong> スマホの通知設定の変更、写真の限定公開、写真データの自動消去など、デジタル面での防衛策を徹底しましょう。</li>
              </ul>

              <h3>3-2. 心のゆとりと自分らしさを取り戻すための秘訣</h3>
              <p>最も重要なのは、「相手に依存しすぎない自立した精神」を持つことです。サードプレイス（第3の居場所）としてのパートナーシップは、自分の人生をより豊かに彩るためのスパイスであり、人生の全責任を委ねる場所ではありません。自分自身の趣味や仕事、自己磨きを楽しみながら、お相手との時間を慈しむゆとりこそが、大人としての洗練された魅力を引き立てます。</p>
"""

def rewrite_single_html_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract existing h2 titles or generate fallback ones
    h2_matches = re.findall(r'<h2>(.*?)</h2>', content)
    h2_1 = h2_matches[0] if len(h2_matches) > 0 else "基本の考え方と大人の心構え"
    h2_2 = h2_matches[1] if len(h2_matches) > 1 else "具体的実践ステップとマナー"
    h2_3 = h2_matches[2] if len(h2_matches) > 2 else "注意点と長続きの秘訣"

    # Extract meta description
    desc_match = re.search(r'<meta name="description" content="(.*?)">', content)
    description = desc_match.group(1) if desc_match else "既婚者のための上質なパートナーシップと身バレ対策の解説。"

    lead_paragraph = f"""
              <p class="article-lead" style="font-size: 1.05rem; line-height: 1.8; color: var(--text-color); margin-bottom: 32px; border-bottom: 1px solid var(--color-border-light); padding-bottom: 24px;">
                {description} 本記事では、社会的ステータスと品格を兼ね備えた大人の男女に向けて、失敗しない考え方やプライバシー対策、お互いに心地よい関係を育むための具体的アプローチを専門的視点から徹底解説します。
              </p>
"""

    sec1_html = generate_deep_section_1(h2_1, description)
    sec2_html = generate_deep_section_2(h2_2, description)
    sec3_html = generate_deep_section_3(h2_3, description)

    # Highlight box
    highlight_html = """
              <div class="highlight-box">
                <div class="highlight-box__title">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                  本記事の重要ポイント
                </div>
                <p>・<strong>家庭第一主義とプライバシー保護の徹底を最優先する</strong></p>
                <p>・<strong>互いの立場と生活リズムを尊重するスマートな距離感を維持する</strong></p>
                <p>・<strong>自立した大人としての心のゆとりと気遣いを持って向き合う</strong></p>
              </div>
"""

    cta_box_html = """
              <div class="in-body-cta" style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--color-border-light); border-radius: 8px; padding: 32px 24px; margin: 48px 0; text-align: center;">
                <h3 style="font-size: 1.25rem; color: var(--color-primary); margin-bottom: 12px; font-weight: 700;">Re.en 創設メンバー事前インビテーション受付中</h3>
                <p style="font-size: 0.95rem; margin-bottom: 24px; color: var(--text-muted); line-height: 1.7;">Re.en（リエン）は、社会的ステータスと品格を備えた既婚者のための完全審査制コミュニティです。<br>現在、創設メンバー限定特典（有料サブスクリプション2ヶ月間完全無料提供）の事前エントリーを受け付けております。</p>
                <a href="preregister.html" class="btn btn--primary" style="display: inline-block; padding: 14px 36px; font-weight: 700; text-decoration: none;">優先インビテーションに申し込む</a>
              </div>
"""

    full_body_html = lead_paragraph + sec1_html + sec2_html + sec3_html + highlight_html + cta_box_html

    pure_text = clean_html(full_body_html)
    char_count = len(pure_text)
    read_time = max(5, int(char_count / 500))

    content = re.sub(
        r'<span class="article-header__readtime">読了目安: [^<]+</span>',
        f'<span class="article-header__readtime">読了目安: {read_time}分</span>',
        content
    )

    body_pattern = r'(?s)(<div class="article-body">).*?(?=\s*<!-- Related Articles -->)'
    content = re.sub(body_pattern, rf'\g<1>\n{full_body_html}\n            </div>', content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return char_count

def main():
    print("Rewriting ALL column-detail HTML files on disk...")
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
