{ pkgs ? import <nixpkgs> {} }:
import ./mkPackages.nix {inherit pkgs;}
