`dependency_management` provides a Python API for common package managers.

It is used extensively by [coala](https://github.com/coala).

The only existing interface implemented are `PackageRequirement` classes,
which describe the dependencies of a piece of software, and provide a generic
method to install those dependencies on any host operating system.

It is tested on Linux, macOS and Windows.

Supported package managers:

- [cabal](https://www.haskell.org/cabal/) - Haskell
- [cargo](https://crates.io/) - Rust
- [composer](https://getcomposer.org/) - Php
- [conda](https://conda.io/) - any software stack
- Distribution
  - apt-get
  - brew (macOS and Linux)
  - dnf
  - pacman (Linux and Windows)
  - portage
  - xbps
  - yum
  - zypper (openSUSE)
- [gem](https://rubygems.org/) - Ruby
- [go get](https://golang.org/) - Golang
- [julia pkg](https://docs.julialang.org/en/stable/stdlib/pkg/) - julia
- [luarocks](https://luarocks.org/) - Lua
- [Apache Maven](https://maven.apache.org/) - Java
- [npm](http://npmjs.com/) - JavaScript
- [pip](https://pip.pypa.io/) - Python
- [Rscript](https://www.r-project.org/) - R
