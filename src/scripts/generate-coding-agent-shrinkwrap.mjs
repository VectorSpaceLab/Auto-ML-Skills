#!/usr/bin/env node

import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const workspaceRoot = join(scriptDir, '..');
const packageDir = join(workspaceRoot, 'packages', 'coding-agent');
const rootLockPath = join(workspaceRoot, 'package-lock.json');
const packageJsonPath = join(packageDir, 'package.json');
const outputPath = join(packageDir, 'npm-shrinkwrap.json');

const workspacePackages = new Map([
	['@auto-ml-skills/disco-tui', 'packages/tui'],
	['@auto-ml-skills/disco-ai', 'packages/ai'],
	['@auto-ml-skills/disco-agent-core', 'packages/agent'],
	['@auto-ml-skills/disco', 'packages/coding-agent'],
]);

function fail(message) {
	console.error(`error: ${message}`);
	process.exit(1);
}

function readJson(path) {
	try {
		return JSON.parse(readFileSync(path, 'utf8'));
	} catch (error) {
		fail(`failed to read ${path}: ${error.message}`);
	}
}

function packagePathForName(name) {
	return `node_modules/${name}`;
}

function lockEntry(lock, path) {
	const entry = lock.packages?.[path];
	if (!entry) {
		fail(`missing lockfile entry: ${path}`);
	}
	return entry;
}

function packageJsonEntry(pkg) {
	const entry = {
		name: pkg.name,
		version: pkg.version,
		license: pkg.license,
	};
	for (const key of [
		'dependencies',
		'optionalDependencies',
		'peerDependencies',
		'peerDependenciesMeta',
		'bin',
		'engines',
		'os',
		'cpu',
		'libc',
	]) {
		if (pkg[key] !== undefined) {
			entry[key] = pkg[key];
		}
	}
	return entry;
}

function publicLockEntry(entry) {
	const copy = { ...entry };
	delete copy.dev;
	delete copy.devOptional;
	delete copy.link;
	return copy;
}

function isNodeModulesPath(path) {
	return (
		path === 'node_modules' ||
		path.startsWith('node_modules/') ||
		path.endsWith('/node_modules') ||
		path.includes('/node_modules/')
	);
}

function candidateDependencyPaths(fromPath, dependencyName) {
	const candidates = [];
	const parts = fromPath ? fromPath.split('/') : [];

	for (let index = parts.length; index >= 0; index -= 1) {
		const prefixParts = parts.slice(0, index);
		const prefix = prefixParts.join('/');
		const base = prefix ? `${prefix}/node_modules/${dependencyName}` : `node_modules/${dependencyName}`;
		candidates.push(base);

		if (index > 0 && parts[index - 1] === 'node_modules') {
			index -= 1;
		}
	}

	candidates.push(`node_modules/${dependencyName}`);
	return [...new Set(candidates)].filter(isNodeModulesPath);
}

function resolveDependency(lock, fromPath, dependencyName) {
	const workspacePath = workspacePackages.get(dependencyName);
	if (workspacePath) {
		return {
			sourcePath: workspacePath,
			outputPath: packagePathForName(dependencyName),
			workspace: true,
		};
	}

	for (const candidate of candidateDependencyPaths(fromPath, dependencyName)) {
		if (lock.packages?.[candidate]) {
			return {
				sourcePath: candidate,
				outputPath: candidate,
				workspace: false,
			};
		}
	}

	fail(`could not resolve dependency ${dependencyName} from ${fromPath || '<root>'}`);
}

function dependencyNames(entry) {
	return [
		...Object.keys(entry.dependencies ?? {}),
		...Object.keys(entry.optionalDependencies ?? {}),
	];
}

function buildShrinkwrap() {
	const lock = readJson(rootLockPath);
	const packageJson = readJson(packageJsonPath);

	if (!lock.packages) {
		fail(`${rootLockPath} is missing packages metadata`);
	}
	if (lock.lockfileVersion !== 3) {
		fail(`expected package-lock lockfileVersion 3, found ${lock.lockfileVersion}`);
	}

	const packages = {
		'': packageJsonEntry(packageJson),
	};
	const queue = [];
	const seen = new Set(['']);

	for (const name of dependencyNames(packages[''])) {
		queue.push(resolveDependency(lock, 'packages/coding-agent', name));
	}

	while (queue.length > 0) {
		const item = queue.shift();
		if (seen.has(item.outputPath)) {
			continue;
		}
		seen.add(item.outputPath);

		const sourceEntry = lockEntry(lock, item.sourcePath);
		const outputEntry = item.workspace
			? packageJsonEntry(readJson(join(workspaceRoot, item.sourcePath, 'package.json')))
			: publicLockEntry(sourceEntry);
		packages[item.outputPath] = outputEntry;

		for (const name of dependencyNames(outputEntry)) {
			const resolved = resolveDependency(lock, item.sourcePath, name);
			if (!seen.has(resolved.outputPath)) {
				queue.push(resolved);
			}
		}
	}

	const shrinkwrap = {
		name: packageJson.name,
		version: packageJson.version,
		lockfileVersion: 3,
		requires: true,
		packages,
	};

	writeFileSync(outputPath, `${JSON.stringify(shrinkwrap, null, '\t')}\n`);
	console.log(
		`wrote ${relative(process.cwd(), outputPath)} with ${Object.keys(packages).length} package entries`,
	);
}

buildShrinkwrap();
