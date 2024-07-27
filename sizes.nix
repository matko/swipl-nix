{
  writeScript,
  bash,
  bc,
  nix,
  swiProlog
}:
let minimal = swiProlog.override {
          withNativeCompiler = false;
          withDb = false;
          withPcre = false;
          withYaml = false;
          withJava = false;
          withOdbc = false;
          withPython = false;
          withGui = false;
    };
    common = minimal.override {
      withDb = true;
      withPcre = true;
      withYaml = true;
    };
    withDb = minimal.override {
      withDb = true;
    };
    withPcre = minimal.override {
      withPcre = true;
    };
    withYaml = minimal.override {
      withYaml = true;
    };
    withJava = minimal.override {
      withJava = true;
    };
    withOdbc = minimal.override {
      withOdbc = true;
    };
    withPython = minimal.override {
      withPython = true;
    };
    withGui = minimal.override {
      withGui = true;
    };
    full = minimal.override {
      withDb = true;
      withPcre = true;
      withYaml = true;
      withJava = true;
      withOdbc = true;
      withPython = true;
      withGui = true;
    };
    noGui = full.override {
      withGui = false;
    };
    noJava = full.override {
      withJava = false;
    };
    noPython = full.override {
      withPython = false;
    };
in
writeScript "swipl-sizes" ''
#!${bash}/bin/bash
closureSize () {
  echo $(${nix}/bin/nix path-info -S "$1"|awk '{print $2}')
}

mbSize () {
  echo "scale=2;$1 / 1024.0 / 1024.0"|${bc}/bin/bc
}

printClosureSize () {
  size=$(closureSize $2)
  printf "%-10s %12s %12s\n" "$1" "$size" "''$(mbSize $size)M"
}

addedSize () {
  minimalSize=$1
  size=$(closureSize $2)
  echo $((size-minimalSize))
}

printAddedSize () {
  size=$(closureSize $3)
  added=$(addedSize $2 $3)
  printf "%-10s %12s %12s %12s\n" "$1" "$size" "''$(mbSize $size)M" "+''$(mbSize $added)M"
}

subtractedSize () {
  fs=$1
  size=$(closureSize $2)
  echo $((fs-size))
}

printSubtractedSize () {
  size=$(closureSize $3)
  subtracted=$(subtractedSize $2 $3)
  printf "%-10s %12s %12s %12s\n" "$1" "$size" "''$(mbSize $size)M" "-''$(mbSize $subtracted)"
}

printf "%10s %12s %12s %12s\n" "PKG" "SIZE" "MBSIZE" "CHANGE"

minimalSize=$(closureSize ${minimal})
fullSize=$(closureSize ${full})
printClosureSize minimal ${minimal}
echo ""
#printClosureSize common ${common}
printAddedSize withYaml $minimalSize ${withYaml}
printAddedSize withOdbc $minimalSize ${withOdbc}
printAddedSize withPcre $minimalSize ${withPcre}
printAddedSize withDb $minimalSize ${withDb}
printAddedSize withGui $minimalSize ${withGui}
printAddedSize withPython $minimalSize ${withPython}
printAddedSize withJava $minimalSize ${withJava}
echo ""
printSubtractedSize noJava $fullSize ${noJava}
printSubtractedSize noPython $fullSize ${noPython}
printSubtractedSize noGui $fullSize ${noGui}
echo ""
printClosureSize full ${full}
''
