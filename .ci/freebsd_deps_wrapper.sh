#!/bin/sh -xe

# Need $PYTHON

export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
PYTHON=$PYTHON .ci/deps.sh
