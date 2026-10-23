{
  description = "A template for developing AI agents in Python";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      # Systems supported for development shells.
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
      ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          name = "template-agentic-project-dev";

          packages = with pkgs; [
            python314
            uv
            gnumake
            stdenv.cc
            cmake
            ninja
          ];

          UV_PYTHON = "${pkgs.python314}/bin/python3";
          UV_PYTHON_DOWNLOADS = "never";

          # Native wheels require runtime libraries and access to host GPU drivers.
          shellHook = pkgs.lib.optionalString pkgs.stdenv.hostPlatform.isLinux ''
            DRIVER_DIR="/run/opengl-driver/lib"
            if [ ! -d "$DRIVER_DIR" ]; then
              DRIVER_DIR="''${TMPDIR:-/tmp}/nix-gpu-drivers-$USER"
              mkdir -p "$DRIVER_DIR"
              for f in /usr/lib/x86_64-linux-gnu/libcuda* /usr/lib/x86_64-linux-gnu/libnvidia* /usr/lib/wsl/lib/libcuda*; do
                if [ -e "$f" ]; then
                  ln -sf "$f" "$DRIVER_DIR/" 2>/dev/null || true
                fi
              done
            fi

            export LD_LIBRARY_PATH="${
              pkgs.lib.makeLibraryPath [
                pkgs.stdenv.cc.cc.lib
                pkgs.zlib
              ]
            }:$DRIVER_DIR''${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
          '';
        };
      });

      formatter = forAllSystems (pkgs: pkgs.nixfmt-rfc-style or pkgs.nixfmt);
    };
}
