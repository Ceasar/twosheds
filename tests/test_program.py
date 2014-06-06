from twosheds.program import Program


def test_gen_tokens():
    program = Program("ls; echo 1;")
    tokens = list(program.gen_tokens())
    assert len(tokens) == 5


def test_gen_tokens_quotes():
    program = Program("ls; 'echo 1;'")
    tokens = list(program.gen_tokens())
    assert len(tokens) == 3


def test_gen_tokens_double_quotes():
    program = Program('git commit -m "test"')
    tokens = list(program.gen_tokens())
    assert len(tokens) == 4
