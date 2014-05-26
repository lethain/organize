env:
	virtualenv env
	$(PWD)/env/bin/pip install -r requirements.txt
	$(PWD)/env/bin/python setup.py develop

test:
	python -m unittest discover -s organize/tests/

style : 
	$(PWD)/env/bin/pep8 --max-line-length=500 organize
	$(PWD)/env/bin/pylint organize -E

upload:
	python setup.py sdist bdist_wininst upload

clean:
	rm -rf build/ dist/ organize.egg-info/