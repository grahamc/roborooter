.PHONY: test
test:
	flake8 --max-complexity=10 .
	python -m unittest  discover
