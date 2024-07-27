{
  swiProlog,
  fetchFromGitHub,
  tcmalloc,

  version,
  repo,
  rev,
  hash
}:
(swiProlog.override {
  # minimize gperftools to just tcmalloc part
  gperftools = tcmalloc;
}).overrideAttrs {
  inherit version;
  src = fetchFromGitHub {
    owner = "SWI-Prolog";
    inherit repo;
    inherit rev;
    inherit hash;
    fetchSubmodules = true;
  };
}
