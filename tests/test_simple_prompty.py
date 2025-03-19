import os

from src.simple_prompty import execute, get_aoai_settings, load_prompty

sample_review = """スターウォーズいいですよね"""


def test_load_prompty(project_root: str):
    prompty_file = os.path.join(project_root, "prompts", "simple.prompty")
    aoai_settings = get_aoai_settings()
    prompty = load_prompty(prompty_file, aoai_settings)

    assert prompty


def test_execute_prompty(project_root: str):
    prompty_file = os.path.join(project_root, "prompts", "simple.prompty")
    aoai_settings = get_aoai_settings()
    prompty = load_prompty(prompty_file, aoai_settings)

    output = execute(prompty, sample_review)

    assert output
