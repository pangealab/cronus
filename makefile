.PHONY: clean build publish

build: clean
	sudo python3 setup.py install

publish: build
	python3 setup.py sdist
	twine upload dist/*

clean:
	rm -r build dist *.egg-info || true