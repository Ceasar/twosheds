from twosheds import Sentence


def test_str():
    sentence = Sentence(['"msg"'])
    assert str(sentence) == '"msg"'
