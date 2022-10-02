import nox

nox.options.sessions = ["build"]


@nox.session
def build(session):
    session.install("-r", "requirements.txt")
    session.run("python", "scripts/make-ninja-build.py")
    session.run("ninja", "-f", "build/build.ninja")


@nox.session
def adjust(session):
    session.install("-r", "requirements.txt")
    session.run("python", "scripts/adjust-sources.py")
    session.run("python", "scripts/update-anchor-propagation-includes.py")
