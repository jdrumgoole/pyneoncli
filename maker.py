import argparse
import os
import shutil
import subprocess

def run(args: list[str]) -> None:
    """Run a command."""
    print(f"Running: {' '.join(args)}")
    subprocess.run(args)

parser = argparse.ArgumentParser(description="Build and publish a Python package.")
parser.add_argument("target", default="all", choices=["all", "clean", "build", "test", "publish"], nargs="?",  help="Target to run")
parser.add_argument("--username", help="Username to use for publishing to PyPI")
parser.add_argument("--password", help="Password to use for publishing to PyPI")

args = parser.parse_args()

if args.target == "all":
    run(["python", __file__, "clean"])
    run(["python", __file__, "build"])
    run(["python", __file__, "test"])
elif args.target == "clean":
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("my_project.egg-info", ignore_errors=True)
    shutil.rmtree(".mypy_cache", ignore_errors=True)
    shutil.rmtree(".pytest_cache", ignore_errors=True)
    shutil.rmtree("htmlcov", ignore_errors=True)
    run(["poetry", "env", "remove"])
elif args.target == "build":
    run(["poetry", "install"])
    run(["poetry", "build"])
elif args.target == "test":
    run(["poetry", "run", "pytest", "--cov=my_project", "--cov-report=html"])
elif args.target == "publish":
    if not args.username or not args.password:
        print("Error: Must specify --username and --password to publish")
        exit(1)
    run(["poetry", "publish", "-u", args.username, "-p", args.password])
else:
    print(f"Error: Invalid target '{args.target}'")
    exit(1)
