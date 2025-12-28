from unittest.mock import Mock, patch

import pytest
import typer

from pp_languagetool.helpers import build_offset_to_line_col_map, run_languagetool


# testing
@pytest.mark.parametrize(
    "text,offset,expected_line,expected_col",
    [
        # (input_text, offset_to_check, expected_line, expected_col)
        ("", 0, 1, 1),  # empty string
        ("A", 0, 1, 1),  # single char
        ("A", 1, 1, 2),  # after single char
        ("Hello\nWorld", 0, 1, 1),  # first char
        ("Hello\nWorld", 5, 1, 6),  # newline position
        ("Hello\nWorld", 6, 2, 1),  # first char of line 2
        ("\n\n\n", 0, 1, 1),  # only newlines - first
        ("\n\n\n", 2, 3, 1),  # only newlines - third
        ("A\n\nB", 2, 2, 1),  # consecutive newlines
        ("Café", 3, 1, 4),  # unicode
    ],
)
def test_build_offset_to_line_col_map_parametrized(
    text, offset, expected_line, expected_col
):
    result = build_offset_to_line_col_map(text)
    assert result[offset] == (expected_line, expected_col)


# testing 'run_languagetool()'
def test_run_languagetool_command_not_found():
    # When languagetool is not installed, subprocess raises FileNotFoundError

    with patch("subprocess.run", side_effect=FileNotFoundError):
        with pytest.raises(typer.Exit) as exc_info:
            run_languagetool("Some text", "en-US")

        # Should exit with code 1
        assert exc_info.value.exit_code == 1


def test_run_languagetool_invalid_json():
    # LanguageTool returns something that's not valid JSON

    mock_result = Mock()
    mock_result.stdout = "This is not JSON!"

    with patch("subprocess.run", return_value=mock_result):
        with pytest.raises(typer.Exit) as exc_info:
            run_languagetool("text", "en-US")

        assert exc_info.value.exit_code == 1
