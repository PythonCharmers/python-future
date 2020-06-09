docker build . -t python-future-builder

version=0.18.2

for i in py26 py27 py33 py34 py35 py36 py37 py38 py39; do
    docker run -ti -v ~/code/python-future/dist/:/root/python-future/dist python-future-builder /root/python-future/setup.sh $version $(basename $i)
done

#python setup.py sdist
echo twine upload dist/*
