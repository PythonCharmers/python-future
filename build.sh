# XXX: TODO: we should make this include -e once tests pass
set -xuo pipefail

docker build . -t jmadler/python-future-builder
docker push jmadler/python-future-builder:latest

version=0.18.2

for i in py26 py27 py33 py34 py35 py36 py37 py38 py39; do
    docker run -ti -v $(realpath dist):/root/python-future/dist python-future-builder /root/python-future/setup.sh $version $(basename $i)
done

python setup.py sdist
python setup.py clean
echo You may now run: "twine upload dist/*"
