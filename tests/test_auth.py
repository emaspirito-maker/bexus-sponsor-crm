import auth


def test_verify_password_accepts_correct_password():
    stored_hash = auth.hashlib.sha256(b"correct-horse").hexdigest()
    assert auth.verify_password("correct-horse", stored_hash) is True


def test_verify_password_rejects_wrong_password():
    stored_hash = auth.hashlib.sha256(b"correct-horse").hexdigest()
    assert auth.verify_password("wrong-guess", stored_hash) is False
