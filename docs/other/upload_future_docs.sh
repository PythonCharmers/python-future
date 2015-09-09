On the local machine
--------------------

git checkout v0.7.0
rm -Rf docs/build/
cd docs; make html
cp cheatsheet.pdf /shared/
cd build
touch /shared/python-future-html-docs.zip
rm /shared/python-future-html-docs.zip
zip -r /shared/python-future-html-docs.zip *

scp -i ~/.ssh/pythoncharmers_2015.pem /shared/python-future-html-docs.zip python-future.org:
scp -i ~/.ssh/pythoncharmers_2015.pem /shared/cheatsheet.pdf python-future.org:
ssh python-future.org


On the remote machine:
----------------------

cd /var/www/python-future/
unzip -o ~/python-future-html-docs.zip
chmod a+r * html/* html/_static/*
cp ~/cheatsheet.pdf ./html/compatible_idioms.pdf
cp ~/cheatsheet.pdf ./html/cheatsheet.pdf

