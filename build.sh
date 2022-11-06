#!/bin/sh
container/Dockerfile.sh > Dockerfile
docker build -t realiserad/adcs-deployment .