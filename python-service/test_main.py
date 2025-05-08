def test_root():
    from main import read_root
    assert read_root() == {"message": "Hello from Python"}

