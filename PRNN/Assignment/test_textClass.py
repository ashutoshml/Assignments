import pytest
import textClassification as t


def test_totalWords():
    dict = {"hi": 301, "bye": 23, "good": 123}
    assert t.totalWords(dict) == 447
