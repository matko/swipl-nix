final: _prev:
{
  swipl-nix = import ./mkPackages.nix {pkgs=final;};
}
