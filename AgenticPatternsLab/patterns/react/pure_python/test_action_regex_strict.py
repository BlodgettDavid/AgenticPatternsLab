import pytest
from AgenticPatternsLab.patterns.react.shared.react_engine import ACTION_RE

# -----------------------------
# VALID ACTIONS (should match)
# -----------------------------
@pytest.mark.parametrize("line", [
    "Action: search('foo')",
    "Action: lookup('bar')",
    "Action: tool_name('some argument')",
])
def test_action_regex_valid(line):
    match = ACTION_RE.match(line)
    assert match is not None
    assert match.group(1) in ["search", "lookup", "tool_name"]
    assert match.group(2) in ["foo", "bar", "some argument"]


# -------------------------------------
# INVALID ACTIONS (should NOT match)
# -------------------------------------
@pytest.mark.parametrize("line", [
    # double quotes not allowed
    'Action: search("foo")',

    # mismatched quotes
    "Action: search('foo\")",
    "Action: search(\"foo')",

    # missing parentheses
    "Action: search'foo'",
    "Action: search foo",

    # missing quotes
    "Action: search(foo)",

    # extra text after action
    "Action: search('foo') extra",
    "Action: search('foo')\nAction: search('bar')",

    # wrong prefix
    "Acton: search('foo')",
    "Action search('foo')",

    # empty argument
    "Action: search('')",
])
def test_action_regex_invalid(line):
    assert ACTION_RE.fullmatch(line) is None
