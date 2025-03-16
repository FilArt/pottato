{pkgs, ...}: {
  env.LOCALE_ARCHIVE = "${pkgs.glibcLocales}/lib/locale/locale-archive";

  # https://devenv.sh/packages/
  packages = with pkgs; [
    ruff
    mypy
  ];

  # https://devenv.sh/languages/
  # languages.rust.enable = true;
  languages.python = {
    enable = true;
    uv = {
      enable = true;
      sync = {
        enable = true;
        allExtras = true;
      };
    };
    venv.enable = true;
  };

  # https://devenv.sh/processes/
  # processes.cargo-watch.exec = "cargo-watch";

  # https://devenv.sh/services/
  services.postgres = {
    enable = true;
    listen_addresses = "127.0.0.1";
    port = 6699;
    initialDatabases = [
      {
        name = "postgres";
        pass = "postgres";
      }
    ];
  };

  # https://devenv.sh/scripts/
  scripts.hello.exec = ''
    echo hello from $GREET
  '';

  enterShell = ''
  '';

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  enterTest = ''
    uv run pytest tests/integration
  '';

  # https://devenv.sh/git-hooks/
  pre-commit.hooks = {
    alejandra.enable = true;
    check-added-large-files.enable = true;
    check-builtin-literals.enable = true;
    check-case-conflicts.enable = true;
    check-executables-have-shebangs.enable = true;
    check-shebang-scripts-are-executable.enable = true;
    check-json.enable = true;
    check-python.enable = true;
    check-toml.enable = true;
    check-yaml.enable = true;
    commitizen.enable = true;
    conform.enable = true;
    dialyzer.enable = true;
    editorconfig-checker.enable = true;
    end-of-file-fixer.enable = true;
    eslint.enable = true;
    flake-checker.enable = true;
    gitlint.enable = true;
    mypy = {
      enable = true;
      settings.binPath = ".devenv/state/venv/bin/mypy";
    };
    pylint = {
      enable = true;
      settings.binPath = ".devenv/state/venv/bin/pylint";
    };
    pyupgrade.enable = true;
    ripsecrets.enable = true;
    ruff.enable = true;
    ruff-format.enable = true;
  };

  # See full reference at https://devenv.sh/reference/options/
}
