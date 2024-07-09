{
  pkgs ? import <nixpkgs> {}
}:
let lib = pkgs.lib;
    package = import ./package.nix;
    tags = lib.importJSON ./tags.json;

    derivations = lib.attrsets.mapAttrs' (version: tag:
      lib.attrsets.nameValuePair
        (builtins.replaceStrings ["."] ["_"] version)
        (pkgs.callPackage package {
          inherit version;
          inherit (tag) repo rev hash;

          # temporary import from a version copied from nixpkgs
          swiProlog = pkgs.callPackage ./swi-prolog {
            inherit (pkgs.darwin.apple_sdk.frameworks) Security;
          };
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
