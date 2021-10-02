import nox

nox.options.sessions = ["lint"]
locations = (
    "discord",
    "setup.py",
    "noxfile.py",
)


@nox.session(python="3.9")
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
