# Use a resolved Path object as key to avoid loading the same conftest
# twice with build systems that create build directories containing
# symlinks to actual files.
# Using Path().resolve() is better than py.path.realpath because
# it resolves to the correct path/drive in case-insensitive file systems (#5792)
key = Path(str(conftestpath)).resolve()

with contextlib.suppress(KeyError):
    return self._conftestpath2mod[key]

pkgpath = conftestpath.pypkgpath()
if pkgpath is None:
    _ensure_removed_sysmodule(conftestpath.purebasename)

try:
    mod = import_path(conftestpath, mode=importmode)
except Exception as e:
    assert e.__traceback__ is not None
    exc_info = (type(e), e, e.__traceback__)
    raise ConftestImportFailure(conftestpath, exc_info) from e

self._check_non_top_pytest_plugins(mod, conftestpath)

self._conftest_plugins.add(mod)
self._conftestpath2mod[key] = mod
dirpath = conftestpath.dirpath()
if dirpath in self._dirpath2confmods:
    for path, mods in self._dirpath2confmods.items():
        if path and path.relto(dirpath) or path == dirpath:
            assert mod not in mods
            mods.append(mod)
self.trace(f"loading conftestmodule {mod!r}")
self.consider_conftest(mod)
return mod
