{ pkgs ? import <nixpkgs> {} }:
with pkgs;
mkShell {
  buildInputs = [
    (python311.withPackages (py: [
      py.pygithub
      py.gitpython
    ]))
    python311Packages.python-lsp-server

    # nix-prefetch-git will use whatever git is in scope, which may or
    # may not be configured to allow file clones. We can easily make
    # it take the required configuration by wrapping git to inject an
    # extra argument.
    (nix-prefetch-git.override {
      git = writeShellScriptBin "git" ''
${git.out}/bin/git -c protocol.file.allow=always "$@"
'';
    })
  ];
}
