clean:
	find . -name '*.py[co]' -delete
	find . -name '*~' -delete
	find . -name '__pycache__' -delete
	rm -rf soco.egg-info
	rm -rf dist
