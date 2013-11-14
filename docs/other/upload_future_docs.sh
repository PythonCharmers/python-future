On the local machine
--------------------

git checkout v0.7.0
rm -Rf docs/build/
cd docs; make html
cd build
touch ../../python-future-html-docs.zip
rm ../../python-future-html-docs.zip
zip -r ../../python-future-html-docs.zip *
scp ../../python-future-html-docs.zip python-future.org:
ssh python-future.org


On the remote machine:
----------------------

cd /var/www/python-future/html
unzip ~/python-future-html-docs.zip
chmod a+r * _static/*

