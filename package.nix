{
  swiProlog,
  fetchFromGitHub,

  version,
  repo,
  rev,
  hash
}:
swiProlog.overrideAttrs {
  inherit version;
  src = fetchFromGitHub {
    owner = "SWI-Prolog";
    inherit repo;
    inherit rev;
    inherit hash;
    fetchSubmodules = true;
  };
}
