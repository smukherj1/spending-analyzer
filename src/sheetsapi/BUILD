load("@io_bazel_rules_python//python:python.bzl", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "sheetsapi",
    srcs = [
        "__init__.py",
        "sheetsapi.py",
    ],
    visibility = ["//src:__pkg__"],
    deps = [
        requirement("google-api-python-client"),
        requirement("oauth2client"),
    ],
)
