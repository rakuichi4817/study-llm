import os
from typing import Literal

from openai import AzureOpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

SYSTEM_MESSAGE = """
あなたは飲食店のレビューから、ポエム的な内容をを抽出するAIアシスタントです。

与えられるテキスト情報は、飲食店に対してその飲食店を訪れたユーザが投稿したレビューです。
レビューの内容は、飲食店の評価や感想、食事内容、サービス内容などが含まれます。
しかし、その中には、飲食店の評価とは直接関係のない、投稿者の背景や昔話、詞的な表現が含まれることがあります。
食べた料理に対して詞的な表現がされている場合、それはポエムではありますが有用な情報なので抽出はしないでください。
この内容を抽出してください。
"""


class Settings(BaseSettings):
    # 各種設定値を読み込む
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../.env")
    )

    aoai_endpoint: str = ""
    aoai_api_version: str = ""
    aoai_api_key: str = ""
    deployment_name: str = "gpt-4o"


class PoemMeassage(BaseModel):
    """抽出されたポエムの情報"""

    sentence: str = Field(title="テキストに含まれていたポエム的な内容")
    reason: str = Field(title="ポエムと判断された理由")
    sentence_type: Literal["自分のこと", "お店のこと"] = Field(
        title="内容が自分の話か、お店の話かを判定してください"
    )


class ExtractPoemResponse(BaseModel):
    """テキストに含まれるポエムのリスト"""

    poem_messages: list[PoemMeassage] = Field(title="抽出されたポエムのリスト")


settings = Settings()


openai_client = AzureOpenAI(
    azure_endpoint=settings.aoai_endpoint,
    api_version=settings.aoai_api_version,
    api_key=settings.aoai_api_key,
)


def extract_poems_from_review(review: str) -> list[PoemMeassage]:
    """レビューテキストからポエムを抽出する

    Args:
        review (str): 抽出対象のレビューテキスト

    Returns:
        list[PoemMeassage]: 抽出されたポエムリスト
    """

    system_message = ChatCompletionSystemMessageParam(
        role="system", content=SYSTEM_MESSAGE
    )
    query = ChatCompletionUserMessageParam(role="user", content=review)
    messages: list[ChatCompletionMessageParam] = [system_message, query]

    response = openai_client.beta.chat.completions.parse(
        model=settings.deployment_name,
        messages=messages,
        temperature=0,
        response_format=ExtractPoemResponse,
    )

    parse_sentence_result = response.choices[0].message.parsed

    if parse_sentence_result is None:
        raise ValueError("ポエムの抽出に失敗しました")
    return parse_sentence_result.poem_messages


if __name__ == "__main__":
    review_text = """
ある日、仕事に疲れた帰り道、「自分へのご褒美」が必要だと感じました。スマホで偶然見つけたこのステーキ屋さん。その写真越しに伝わる肉の輝きに惹かれ、気づけば予約ボタンを押していました。扉を開けた瞬間のあの香り――それは、疲れた心に優しく語りかけるような芳醇な肉の誘い。まるで、「今日という日をよく頑張ったね」と囁いてくれるかのようでした。

店内は、落ち着いた木の香りが漂う癒しの空間。壁には地元のアーティストが描いたらしい抽象画がかかり、どこか「静かなる情熱」を感じさせるようなインテリア。窓の外には小さな庭が広がり、ライトに照らされた植物たちが夜の静寂を美しく彩っていました。

「この空間は、料理を味わうためだけに存在しているんだな」と思わせるような、静かでありながらも温かい雰囲気。

頼んだのはお店の一番人気、特選サーロインステーキ200g。運ばれてきた瞬間、肉の表面で輝く美しい焼き加減に目を奪われます。ナイフを入れると、予想以上に柔らかく滑らかに切れていき、そこから溢れる肉汁に思わず息をのみました。

ナイフを入れた瞬間、肉の繊維がするするとほぐれていくのが見て取れます。一口頬張ると、まるで「肉の小宇宙」が広がるかのような感覚。噛むたびに、肉汁とともに溢れ出る深い旨味と甘み。それは、ただの食事ではなく、一種の芸術体験に近いものでした。付け合わせのポテトグラタンも絶品。ほのかに香るチーズが、肉の重厚さを優しく受け止め、次の一口をさらに待ち遠しいものにしてくれます。

スタッフの方々の心遣いもまた感動的でした。「お肉がこの温かさで一番美味しいタイミングです」という一言に込められたプロフェッショナルの矜持。それが、食事全体の信頼感をさらに高めてくれました。

総評
ただの食事ではなく、心を満たすひとときを提供してくれる、そんなステーキ屋さんでした。このお店を訪れた日を、私の「食の記憶」に残る大切な1ページとして忘れることはないでしょう。また、あの魔法の一皿に会いに行きたいと思います。
    """
    poems = extract_poems_from_review(review_text)
    for poem in poems:
        print(poem)
