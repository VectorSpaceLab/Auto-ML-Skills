#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$ROOT_DIR/src"
CLI_PACKAGE_DIR="$SRC_DIR/packages/coding-agent"

if [[ ! -f "$SRC_DIR/package.json" ]]; then
	echo "error: expected source workspace at $SRC_DIR" >&2
	echo "run this script from a checkout that contains src/package.json" >&2
	exit 1
fi

if [[ ! -f "$CLI_PACKAGE_DIR/package.json" ]]; then
	echo "error: expected CLI package at $CLI_PACKAGE_DIR" >&2
	exit 1
fi

cd "$SRC_DIR"

echo "==> Removing local install and build artifacts"
rm -rf node_modules packages/*/node_modules packages/*/dist

echo "==> Installing workspace dependencies"
npm install --ignore-scripts

echo "==> Building TypeScript packages"
npm run build

echo "==> Linking disco CLI"
cd "$CLI_PACKAGE_DIR"
npm link

echo "==> Done"
echo "disco is linked globally. Try: disco --help"
