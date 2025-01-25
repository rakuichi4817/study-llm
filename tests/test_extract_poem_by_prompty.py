import os

from src.extract_poem_by_prompty import (
    extract_poems_from_review,
    get_aoai_settings,
    load_prompty,
)

sample_review = """ある日、仕事に疲れた帰り道、「自分へのご褒美」が必要だと感じました。スマホで偶然見つけたこのステーキ屋さん。その写真越しに伝わる肉の輝きに惹かれ、気づけば予約ボタンを押していました。扉を開けた瞬間のあの香り――それは、疲れた心に優しく語りかけるような芳醇な肉の誘い。まるで、「今日という日をよく頑張ったね」と囁いてくれるかのようでした。

店内は、落ち着いた木の香りが漂う癒しの空間。壁には地元のアーティストが描いたらしい抽象画がかかり、どこか「静かなる情熱」を感じさせるようなインテリア。窓の外には小さな庭が広がり、ライトに照らされた植物たちが夜の静寂を美しく彩っていました。

「この空間は、料理を味わうためだけに存在しているんだな」と思わせるような、静かでありながらも温かい雰囲気。

頼んだのはお店の一番人気、特選サーロインステーキ200g。運ばれてきた瞬間、肉の表面で輝く美しい焼き加減に目を奪われます。ナイフを入れると、予想以上に柔らかく滑らかに切れていき、そこから溢れる肉汁に思わず息をのみました。

ナイフを入れた瞬間、肉の繊維がするするとほぐれていくのが見て取れます。一口頬張ると、まるで「肉の小宇宙」が広がるかのような感覚。噛むたびに、肉汁とともに溢れ出る深い旨味と甘み。それは、ただの食事ではなく、一種の芸術体験に近いものでした。付け合わせのポテトグラタンも絶品。ほのかに香るチーズが、肉の重厚さを優しく受け止め、次の一口をさらに待ち遠しいものにしてくれます。

スタッフの方々の心遣いもまた感動的でした。「お肉がこの温かさで一番美味しいタイミングです」という一言に込められたプロフェッショナルの矜持。それが、食事全体の信頼感をさらに高めてくれました。

総評
ただの食事ではなく、心を満たすひとときを提供してくれる、そんなステーキ屋さんでした。このお店を訪れた日を、私の「食の記憶」に残る大切な1ページとして忘れることはないでしょう。また、あの魔法の一皿に会いに行きたいと思います。"""


def test_load_prompty(project_root: str):
    prompty_file = os.path.join(project_root, "prompts", "sample.prompty")
    aoai_settings = get_aoai_settings()
    prompty = load_prompty(prompty_file, aoai_settings)

    assert prompty


def test_execute_prompty(project_root: str):
    prompty_file = os.path.join(project_root, "prompts", "sample.prompty")
    aoai_settings = get_aoai_settings()
    prompty = load_prompty(prompty_file, aoai_settings)

    output = extract_poems_from_review(prompty, sample_review)

    assert output
