.PHONY: test
test:
	flake8 .
	python -m unittest  discover
