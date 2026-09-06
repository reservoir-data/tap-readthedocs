"""Stream type classes for tap-readthedocs."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, override

from singer_sdk import typing as th
from toolz.dicttoolz import update_in

from tap_readthedocs.client import ReadTheDocsStream

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context

logger = logging.getLogger(__name__)

# A value that is either a string or a list of strings.
_STRING_OR_LIST = th.CustomType(
    {"type": ["array", "string"], "items": {"type": ["string"]}},
)


class Projects(ReadTheDocsStream):
    """Projects stream."""

    name = "projects"
    path = "/api/v3/projects/"
    primary_keys = ("id",)

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("slug", th.StringType),
        th.Property("created", th.DateTimeType),
        th.Property("modified", th.DateTimeType),
        th.Property(
            "language",
            th.ObjectType(
                th.Property("code", th.StringType),
                th.Property("name", th.StringType),
                additional_properties=True,
            ),
        ),
        th.Property(
            "programming_language",
            th.ObjectType(
                th.Property("code", th.StringType),
                th.Property("name", th.StringType),
                additional_properties=True,
            ),
        ),
        th.Property(
            "repository",
            th.ObjectType(
                th.Property("url", th.StringType),
                th.Property("type", th.StringType),
                additional_properties=True,
            ),
        ),
        th.Property("default_version", th.StringType),
        th.Property("default_branch", th.StringType),
        th.Property("subproject_of", th.IntegerType),
        th.Property("translation_of", th.IntegerType),
        th.Property(
            "urls",
            th.ObjectType(
                th.Property("documentation", th.StringType),
                th.Property("home", th.StringType),
                th.Property("builds", th.StringType),
                th.Property("versions", th.StringType),
                th.Property("downloads", th.StringType),
                additional_properties=True,
            ),
        ),
        th.Property("tags", th.ArrayType(th.StringType)),
        th.Property(
            "users",
            th.ArrayType(
                th.ObjectType(
                    th.Property("username", th.StringType),
                ),
            ),
        ),
        th.Property("active_versions", th.ObjectType()),
        th.Property("homepage", th.StringType),
        th.Property("external_builds_privacy_level", th.StringType),
        th.Property("privacy_level", th.StringType),
        th.Property("single_version", th.BooleanType),
        th.Property("versioning_scheme", th.StringType),
        th.Property("readthedocs_yaml_path", th.StringType),
        th.Property("_links", th.ObjectType(additional_properties=True)),
    ).to_dict()

    @override
    def get_child_context(
        self,
        record: dict[str, Any],
        context: Context | None,
    ) -> dict[str, Any] | None:
        return {"project_slug": record["slug"]}


class Versions(ReadTheDocsStream):
    """Versions stream."""

    name = "versions"
    path = "/api/v3/projects/{project_slug}/versions"
    primary_keys = ("id",)
    parent_stream_type = Projects

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("project_slug", th.StringType),
        th.Property("slug", th.StringType),
        th.Property("verbose_name", th.StringType),
        th.Property("identifier", th.StringType),
        th.Property("ref", th.StringType),
        th.Property("built", th.BooleanType),
        th.Property("active", th.BooleanType),
        th.Property("hidden", th.BooleanType),
        th.Property("type", th.StringType),
        th.Property("last_build", th.IntegerType),
        th.Property("downloads", th.ObjectType()),
        th.Property("urls", th.ObjectType()),
    ).to_dict()


class Builds(ReadTheDocsStream):
    """Builds stream."""

    name = "builds"
    path = "/api/v3/projects/{project_slug}/builds"
    primary_keys = ("id",)
    parent_stream_type = Projects

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("project_slug", th.StringType),
        th.Property("version", th.StringType),
        th.Property("project", th.StringType),
        th.Property("created", th.DateTimeType),
        th.Property("finished", th.DateTimeType),
        th.Property("duration", th.IntegerType),
        th.Property(
            "state",
            th.ObjectType(
                th.Property("code", th.StringType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("success", th.BooleanType),
        th.Property("error", th.StringType),
        th.Property("commit", th.StringType),
        th.Property("urls", th.ObjectType()),
        th.Property(
            "config",
            th.ObjectType(
                th.Property("version", th.StringType),
                th.Property("formats", th.ArrayType(th.StringType)),
                th.Property("doctype", th.StringType),
                th.Property(
                    "conda",
                    th.ObjectType(
                        th.Property("environment", th.StringType),
                        additional_properties=True,
                    ),
                ),
                th.Property(
                    "build",
                    th.ObjectType(
                        # Legacy (config version 1) field.
                        th.Property("image", th.StringType),
                        th.Property("os", th.StringType),
                        th.Property("apt_packages", th.ArrayType(th.StringType)),
                        th.Property("commands", th.ArrayType(th.StringType)),
                        th.Property(
                            "tools",
                            th.ObjectType(
                                th.Property(
                                    "python",
                                    th.ObjectType(
                                        th.Property("version", th.StringType),
                                        th.Property("full_version", th.StringType),
                                        additional_properties=True,
                                    ),
                                ),
                                th.Property(
                                    "nodejs",
                                    th.ObjectType(
                                        th.Property("version", th.StringType),
                                        th.Property("full_version", th.StringType),
                                        additional_properties=True,
                                    ),
                                ),
                                th.Property(
                                    "ruby",
                                    th.ObjectType(
                                        th.Property("version", th.StringType),
                                        th.Property("full_version", th.StringType),
                                        additional_properties=True,
                                    ),
                                ),
                                th.Property(
                                    "rust",
                                    th.ObjectType(
                                        th.Property("version", th.StringType),
                                        th.Property("full_version", th.StringType),
                                        additional_properties=True,
                                    ),
                                ),
                                th.Property(
                                    "golang",
                                    th.ObjectType(
                                        th.Property("version", th.StringType),
                                        th.Property("full_version", th.StringType),
                                        additional_properties=True,
                                    ),
                                ),
                                additional_properties=True,
                            ),
                        ),
                        th.Property(
                            "jobs",
                            th.ObjectType(
                                th.Property(
                                    "pre_checkout",
                                    th.ArrayType(th.StringType),
                                ),
                                th.Property(
                                    "post_checkout",
                                    th.ArrayType(th.StringType),
                                ),
                                th.Property(
                                    "pre_system_dependencies",
                                    th.ArrayType(th.StringType),
                                ),
                                th.Property(
                                    "post_system_dependencies",
                                    th.ArrayType(th.StringType),
                                ),
                                th.Property(
                                    "pre_create_environment",
                                    th.ArrayType(th.StringType),
                                ),
                                th.Property(
                                    "create_environment",
                                    th.ArrayType(th.StringType),
                                ),
                                th.Property(
                                    "post_create_environment",
                                    th.ArrayType(th.StringType),
                                ),
                                th.Property("pre_install", th.ArrayType(th.StringType)),
                                th.Property("install", th.ArrayType(th.StringType)),
                                th.Property(
                                    "post_install",
                                    th.ArrayType(th.StringType),
                                ),
                                th.Property("pre_build", th.ArrayType(th.StringType)),
                                th.Property(
                                    "build",
                                    th.ObjectType(
                                        th.Property("html", _STRING_OR_LIST),
                                        th.Property("htmlzip", _STRING_OR_LIST),
                                        th.Property("pdf", _STRING_OR_LIST),
                                        th.Property("epub", _STRING_OR_LIST),
                                        additional_properties=True,
                                    ),
                                ),
                                th.Property("post_build", th.ArrayType(th.StringType)),
                                additional_properties=True,
                            ),
                        ),
                        additional_properties=True,
                    ),
                ),
                th.Property(
                    "python",
                    th.ObjectType(
                        th.Property("version", th.StringType),
                        th.Property("use_system_site_packages", th.BooleanType),
                        th.Property(
                            "install",
                            th.ArrayType(
                                th.ObjectType(
                                    th.Property("requirements", th.StringType),
                                    th.Property("method", th.StringType),
                                    th.Property("path", th.StringType),
                                    th.Property(
                                        "extra_requirements",
                                        th.ArrayType(th.StringType),
                                    ),
                                    # uv-specific fields.
                                    th.Property("command", th.StringType),
                                    th.Property("groups", _STRING_OR_LIST),
                                    th.Property("extras", _STRING_OR_LIST),
                                    additional_properties=True,
                                ),
                            ),
                        ),
                        additional_properties=True,
                    ),
                ),
                th.Property(
                    "sphinx",
                    th.ObjectType(
                        th.Property("builder", th.StringType),
                        th.Property("configuration", th.StringType),
                        th.Property("fail_on_warning", th.BooleanType),
                        additional_properties=True,
                    ),
                ),
                th.Property(
                    "mkdocs",
                    th.ObjectType(
                        th.Property("configuration", th.StringType),
                        th.Property("fail_on_warning", th.BooleanType),
                        additional_properties=True,
                    ),
                ),
                th.Property(
                    "submodules",
                    th.ObjectType(
                        th.Property("include", _STRING_OR_LIST),
                        th.Property("exclude", _STRING_OR_LIST),
                        th.Property("recursive", th.BooleanType),
                        additional_properties=True,
                    ),
                ),
                th.Property(
                    "search",
                    th.ObjectType(
                        th.Property(
                            "ranking",
                            th.ObjectType(additional_properties=True),
                        ),
                        th.Property("ignore", th.ArrayType(th.StringType)),
                        additional_properties=True,
                    ),
                ),
                additional_properties=True,
            ),
        ),
    ).to_dict()

    @override
    def post_process(
        self,
        row: dict[str, Any],
        context: Context | None = None,
    ) -> dict[str, Any] | None:
        if row["config"]:
            row = update_in(row, ["config", "python", "version"], str, "")  # ty:ignore[no-matching-overload]
        return row


class Subprojects(ReadTheDocsStream):
    """Subprojects stream."""

    name = "subprojects"
    path = "/api/v3/projects/{project_slug}/subprojects"
    primary_keys = ("alias",)
    parent_stream_type = Projects

    schema = th.PropertiesList(
        th.Property("alias", th.StringType),
        th.Property(
            "child",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("slug", th.StringType),
                th.Property("created", th.DateTimeType),
                th.Property("modified", th.DateTimeType),
                th.Property(
                    "language",
                    th.ObjectType(
                        th.Property("code", th.StringType),
                        th.Property("name", th.StringType),
                        additional_properties=True,
                    ),
                ),
                th.Property(
                    "programming_language",
                    th.ObjectType(
                        th.Property("code", th.StringType),
                        th.Property("name", th.StringType),
                        additional_properties=True,
                    ),
                ),
                th.Property(
                    "repository",
                    th.ObjectType(
                        th.Property("url", th.StringType),
                        th.Property("type", th.StringType),
                        additional_properties=True,
                    ),
                ),
                th.Property("default_version", th.StringType),
                th.Property("default_branch", th.StringType),
                th.Property(
                    "translation_of",
                    th.ObjectType(
                        th.Property("slug", th.StringType),
                        th.Property(
                            "_links", th.ObjectType(additional_properties=True)
                        ),
                        additional_properties=True,
                    ),
                ),
                th.Property(
                    "urls",
                    th.ObjectType(
                        th.Property("documentation", th.StringType),
                        th.Property("home", th.StringType),
                        th.Property("builds", th.StringType),
                        th.Property("versions", th.StringType),
                        th.Property("downloads", th.StringType),
                        additional_properties=True,
                    ),
                ),
                th.Property("tags", th.ArrayType(th.StringType)),
                th.Property(
                    "users",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("username", th.StringType),
                        ),
                    ),
                ),
                th.Property("homepage", th.StringType),
                th.Property("external_builds_privacy_level", th.StringType),
                th.Property("privacy_level", th.StringType),
                th.Property("single_version", th.BooleanType),
                th.Property("versioning_scheme", th.StringType),
                th.Property("readthedocs_yaml_path", th.StringType),
                th.Property("_links", th.ObjectType(additional_properties=True)),
                additional_properties=True,
            ),
        ),
        th.Property(
            "_links",
            th.ObjectType(
                th.Property("_self", th.StringType),
                th.Property("parent", th.StringType),
                additional_properties=True,
            ),
        ),
    ).to_dict()


class Translations(ReadTheDocsStream):
    """Translations stream."""

    name = "translations"
    path = "/api/v3/projects/{project_slug}/translations"
    primary_keys = ("id",)
    parent_stream_type = Projects

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("slug", th.StringType),
        th.Property("created", th.DateTimeType),
        th.Property("modified", th.DateTimeType),
        th.Property(
            "language",
            th.ObjectType(
                th.Property("code", th.StringType),
                th.Property("name", th.StringType),
                additional_properties=True,
            ),
        ),
        th.Property(
            "programming_language",
            th.ObjectType(
                th.Property("code", th.StringType),
                th.Property("name", th.StringType),
                additional_properties=True,
            ),
        ),
        th.Property(
            "repository",
            th.ObjectType(
                th.Property("url", th.StringType),
                th.Property("type", th.StringType),
                additional_properties=True,
            ),
        ),
        th.Property("default_version", th.StringType),
        th.Property("default_branch", th.StringType),
        th.Property(
            "subproject_of",
            th.ObjectType(
                th.Property("slug", th.StringType),
                th.Property("_links", th.ObjectType(additional_properties=True)),
                additional_properties=True,
            ),
        ),
        th.Property(
            "translation_of",
            th.ObjectType(
                th.Property("slug", th.StringType),
                th.Property("_links", th.ObjectType(additional_properties=True)),
                additional_properties=True,
            ),
        ),
        th.Property(
            "urls",
            th.ObjectType(
                th.Property("documentation", th.StringType),
                th.Property("home", th.StringType),
                th.Property("builds", th.StringType),
                th.Property("versions", th.StringType),
                th.Property("downloads", th.StringType),
                additional_properties=True,
            ),
        ),
        th.Property("tags", th.ArrayType(th.StringType)),
        th.Property(
            "users",
            th.ArrayType(
                th.ObjectType(
                    th.Property("username", th.StringType),
                ),
            ),
        ),
        th.Property("homepage", th.StringType),
        th.Property("external_builds_privacy_level", th.StringType),
        th.Property("privacy_level", th.StringType),
        th.Property("single_version", th.BooleanType),
        th.Property("versioning_scheme", th.StringType),
        th.Property("readthedocs_yaml_path", th.StringType),
        th.Property("_links", th.ObjectType(additional_properties=True)),
    ).to_dict()


class Redirects(ReadTheDocsStream):
    """Redirects stream."""

    name = "redirects"
    path = "/api/v3/projects/{project_slug}/redirects"
    primary_keys = ("id",)
    parent_stream_type = Projects

    # TODO(edgarrmondragon): get the complete schema
    # https://github.com/reservoir-data/tap-readthedocs/issues/2
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        # TODO(edgarrmondragon): Inform max length of 255
        # https://github.com/reservoir-data/tap-readthedocs/issues/295
        th.Property("redirect_type", th.StringType),
        # TODO(edgarrmondragon): Inform max length of 255
        # https://github.com/reservoir-data/tap-readthedocs/issues/295
        th.Property(
            "from_url",
            th.StringType,
            description="Absolute path, excluding the domain",
            examples=["/docs/", "/install.html"],
        ),
        # TODO(edgarrmondragon): Inform max length of 255
        # https://github.com/reservoir-data/tap-readthedocs/issues/295
        th.Property(
            "to_url",
            th.StringType,
            description="Absolute or relative URL",
            examples=["/tutorial/install.html"],
        ),
        th.Property(
            "force",
            th.BooleanType,
            description="Apply the redirect even if the page exists",
        ),
        # TODO(edgarrmondragon): Inform "small" integer
        # https://github.com/reservoir-data/tap-readthedocs/issues/295
        th.Property(
            "http_status",
            th.IntegerType,
            description="HTTP status code for the redirect",
        ),
        th.Property("enabled", th.BooleanType),
        # TODO(edgarrmondragon): Inform max length of 255
        # https://github.com/reservoir-data/tap-readthedocs/issues/295
        th.Property("description", th.StringType),
        # TODO(edgarrmondragon): Inform positive integer
        # https://github.com/reservoir-data/tap-readthedocs/issues/295
        th.Property(
            "position",
            th.IntegerType,
            description="Order of execution of the redirect",
        ),
        th.Property("create_dt", th.DateTimeType),
        th.Property("update_dt", th.DateTimeType),
    ).to_dict()


class Organizations(ReadTheDocsStream):
    """Organizations stream."""

    name = "organizations"
    path = "/api/v3/organizations/"
    primary_keys = ("slug",)

    schema = th.PropertiesList(
        th.Property("slug", th.StringType),
        th.Property("name", th.StringType),
        th.Property("url", th.StringType),
        th.Property("email", th.StringType),
        th.Property("description", th.StringType),
        th.Property("created", th.DateTimeType),
        th.Property("modified", th.DateTimeType),
        th.Property("disabled", th.BooleanType),
        th.Property(
            "owners",
            th.ArrayType(
                th.ObjectType(
                    th.Property("username", th.StringType),
                ),
            ),
        ),
    ).to_dict()
