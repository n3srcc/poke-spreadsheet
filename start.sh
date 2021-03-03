#!/bin/bash

IMAGE="n3srcc/poke-spreadsheet"

function help()
{
cat << HEREDOC
Usage: app.py [--page PAGE]

Build
Usage: app.py --build

Run Container
Usage: app.py --run --page PAGE

optional arguments:
    -h, --help                  show this help message and exit
    -b, --build BUILD           Build Docker Image
    -r, --run RUN --page PAGE   Run the docker container
HEREDOC
}

while [[ ${1:0:1} == - ]]; do
    [[ $1 =~ ^-h|--help ]] && {
        help
    };
    
    [[ $1 =~ ^-b|--build$ ]] && { docker build -t $IMAGE . ; };
    [[ $1 =~ ^-r|--run$ ]] && [[ $2 =~ ^-p|--page$ ]] && [[ "$3" -ge "1" ]] && { docker run -it "$IMAGE" app.py --page "$3" ; };
    
    break;
done