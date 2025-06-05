{ pkgs }: {
  deps = [
    pkgs.python310Full
    pkgs.replitPackages.prybar-python310
    pkgs.replitPackages.stderred
    pkgs.tk
    pkgs.tcl
    pkgs.xorg.libX11
    pkgs.xorg.libXext
    pkgs.xorg.libXft
    pkgs.xorg.libXrender
    pkgs.fontconfig
    pkgs.freetype
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.tk
      pkgs.tcl
      pkgs.xorg.libX11
      pkgs.xorg.libXext
      pkgs.xorg.libXft
      pkgs.xorg.libXrender
      pkgs.fontconfig
      pkgs.freetype
    ];
    DISPLAY = ":0";
  };
}
