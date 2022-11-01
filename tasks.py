from invoke import task

@task(iterable=["exec"],
help={"exec": "Specify which tests to execute. Available options mypy, unit"}
)
def test(c, exec=None):
    """Execute test cases"""
    exec = exec or ["mypy", "isort", "black", "unit"]
    print(f"Executing tests {exec}:")
    if "mypy" in exec:
        print("Running mypy...")
        c.run("mypy src")
        print()
    if "isort" in exec:
        print("Running isort...")
        c.run("isort src")
        print()
    if "black" in exec:
        print("Running black...")
        c.run("black src")
        print()
    if "unit" in exec:
        print("Running pytest...")
        c.run("pytest --cov")
