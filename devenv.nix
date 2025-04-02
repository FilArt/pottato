{pkgs, ...}: {
  env = {
    PYTHONASYNCIODEBUG = 1;
    DB_URL = "asyncpg://localhost:6699/postgres";
    DEBUG = true;
  };
  # https://devenv.sh/packages/
  packages = with pkgs; [
    ruff
    mypy
  ];

  # https://devenv.sh/languages/
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

  enterTest = ''
    uv run --group test pytest tests/integration
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
    dialyzer.enable = true;
    editorconfig-checker.enable = true;
    end-of-file-fixer.enable = true;
    eslint.enable = true;
    flake-checker.enable = true;
    pyupgrade.enable = true;
    ripsecrets.enable = true;
    ruff.enable = true;
    ruff-format.enable = true;
  };

  scripts = {
    migrate.exec = "alembic upgrade head";
    downgrade.exec = "alembic downgrade -1";
    makemigrations.exec = "alembic revision --autogenerate -m $1";
    "test:int".exec = "uv run --group test pytest tests/integration";
    run.exec = "uv run uvicorn run:server --reload";
  };
}
