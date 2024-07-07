py-files := `find . -type f -name "*.py" -and -not -path "./venv/*" | tr "\n" " "`

tree:
    git ls-files | tree --fromfile --dirsfirst

venv:
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
    venv/bin/pip install -r requirements-dev.txt

pylint:
    pylint ./prompt_pdfs --max-line-length 120 || :
    pylint ./tests --max-line-length 120 || :

mypy:
    mypy -m prompt_pdfs.vectorize --strict || :
    mypy -m prompt_pdfs.chat --strict || :

pytest:
    pytest --setup-show

vectorize:
    python3 -m prompt_pdfs.vectorize

chat:
    python3 -m prompt_pdfs.chat

clean:
    rm -rf chroma
    rm -f indexed_hashes.txt
