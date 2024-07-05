py-files := `find . -type f -name "*.py" -and -not -path "./venv/*" | tr "\n" " "`

clean:
    rm -rf chroma
    rm -f indexed_hashes.txt

vectorize:
    python3 vectorize.py

chat:
    python3 chat.py

venv:
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
    venv/bin/pip install -r requirements-dev.txt

lint file:
    pylint {{file}} || :
    mypy {{file}} || :

lint-all:
    pylint {{py-files}} || :
    mypy {{py-files}} || :
