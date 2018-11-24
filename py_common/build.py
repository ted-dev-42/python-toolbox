import subprocess
import sys
from collections import namedtuple
from py_modules.pathlib2 import Path
import utils
import fsutils

working_path = None  # type: Path
build_dir = None  # type: Path
dist_dir = None  # type: Path
build_config = None  # type: namedtuple


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
            fsutils.copy(src, dest)


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
    working_path, config_file = get_config_file_dir_name(sys.argv[1])
    build_config = load_build_config(config_file)
    build_dir = get_build_dir()
    if build_dir.exists():
        fsutils.remove(str(build_dir))
    dist_dir = get_dist_dir()


def build():
    print('building ...')
    init()
    copy_project_file(build_config.project_files)
    pack()


def load_build_config(config_file):
    # type: (Path) -> namedtuple
    if not config_file.exists():
        print('config file not exits')
        sys.exit(1)

    with config_file.open() as f:
        return utils.json2obj(f.read())


def get_config_file_dir_name(config_file):
    # type: (str) -> (Path, Path)
    config_path = Path(config_file).resolve()
    dir_name = config_path.parent
    file_name = config_path.name
    print("config file location: {}, name: {}".format(dir_name, file_name))
    return dir_name, config_path


def get_dist_name():
    return "{}_{}.zip".format(dist_dir.joinpath(build_config.name), get_version())


def get_version():
    import config
    config.load(str(build_dir.joinpath('config.xml')))
    return config.get_version()


def pack():
    dist_dir.parent.mkdir(parents=True, exist_ok=True)

    cmd = "7za a {} {}".format(get_dist_name(), get_build_dir())
    cmd_proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output = cmd_proc.communicate()[0]
    print(output)
    if cmd_proc.returncode == 0:
        print("pack success")
    else:
        print("pack failed")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("must specify a build config file")
        sys.exit(1)
    build()
