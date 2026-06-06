import re
from AgenticPatternsLab.patterns.react.shared.prompt_builder import build_react_prompt


def test_prompt_builder_includes_user_query():
    prompt = build_react_prompt("Where is the library?")
    assert "Where is the library?" in prompt


def test_prompt_builder_contains_strict_rules():
    prompt = build_react_prompt("test")

    # Check for key rule phrases
    assert "You MUST begin every response with \"Thought:\"" in prompt
    assert "You MUST include a Thought before every Action or Final Answer." in prompt
    assert "You MUST use ONLY single quotes inside search('<query>')." in prompt
    assert "You MUST NOT use double quotes in any Action." in prompt
    assert "If you violate ANY rule, output EXACTLY: FORMAT ERROR" in prompt


def test_prompt_builder_has_react_structure():
    prompt = build_react_prompt("test")

    # Ensure the template includes the expected ReAct scaffolding
    assert "Thought:" in prompt
    assert "Action: search('<query>')" in prompt
    assert "User query:" in prompt


def test_prompt_builder_is_multiline_string():
    prompt = build_react_prompt("hello")
    assert isinstance(prompt, str)
    assert "\n" in prompt


def test_prompt_builder_is_deterministic():
    p1 = build_react_prompt("abc")
    p2 = build_react_prompt("abc")
    assert p1 == p2
