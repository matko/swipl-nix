# swipl-nix - manage swipl versions using Nix
SWI-Prolog (swipl for short) is a prolog environment that has had a
lot of versions over the years. It is useful to be able to quickly
fetch and run one such version, for example for testing code against
different versions.

This project allows you to do so using Nix. It also allows Nix code to
depend on specific versions of swipl easily.

## Basic usage
Commands below assume a Nix install with flakes enabled. Instructions
for this can be found on the [NixOS wiki](https://nixos.wiki/wiki/Flakes).

### Run the latest stable
```
nix run github:matko/swipl-nix
```
or more explicitely,
```
nix run github:matko/swipl-nix#latest
```

### Run the latest devel
```
nix run github:matko/swipl-nix#latest-devel
```
or
```
nix run github:matko/swipl-nix#devel
```

### Run a specific version
```
nix run github:matko/swipl-nix#9_2_3
```
```
nix run github:matko/swipl-nix#9_2
```
```
nix run github:matko/swipl-nix#9
```
```
nix run github:matko/swipl-nix#9-devel
```

Versions can be specified either completely (`9_2_3` above) or
incompletely, in which case the most recent version with that prefix
is used.

When only a major version is specified, the version is completed to
the most recent stable version with that prefix. If the latest devel
version is required instead, add `-devel` at the end.

## Alternative: swivm
swipl-nix requires you to first install Nix, after which Nix does most
of the heavy lifting for version management. If you are not already a
Nix/NixOS user and your goal is just to get a specific swipl version
installed as soon as possible,
[swivm](https://github.com/fnogatz/swivm) is probably the quicker and
easier option for you.

As a non-nix user you might be wondering why you'd use this project at all.

## Minimum version
Currently, only versions from 8.4.0 upwards are supported. This is the
earliest version that builds cleanly with the unmodified package
definition in nixpkgs.

I would like to support older versions, but this will require
modifying the package definition to fix the build for older
versions. Specifically, it appears that openssl's `RSA_SSLV23_PADDING`
macro was removed in newer versions of openssl, and older swipl
versions depend on it.

## Structure
This project is usable as a flake or as an overlay.

### Flake
As a flake, this project exposes a package set for easy running using
the basic examples above, where each package name is the version
number.

Additionally, this flake provides an overlay under the
`overlays.default` property, which provides the same overlay as
described below.

### Overlay
This project can also be used without flakes. `overlay.nix` defines an
overlay which can be used with nixpkgs to get a package set under
`swipl-nix`. For example, to get version 8.5.3, you'd use `pkgs.swipl-nix."8_5_3"`.

For more information on overlays, consult the [NixOS wiki](https://nixos.wiki/wiki/Overlays).

## Project internals
For any external source (in our case, SWI-Prolog and its modules), nix
requires that we know in advance what the hash will be which it will
assign after doing its import. In order to provide a package set and
overlay, we will likewise need to know in advance what these values
are.

Nixpkgs provides a nice tool for doing this: nix-prefetch-git. This
tool will download a git repo, initialize all submodules, then compute
a hash out of all fetched items. This repository contains code for
automating this process for all version tags in the swipl and
swipl-devel repositories.

Since the swipl repository makes heavy use of submodules, and doing a
fresh clone for every single version is prohibitively expensive, the
automation additionally ensures that all these repositories are
fetched only once.

All this automation can be run as follows:
```
nix develop .
./refresh.sh
```

If you are using direnv, the development environment will activate
automatically when entering the directory, and you won't have to do
`nix develop .` manually.
