.PHONY: clean

XARGS := $(shell which parallel || which xargs) $(shell test $$(uname) = Linux && echo -r)

data/crossings.json: data/crossings.csv
	env PYTHONPATH=. bin/crossings-to-json.py < $< > $@

test:
	python -m discover crossings

clean:
	rm -f data/crossings.json
	find crossings -name '*.pyc' -print0 | $(XARGS) -0 rm
	find . -name '__pycache__' -print0 | $(XARGS) -0 rm -rf
