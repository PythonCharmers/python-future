# XXX: TODO: we should make this include -e once tests pass
set -xuo pipefail

DOCKER_IMAGE=jmadler/python-future-builder
# XXX: TODO: Perhaps this version shouldn't be hardcoded
version=0.18.4

docker build . -t $DOCKER_IMAGE
docker push $DOCKER_IMAGE:latest

for i in py26 py27 py33 py34 py35 py36 py37 py38 py39; do
    docker run -ti -v $(realpath dist):/root/python-future/dist $DOCKER_IMAGE /root/python-future/setup.sh $version $(basename $i)
done

python setup.py sdist
python setup.py clean
echo You may now run: "twine upload dist/*"
