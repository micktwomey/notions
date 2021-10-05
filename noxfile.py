import nox


@nox.session()
def lint(session: nox.Session):
    session.install(".", "mypy", "black", "isort")
    session.run("mypy", ".")
    session.run("isort", "--check", ".")
    session.run("black", "--check", ".")


@nox.session(py=["3.8", "3.9", "3.10"])
def test(session: nox.Session):
    session.install(".")
    session.install("pytest")
    session.run("pytest")
