{
  description = "SWI-Prolog versions";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {nixpkgs, flake-utils, ...}:
    let mkPackages = import ./mkPackages.nix; in
    {
      overlays.default = import ./overlay.nix;
      packages = builtins.mapAttrs (system: _:
        mkPackages {pkgs=nixpkgs.legacyPackages.${system};}
      ) flake-utils.lib.system;

      devShells = builtins.mapAttrs (system: _:
        {
          default = import ./shell.nix {pkgs=nixpkgs.legacyPackages.${system};};
        }
      ) flake-utils.lib.system;
  };
}
