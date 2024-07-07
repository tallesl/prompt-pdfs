py-files := `find . -type f -name "*.py" -and -not -path "./venv/*" | tr "\n" " "`

tree:
    git ls-files | tree --fromfile --dirsfirst

venv:
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
    venv/bin/pip install -r requirements-dev.txt

lint file:
    pylint {{file}} --max-line-length 120 || :
    mypy {{file}} --strict || :

lint-all:
    pylint {{py-files}} --max-line-length 120 || :
    mypy {{py-files}} --strict || :

test:
    pytest --setup-show

vectorize:
    python3 src/vectorize.py

chat:
    python3 src/chat.py

clean:
    rm -rf chroma
    rm -f indexed_hashes.txt
