On the local machine
--------------------

git checkout v0.7.0
rm -Rf docs/build/
cd docs; make html
cd build
touch /shared/python-future-html-docs.zip
rm /shared/python-future-html-docs.zip
zip -r /shared/python-future-html-docs.zip *

cd /shared
scp python-future-html-docs.zip python-future.org:
ssh python-future.org


On the remote machine:
----------------------

cd /var/www/python-future/
unzip -o ~/python-future-html-docs.zip
chmod a+r * html/* html/_static/*

