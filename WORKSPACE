workspace(name = "spending_analyzer")

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "io_bazel_rules_python",
    commit = "ebd7adcbcafcc8abe3fd8e5b0e42e10ced1bfe27",
    remote = "https://github.com/bazelbuild/rules_python.git",
)

# Only needed for PIP support:
load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories")

pip_repositories()

load("@io_bazel_rules_python//python:pip.bzl", "pip_import")

# This rule translates the specified requirements.txt into
# @py_deps//:requirements.bzl, which itself exposes a pip_install method.
pip_import(
    name = "py_deps",
    requirements = ":requirements.txt",
)

# Load the pip_install symbol for my_deps, and create the dependencies'
# repositories.
load("@py_deps//:requirements.bzl", "pip_install")

pip_install()

# The end.

