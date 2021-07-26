import nox


@nox.session(py=["3.8", "3.9", "3.10"])
def test(session: nox.Session):
    session.install(".")
    session.install("pytest")
    session.run("pytest")
