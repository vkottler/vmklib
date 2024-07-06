"""
A module implementing a release task for Python projects.
"""

# built-in
from json import loads
import os
from pathlib import Path
from typing import Any, Dict

# third-party
from vcorelib.task import Inbox, Outbox

# internal
from vmklib.tasks.github import COMMON_ARGS, ensure_api_token, repo_url
from vmklib.tasks.mixins import CurlMixin, curl_headers

ApiResult = Dict[str, Any]


class GithubRelease(CurlMixin):
    """A task for creating a GitHub release for a given package."""

    async def create_release(
        self, owner: str, repo: str, data: Dict[str, Any]
    ) -> ApiResult:  # pragma: nocover
        """Attempt to create a release."""

        result = await self.curl(
            *COMMON_ARGS, repo_url(owner, repo), post_data=data
        )
        return loads(result.stdout)  # type: ignore

    async def upload_release_asset(
        self, owner: str, repo: str, release_id: int, path: Path
    ) -> ApiResult:  # pragma: nocover
        """Attempt to upload a release asset."""

        result = await self.curl(
            *COMMON_ARGS,
            (
                f"{repo_url(owner, repo, kind='uploads')}/{release_id}/assets"
                f"?name={path.name}"
            ),
            *curl_headers({"Content-Type": "application/octet-stream"}),
            "--data-binary",
            f"@{path}",
            method="POST",
        )
        return loads(result.stdout)  # type: ignore

    async def release(
        self,
        cwd: Path,
        owner: str,
        repo: str,
        version: str,
        dist: str = "dist",
    ) -> bool:  # pragma: nocover
        """Create a release."""

        # Check for API key in environment.
        if "GITHUB_API_TOKEN" not in os.environ:
            self.log.error(
                "Environment variable 'GITHUB_API_TOKEN' is not set!"
            )
            return False

        # Set token header.
        ensure_api_token(os.environ["GITHUB_API_TOKEN"])

        # Ensure GitHub parameters are set.
        if not owner or not repo or not version:
            return False

        # Attempt to create a new release.
        result = await self.create_release(
            owner,
            repo,
            {
                "tag_name": version,
                "generate_release_notes": True,
            },
        )

        self.log.info("Create-release result: '%s'.", result)

        if "message" in result and result["message"] == "Validation Failed":
            self.log.warning("Release at current version already exists.")
            return True

        success = False

        if "id" in result:
            release_id = result["id"]

            # Use 'Upload a release asset' API to upload all files in the
            # 'dist' directory to the new release.
            for item in cwd.joinpath(dist).iterdir():
                result = await self.upload_release_asset(
                    owner, repo, release_id, item
                )
                self.log.info("Uploaded '%s'.", result["browser_download_url"])

            success = True

        return success

    async def run(
        self,
        inbox: Inbox,
        outbox: Outbox,
        *args,
        **kwargs,
    ) -> bool:  # pragma: nocover
        """Generate ninja configuration files."""

        return await self.release(
            args[0],
            kwargs["owner"],
            kwargs["repo"],
            kwargs["version"],
            dist=kwargs.get("dist", "dist"),
        )
