.PHONY: test strict
test:
	flake8 --max-complexity=9 .
	python -m unittest  discover

strict:
	flake8 --max-complexity=8 .
	python -m unittest  discover

