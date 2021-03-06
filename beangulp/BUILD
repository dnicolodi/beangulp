package(default_visibility = ["//visibility:public"])

py_library(
    name = "importer",
    srcs = [
        "importer.py",
    ],
    deps = [
        "//beancount/core:flags",
    ],
)

py_test(
    name = "importer_test",
    srcs = [
        "importer_test.py",
    ],
    deps = [
        ":importer",
        ":cache",
    ],
)

py_library(
    name = "cache",
    srcs = [
        "cache.py",
    ],
    deps = [
        "//beangulp:file_type",
        "//beangulp:defdict",
    ],
)

py_test(
    name = "cache_test",
    srcs = [
        "cache_test.py",
    ],
    deps = [
        ":cache",
        "//beangulp:file_type",
    ],
)

py_library(
    name = "scripts_utils",
    srcs = [
        "scripts_utils.py",
    ],
    deps = [
        "//beancount/ingest:importer",
        "//beancount/ingest:cache",
        "//beangulp:test_utils",
        "//beancount/parser:version",
        "//beancount/ingest:identify",
        "//beancount/ingest:extract",
        "//beancount/ingest:file",
    ],
)

py_test(
    name = "scripts_utils_test",
    srcs = [
        "scripts_utils_test.py",
    ],
    deps = [
        ":scripts_utils",
        "//beangulp:test_utils",
        "//beancount/ingest:extract",
    ],
)

py_library(
    name = "similar",
    srcs = [
        "similar.py",
    ],
    deps = [
        "//beancount/core:number",
        "//beancount/core:data",
        "//beancount/core:amount",
        "//beancount/core:interpolate",
    ],
)

py_test(
    name = "similar_test",
    srcs = [
        "similar_test.py",
    ],
    deps = [
        ":similar",
        "//beancount/core:number",
        "//beancount/core:data",
        "//beancount/parser:cmptest",
        "//beancount/parser:parser",
        "//beancount:loader",
        "//beancount/ops:pad",
        "//beancount/ops:documents",
        "//beancount/plugins:auto_accounts",
        "//beancount/ops:balance",
    ],
)

py_library(
    name = "extract",
    srcs = [
        "extract.py",
    ],
    deps = [
        ":similar",
        ":identify",
        ":cache",
        "//beancount/core:data",
        "//beancount/parser:printer",
        "//beancount:loader",
    ],
)

py_test(
    name = "extract_test",
    srcs = [
        "extract_test.py",
    ],
    data = [
        "//examples:example",
        "//examples/ingest:office_files",
    ],
    deps = [
        ":extract",
        "//examples/ingest:office",
        "//beangulp:test_utils",
        "//beangulp:misc_utils",
        "//beancount/parser:parser",
        "//beancount:loader",
        "//beancount/ingest:importer",
        "//beancount/ingest:scripts_utils",
    ],
)

py_library(
    name = "file",
    srcs = [
        "file.py",
    ],
    deps = [
        ":identify",
        "//beancount/core:account",
        "//beangulp:misc_utils",
        "//beancount/ingest:cache",
    ],
)

py_test(
    name = "file_test",
    srcs = [
        "file_test.py",
    ],
    data = [
        "//examples:example",
        "//examples/ingest:office_files",
    ],
    deps = [
        ":file",
        ":scripts_utils",
        "//examples/ingest:office",
        "//beangulp:test_utils",
        "//beangulp:file_utils",
    ],
)

py_library(
    name = "identify",
    srcs = [
        "identify.py",
    ],
    deps = [
        ":cache",
        "//beangulp:file_utils",
    ],
)

py_test(
    name = "identify_test",
    srcs = [
        "identify_test.py",
    ],
    data = [
        "//examples:example",
        "//examples/ingest:office_files",
    ],
    deps = [
        ":identify",
        "//examples/ingest:office",
        "//beangulp:test_utils",
        "//beancount/ingest:importer",
        "//beancount/ingest:scripts_utils",
    ],
)

py_library(
    name = "regression",
    srcs = [
        "regression.py",
    ],
    deps = [
        "//beancount/ingest:importer",
        "//beancount/parser:printer",
        "//beangulp:test_utils",
        "//beangulp:misc_utils",
        "//beancount/ingest:extract",
        "//beancount/ingest:cache",
    ],
)

py_library(
    name = "regression_pytest",
    srcs = [
        "regression_pytest.py",
    ],
    deps = [
        "//beancount/ingest:cache",
        "//beancount/ingest:extract",
        "//beancount/parser:printer",
    ],
)

py_test(
    name = "regression_test",
    srcs = [
        "regression_test.py",
    ],
    deps = [
        ":regression",
        "//beangulp:test_utils",
        "//beancount/parser:parser",
        "//beancount/ingest:importer",
    ],
)

py_library(
    name = "file_type",
    srcs = ["file_type.py"],
    deps = [
        "@python_magic//:magic"
    ],
)

py_test(
    name = "file_type_test",
    srcs = ["file_type_test.py"],
    data = glob(["file_type_testdata/*"]),
    deps = [
        ":file_type",
    ],
)
