#!/usr/bin/env python3
"""Read-only OpenHands backend import diagnostic.

This helper checks selected backend modules without starting the server, creating
sandboxes, contacting external services, or generating schema/OpenAPI artifacts.
It is intended to separate missing dependency/setup problems from application
code regressions.
"""

from __future__ import annotations

import argparse
import importlib
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModuleCheck:
    name: str
    why: str


MODULES: tuple[ModuleCheck, ...] = (
    ModuleCheck('openhands', 'top-level package'),
    ModuleCheck('openhands.app_server', 'app-server package'),
    ModuleCheck('openhands.server', 'server compatibility package'),
    ModuleCheck('openhands.app_server.config', 'configuration and dependency injectors'),
    ModuleCheck('openhands.app_server.v1_router', 'V1 API router aggregation'),
    ModuleCheck('openhands.app_server.settings.settings_models', 'settings Pydantic models'),
    ModuleCheck('openhands.app_server.settings.settings_router', 'settings API route module'),
    ModuleCheck('openhands.app_server.secrets.secrets_models', 'secrets Pydantic models'),
    ModuleCheck('openhands.app_server.secrets.secrets_router', 'secrets API route module'),
    ModuleCheck('openhands.app_server.sandbox.sandbox_models', 'sandbox Pydantic models'),
    ModuleCheck('openhands.app_server.sandbox.session_auth', 'sandbox session authentication helpers'),
    ModuleCheck('openhands.app_server.app_conversation.app_conversation_models', 'conversation Pydantic models'),
    ModuleCheck('openhands.app_server.config_api.config_models', 'config API response models'),
    ModuleCheck('openhands.app_server.web_client.web_client_models', 'web-client config models'),
)


def _module_hint(error: BaseException) -> str:
    if isinstance(error, ModuleNotFoundError):
        missing = error.name or '<unknown>'
        if missing == 'openhands':
            return (
                'OpenHands package was not importable. Run from the repository root '
                'with --repo-root, or install the package into the active Python environment.'
            )
        if missing.startswith('openhands.'):
            return (
                f"OpenHands namespace module '{missing}' was not importable. "
                'Install backend dependencies such as the OpenHands SDK/agent-server packages, '
                'then rerun this diagnostic.'
            )
        return (
            f"Missing dependency '{missing}'. Install backend dependencies for the active "
            'Python environment, then rerun this diagnostic.'
        )
    if isinstance(error, ImportError):
        return 'A dependency or symbol import failed. Check the traceback for the missing package or changed API.'
    return 'The module raised during import. Inspect the traceback before assuming server startup is broken.'


def _add_repo_root(repo_root: Path) -> None:
    root = repo_root.resolve()
    if not root.exists():
        raise SystemExit(f'--repo-root does not exist: {repo_root}')
    if not (root / 'pyproject.toml').exists():
        raise SystemExit(f'--repo-root is not an OpenHands checkout root: {repo_root}')
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)


def _check_config_schema(show_tracebacks: bool) -> BaseException | None:
    try:
        from openhands.app_server.config import AppServerConfig

        schema = AppServerConfig.model_json_schema()
        if not isinstance(schema, dict) or 'properties' not in schema:
            raise RuntimeError('AppServerConfig.model_json_schema() returned an unexpected shape')
    except BaseException as exc:  # noqa: BLE001 - diagnostics should report all schema failures
        print('FAIL AppServerConfig.model_json_schema — config schema sanity check')
        print(f'     {exc.__class__.__name__}: {exc}')
        print(f'     Hint: {_module_hint(exc)}')
        if show_tracebacks:
            traceback.print_exception(exc)
        return exc

    print('OK   AppServerConfig.model_json_schema — config schema sanity check')
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Check selected OpenHands backend imports without server startup.'
    )
    parser.add_argument(
        '--repo-root',
        default='.',
        help='OpenHands repository root or installed-package source root. Defaults to current directory.',
    )
    parser.add_argument(
        '--show-tracebacks',
        action='store_true',
        help='Print full tracebacks for failed imports.',
    )
    args = parser.parse_args()

    _add_repo_root(Path(args.repo_root))

    failures: list[tuple[ModuleCheck, BaseException]] = []
    print('OpenHands backend import diagnostic')
    print(f'Python: {sys.version.split()[0]}')
    print('Mode: read-only imports; no server startup')
    print()

    for check in MODULES:
        try:
            importlib.import_module(check.name)
        except BaseException as exc:  # noqa: BLE001 - diagnostics should report all import failures
            failures.append((check, exc))
            print(f'FAIL {check.name} — {check.why}')
            print(f'     {exc.__class__.__name__}: {exc}')
            print(f'     Hint: {_module_hint(exc)}')
            if args.show_tracebacks:
                traceback.print_exception(exc)
        else:
            print(f'OK   {check.name} — {check.why}')

    schema_failure = _check_config_schema(args.show_tracebacks)

    print()
    if failures or schema_failure:
        total = len(failures) + (1 if schema_failure else 0)
        print(f'{total} backend check(s) failed.')
        print('Resolve the first missing dependency or import error, then rerun this script.')
        return 1

    print('All selected backend imports and config schema checks succeeded.')
    print('Next step: run focused backend tests for the area you changed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
