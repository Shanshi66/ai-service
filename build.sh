# if pass arg "docker-build", then build docker image
if [ "$1" = "docker-build" ]; then
    docker build -t readbot-python-layer .
fi

docker run --rm -v $(pwd):/tmp readbot-python-layer sh -c "cp /code/python.zip /tmp/"

# remove old python folder in './deploy'
rm -rf ./deploy/python

# unzip python.zip to './deploy' quietly
unzip -q python.zip -d ./deploy

# remove python.zip
rm python.zip

