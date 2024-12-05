{
  description = "Hugo";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      # Dev shell for development
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          hugo
          git
        ];
      };

      apps.${system}.default = {
        type = "app";
        program = "${pkgs.writeShellScript "run-hugo-server" ''
          ${pkgs.hugo}/bin/hugo server
        ''}";
      };
      # Build the static site
      packages.default = pkgs.stdenv.mkDerivation {
        name = "hugo-static-site";
        src = ./.;
        buildInputs = [pkgs.hugo];
        buildPhase = ''
          hugo --minify
        '';
        installPhase = ''
          mkdir -p $out
          cp -r public/* $out
        '';
      };
    });
}
