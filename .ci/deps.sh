#!/bin/sh -xe

# Need $PYTHON

$PYTHON -m pip install --upgrade pip setuptools
npm install -g bower
curl -fsSL -o haskellstack.sh https://get.haskellstack.org/
curl -fsSL -o miniconda.sh \
     http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x haskellstack.sh miniconda.sh
./haskellstack.sh
stack setup --resolver ghc-8.4.2
./miniconda.sh -b -p "$HOME/miniconda"
go get -u github.com/gpmgo/gopm
go install github.com/gpmgo/gopm
go get -u gopkg.in/alecthomas/gometalinter.v2
cpan App::cpanminus
echo 'pytest-spec' >> test-requirements.txt
$PYTHON -m pip install -r requirements.txt -r test-requirements.txt
