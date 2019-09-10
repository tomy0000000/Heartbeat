"""Boot Script of Tubee"""
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

COV = None
if os.environ.get("FLASK_COVERAGE"):
    import coverage
    COV = coverage.coverage(branch=True, include="app/*")
    COV.start()

import sys
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate()
with app.app_context():
    migrate.init_app(app, db, render_as_batch=True)

@app.cli.command()
@click.option("--coverage/--no-coverage", default=False,
              help="Run tests under code coverage.")
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get("FLASK_COVERAGE"):
        import subprocess
        os.environ["FLASK_COVERAGE"] = "1"
        sys.exit(subprocess.call(sys.argv))

    import unittest
    tests = unittest.TestLoader().discover("tests")
    results = unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, "htmlcov")
        COV.html_report(directory=covdir)
        print("HTML version: file://%s/index.html" % covdir)
    sys.exit(not results.wasSuccessful())

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

if __name__ == "__main__":
    app.run()
