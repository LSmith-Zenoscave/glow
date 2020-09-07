from tests.fixtures import *


def pytest_generate_tests(metafunc):
    """Creates scenario capabilities a la [testscenarios](https://pypi.org/project/testscenarios/)

    Taken from [here](https://docs.pytest.org/en/stable/example/parametrize.html)
    Now with fixture secnarios...
    """
    if hasattr(metafunc.cls, "scenarios"):
        idlist = []
        argvalues = []
        argnames = set()
        for scenario in metafunc.cls.scenarios:
            idlist.append(scenario["Name"])
            items = scenario["Values"].items()
            argnames |= {x[0] for x in items}
            argvalues.append([x[1] for x in items])

        metafunc.parametrize(list(argnames), argvalues,
                             ids=idlist, scope="class")

    for fixture in metafunc.fixturenames:
        scenarios = getattr(metafunc.cls, f"{fixture}_scenarios", [])
        if scenarios:
            metafunc.parametrize(fixture, scenarios, indirect=True)
