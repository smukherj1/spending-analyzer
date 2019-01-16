load("@io_bazel_rules_python//python:python.bzl", "py_binary")

py_binary(
    name = "analyze",
    srcs = ["analyze.py"],
    main = "analyze.py",
    deps = [
        "//src/driveapi",
        "//src/sheetsapi",
    ],
)
