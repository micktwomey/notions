import nox


@nox.session()
def lint(session: nox.Session):
    session.install(
        ".",
        "mypy",
        "black",
        "isort",
        "types-PyYAML",
        "iso8601",
        "pytest",
        "httpx",
        "typer",
        "nox",
    )
    session.run("mypy", ".")
    session.run("isort", "--check", ".")
    session.run("black", "--check", ".")


@nox.session(py=["3.9", "3.10", "3.11"])
def test(session: nox.Session):
    session.install(".", "pytest", "iso8601")
    session.run("pytest")
