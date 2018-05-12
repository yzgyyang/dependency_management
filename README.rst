``dependency_management`` provides a Python API for common package
managers.

It is used extensively by `coala <https://github.com/coala>`__.

The only existing interface implemented are ``PackageRequirement``
classes, which describe the dependencies of a piece of software, and
provide a generic method to install those dependencies on any host
operating system.

It is tested on Linux, macOS and Windows.

Supported package managers:

-  Haskell

   -  `stack <http://haskellstack.org>`__
   -  `cabal <https://www.haskell.org/cabal/>`__

-  `cargo <https://crates.io/>`__ - Rust
-  `composer <https://getcomposer.org/>`__ - Php
-  `conda <https://conda.io/>`__ - any software stack
-  Distribution

   -  apt-get
   -  brew (macOS and Linux)
   -  dnf
   -  pacman (Linux and Windows)
   -  portage
   -  xbps
   -  yum
   -  zypper (openSUSE)

-  `gem <https://rubygems.org/>`__ - Ruby
-  `go get <https://golang.org/>`__ - Golang
-  `julia pkg <https://docs.julialang.org/en/stable/stdlib/pkg/>`__ -
   julia
-  `luarocks <https://luarocks.org/>`__ - Lua
-  `Apache Maven <https://maven.apache.org/>`__ - Java
-  `npm <http://npmjs.com/>`__ - JavaScript
-  `bower <https://bower.io/>`__ - JavaScript
-  `pip <https://pip.pypa.io/>`__ - Python
-  `Rscript <https://www.r-project.org/>`__ - R
