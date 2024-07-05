{ pkgs ? import <nixpkgs> {} }:
with pkgs;
mkShell {
  buildInputs = [
    (python311.withPackages (py: [
      py.pygithub
    ]))
  ];
}
