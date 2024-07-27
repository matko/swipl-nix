{
  pkgs ? import <nixpkgs> {},
  swiProlog ? pkgs.swiProlog,
  fetchFromGitHub ? pkgs.fetchFromGitHub
}:
let lib = pkgs.lib;
    package = import ./package.nix;
    branches = lib.importJSON ./branches.json;
    tags = lib.importJSON ./tags.json;

    branchDerivations = lib.attrsets.mapAttrs' (name: branch:
      let reportedVersion = "${branch.version}-${builtins.substring 0 7 branch.rev}";
          base = package {
            inherit swiProlog fetchFromGitHub;

            version = reportedVersion;
            inherit (branch) repo rev hash;
          }; in
      lib.attrsets.nameValuePair
        name
        (base.overrideAttrs (_: prev: {
          cmakeFlags = prev.cmakeFlags ++ [
            "-DGIT_VERSION=${reportedVersion}"
          ];
          # Not sure if this patch even does anything.
          # The version that is reported on startup is the one in the cmake flags.
          postPatch = ''
echo ${reportedVersion} >VERSION
'';
        }))
    ) branches;

    tagDerivations = lib.attrsets.mapAttrs' (version: tag:
      lib.attrsets.nameValuePair
        (builtins.replaceStrings ["."] ["_"] version)
        (package {
          inherit swiProlog fetchFromGitHub;

          inherit version;
          inherit (tag) repo rev hash;
        })
    ) tags;
    derivations = branchDerivations // tagDerivations;

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
