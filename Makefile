# vim: set ts=8 sts=8 sw=8 noexpandtab:

.env:
	@./setup.bash

requirements.txt: *.py .env
	pip freeze > requirements.txt

lacroix.zip: requirements.txt
	zip lacroix.zip *.py
	cd .env && zip -r ../lacroix.zip lib/python2.7/site-packages

package: lacroix.zip

publish: package
	@./publish.bash
