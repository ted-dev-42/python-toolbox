import logging
import os
import subprocess
import sys
from collections import namedtuple

from pathlib2 import Path
import utils
import fsutils

working_path = None  # type: Path
build_dir = None  # type: Path
dist_dir = None  # type: Path
build_config = None  # type: namedtuple
DEFAULT_INSTALL_DEST = Path("py_common/py_modules")


def copy_project_file(dir_list):
    for d in dir_list:
        for f in d.files:
            if f[1] == "":
                f[1] = f[0]
            src_path = Path(d.src_dir)
            if src_path.is_absolute():
                src = src_path.joinpath(f[0])
            else:
                src = working_path.joinpath(d.src_dir, f[0])
            dest = build_dir.joinpath(f[1])
            print("copy {} to {}".format(src, dest))

            try:
                ign = d.ignores
            except AttributeError:
                ign = None
            fsutils.copy(src, dest, ign)


def get_build_dir():
    build_path = Path(build_config.build_dir)
    if build_path.is_absolute():
        return build_path.joinpath(build_config.name)
    else:
        return Path(working_path).joinpath(build_config.build_dir, build_config.name)


def get_dist_dir():
    dist_path = Path(build_config.dist_dir)
    if dist_path.is_absolute():
        return dist_path
    return Path(working_path).joinpath(build_config.dist_dir)


def init():
    global working_path
    global build_config
    global build_dir
    global dist_dir
    working_path, config_file = get_config_file(sys.argv[1])
    build_config = load_build_config(config_file)
    build_dir = get_build_dir()
    if build_dir.exists():
        fsutils.remove(str(build_dir))
    dist_dir = get_dist_dir()
    # save_version()


def build():
    print('building ...')
    init()
    copy_project_file(build_config.project_files)
    try:
        install_modules(build_config.install)
    except AttributeError:
        pass
    pack()


def install_modules(install_config):
    if install_config is None:
        return

    try:
        dest = get_build_dir().joinpath(install_config.dest)
    except AttributeError:
        dest = get_build_dir().joinpath(DEFAULT_INSTALL_DEST)

    import lib_installer_legacy as installer
    installer.init(install_config.libs_dir)
    for m in install_config.modules:
        installer.install(m, dest)


def load_build_config(config_file):
    # type: (Path) -> namedtuple
    if not config_file.exists():
        print('config file not exits')
        sys.exit(1)

    with config_file.open() as f:
        return utils.json2obj(f.read())


def get_config_file(config_file):
    # type: (str) -> (Path, Path)
    config_path = Path(config_file).resolve()
    dir_name = config_path.parent
    file_name = config_path.name
    print("config file location: {}, name: {}".format(dir_name, file_name))
    return dir_name, config_path


def get_dist_name():
    version = get_version()
    dist_file_path = dist_dir.joinpath(build_config.name)
    if version == "":
        return "{}.zip".format(dist_file_path)
    else:
        return "{}_{}.zip".format(dist_file_path, version)


def get_version_file():
    try:
        return str(working_path.joinpath(build_config.version_file))
    except AttributeError:
        pass

    if working_path.joinpath("version").exists():
        return "version"
    elif working_path.joinpath("VERSION").exists():
        return "VERSION"
    else:
        return None


def get_version():
    # if build_dir.joinpath('config.xml').exists():
    #     import config
    #     config.load(str(build_dir.joinpath('config.xml')))
    #     return config.get_version()
    # else:
    version_file = get_version_file()
    if version_file is None:
        return ""
    return fsutils.read_file(version_file).strip()


# def save_version():
#     with open('VERSION', 'w') as vf:
#         vf.write(build_config.version)


def pack():
    dist_dir.parent.mkdir(parents=True, exist_ok=True)

    dist_file_name = get_dist_name()
    if os.path.exists(dist_file_name):
        fsutils.remove(dist_file_name)

    try:
        exclude_root = build_config.pack.exclude_root_dir
    except AttributeError:
        exclude_root = False

    if exclude_root:
        target_dir = '.'
        cwd = str(get_build_dir())
    else:
        target_dir = get_build_dir()
        cwd = None

    if utils.get_os() == 'windows':
        cmd = "7za a {} {}".format(get_dist_name(), get_build_dir())
    else:
        cmd = "zip -r {} {}".format(get_dist_name(), target_dir)

    cmd_proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, cwd=cwd)
    output = cmd_proc.communicate()[0]
    print(output)
    if cmd_proc.returncode == 0:
        print("pack success")
    else:
        print("pack failed")


def init_log():
    logging.basicConfig(level=logging.DEBUG,
                        stream=sys.stdout,
                        format='[BUILD]%(asctime)s [%(levelname)s] %(message)s (%(filename)s[%(lineno)d])',
                        datefmt='%m-%d %H:%M:%S')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("must specify a build config file")
        sys.exit(1)
    build()
