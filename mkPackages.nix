{
  pkgs ? import <nixpkgs> {},
  swiProlog ? pkgs.swiProlog,
  fetchFromGitHub ? pkgs.fetchFromGitHub
}:
let lib = pkgs.lib;
    package = import ./package.nix;
    tags = lib.importJSON ./tags.json;

    derivations = lib.attrsets.mapAttrs' (version: tag:
      lib.attrsets.nameValuePair
        (builtins.replaceStrings ["."] ["_"] version)
        (package {
          inherit swiProlog fetchFromGitHub;

          inherit version;
          inherit (tag) repo rev hash;
        })
    ) tags;

    aliases = lib.importJSON ./alias.json;
    aliasedDerivations = lib.attrsets.mapAttrs' (version: full_version:
      lib.attrsets.nameValuePair
        (builtins.replaceStrings ["."] ["_"] version)
        derivations.${builtins.replaceStrings ["."] ["_"] full_version}
    ) aliases;
in
derivations // aliasedDerivations // {
  default = aliasedDerivations.latest;
  devel = aliasedDerivations.latest-devel;
}
