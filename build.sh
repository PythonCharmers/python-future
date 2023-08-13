# XXX: TODO: we should make this include -e once tests pass
set -xuo pipefail

DOCKER_IMAGE=jmadler/python-future-builder
# XXX: TODO: Perhaps this version shouldn't be hardcoded
version=0.18.3

docker build . -t $DOCKER_IMAGE
#docker push $DOCKER_IMAGE:latest

for i in cp27-cp27m cp35-cp35m cp36-cp36m cp37-cp37m cp38-cp38 cp39-cp39; do
    docker run -ti -v $(realpath dist):/root/python-future/dist $DOCKER_IMAGE /root/python-future/setup.sh $version $(basename $i)
done

python setup.py sdist
python setup.py clean
echo You may now run: "twine upload dist/*"
