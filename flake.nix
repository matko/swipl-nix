{
  description = "SWI-Prolog versions";

  inputs = {
    nixpkgs.url = "github:matko/nixpkgs/swipl_to_9.2.6";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {nixpkgs, flake-utils, ...}:
    let mkPackages = import ./mkPackages.nix; in
    {
      overlays.default = import ./overlay.nix;
    } //
    flake-utils.lib.eachSystem flake-utils.lib.allSystems (system:
      let pkgs = nixpkgs.legacyPackages.${system}; in
      rec {
        packages = mkPackages {pkgs=nixpkgs.legacyPackages.${system};};
        apps = {
          sizes =
            let p = pkgs.callPackage ./sizes.nix {swiProlog=packages.master;}; in
            {
            type = "app";
            program = "${p}";
          };
        };

        devShells = {
          default = import ./shell.nix {pkgs=nixpkgs.legacyPackages.${system};};
        };
      });
}
