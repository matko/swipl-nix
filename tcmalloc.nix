{
  stdenv,
  gperftools
}:
stdenv.mkDerivation {
  pname = "tcmalloc_minimal";
  version = gperftools.version;
  dontUnpack = true;
  installPhase = ''
runHook preInstall
mkdir -p $out/lib/pkgconfig
cp ${gperftools}/lib/libtcmalloc_minimal.so* $out/lib/
cp ${gperftools}/lib/pkgconfig/libtcmalloc_minimal.pc $out/lib/pkgconfig/
substituteInPlace $out/lib/pkgconfig/libtcmalloc_minimal.pc --replace-fail ${gperftools} $out
runHook postInstall
'';
}
