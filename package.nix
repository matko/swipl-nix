{
  lib,
  swiProlog,
  fetchFromGitHub,

  version,
  repo,
  rev,
  hash
}:
swiProlog.overrideAttrs (final: prev: {
  inherit version;
  src = fetchFromGitHub {
    owner = "SWI-Prolog";
    inherit repo;
    inherit rev;
    inherit hash;
    fetchSubmodules = true;
  };
  preUnpack = ''
echo "display is ''${DISPLAY:-unset}"
'';
  passthru = prev // rec {
    overridePackages = overrides: builtins.foldl' (p: def: p.overridePackage def) final.finalPackage (lib.mapAttrsToList (n: v: v // {name=n;}) overrides);
    overridePackage = ({ name, path ? null, rev ? null, hash ? null }:
      let path' = if path != null then path else fetchFromGitHub {
            owner = "SWI-Prolog";
            repo = "packages-${name}";
            inherit rev hash;
          }; in
      final.finalPackage.overrideAttrs (f2: p2: {
        postUnpack = p2.postUnpack ++ [''
echo Replacing package ${name}
rm -rf $sourceRoot/packages/${name}
cp -r ${path'} $sourceRoot/packages/${name}
chmod -R u+w $sourceRoot/packages/${name}
ls -alh $sourceRoot/packages
ls -alh $sourceRoot/packages/${name}
''];
      }));
  };
  postUnpack = [];
})
