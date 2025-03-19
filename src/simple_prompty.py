import os
import sys
from pprint import pprint

import prompty
import prompty.azure
from prompty import Prompty
from pydantic_settings import BaseSettings, SettingsConfigDict


class AoaiSettings(BaseSettings):
    """Azure OpenAIの接続情報

    Notes:
        .envファイルから設定を読み込む
    """

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../.env")
    )

    aoai_endpoint: str = ""
    aoai_api_version: str = ""
    aoai_api_key: str = ""
    deployment_name: str = "gpt-4o"


def get_aoai_settings() -> AoaiSettings:
    return AoaiSettings()


def load_prompty(prompty_file: str, aoai_settings: AoaiSettings) -> Prompty:
    """Promptyファイルの設定を読み込む

    Notes:
        Promptyコード内でAOAIクライアントを初期化する部分を見ると、
        azure_endpointなどの引数は`prmoty.model.configuration.items()`で取得できるkey-valueを渡している。
        そのため、AOAIの設定値を取得するためには、Promptyの設定ファイルを読み込んで、
        model.configurationに、AOAIクライアントに渡す引数を入れておけばよい。

    Args:
        prompty_file (str): Promptyの設定ファイルパス
        aoai_settings (AoaiSettings): AOAIの設定

    Returns:
        prompty.Prompty: Promptyのインスタンス
    """

    prompty_ = prompty.load(prompty_file)
    prompty_.model.configuration["azure_endpoint"] = aoai_settings.aoai_endpoint
    prompty_.model.configuration["api_version"] = aoai_settings.aoai_api_version
    prompty_.model.configuration["api_key"] = aoai_settings.aoai_api_key
    prompty_.model.configuration["azure_deployment"] = aoai_settings.deployment_name

    return prompty_


def execute(prompty_: Prompty, question: str) -> str:
    """Promptyを実行する

    Args:
        prompty_ (Prompty): Promptyのインスタンス
        question (str): 入力テキスト
    """
    return prompty.execute(prompt=prompty_, inputs={"question": question})


if __name__ == "__main__":
    # コマンドライン引数から入力テキストを取得
    if len(sys.argv) < 2:
        print("Usage: python simple_prompty.py <input_text>")
    input_text = sys.argv[1]
    aoai_settings = get_aoai_settings()
    prompty_file = os.path.join("../prompts", "simple.prompty")
    prompty_ = load_prompty(prompty_file, aoai_settings)

    result = execute(prompty_, input_text)
    pprint(result)
