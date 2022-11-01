#!/bin/sh
sh container/Dockerfile.sh > Dockerfile
docker build --squash -t realiserad/adcs-deployment .
