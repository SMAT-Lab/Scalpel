importlib.invalidate_caches()
plugins = list(plugins)
finalizers = []
try:
    # Any sys.module or sys.path changes done while running pytest
    # inline should be reverted after the test run completes to avoid
    # clashing with later inline tests run within the same pytest test,
    # e.g. just because they use matching test module names.
    finalizers.append(self.__take_sys_modules_snapshot().restore)
    finalizers.append(SysPathsSnapshot().restore)

    # Important note:
    # - our tests should not leave any other references/registrations
    #   laying around other than possibly loaded test modules
    #   referenced from sys.modules, as nothing will clean those up
    #   automatically

    rec = []

    class Collect:
        def pytest_configure(x, config: Config) -> None:
            rec.append(self.make_hook_recorder(config.pluginmanager))

    plugins.append(Collect())
    ret = main([str(x) for x in args], plugins=plugins)
    if len(rec) == 1:
        reprec = rec.pop()
    else:

        class reprec:  # type: ignore
            pass

    reprec.ret = ret  # type: ignore

    # Typically we reraise keyboard interrupts from the child run
    # because it's our user requesting interruption of the testing.
    if ret == ExitCode.INTERRUPTED and not no_reraise_ctrlc:
        calls = reprec.getcalls("pytest_keyboard_interrupt")
        if calls and calls[-1].excinfo.type == KeyboardInterrupt:
            raise KeyboardInterrupt()
    return reprec
finally:
    for finalizer in finalizers:
        finalizer()
