#!/usr/bin/env node

/**
 * Syncs all workspace package dependency versions to match their current versions.
 * This ensures lockstep versioning across the monorepo.
 */

import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { join } from 'path';

const args = process.argv.slice(2);
const setIndex = args.indexOf('--set');
const bumpIndex = args.indexOf('--bump');
const explicitVersion = setIndex === -1 ? undefined : args[setIndex + 1];
const bumpType = bumpIndex === -1 ? undefined : args[bumpIndex + 1];
const validBumps = new Set(['patch', 'minor', 'major']);

function fail(message) {
	console.error(message);
	process.exit(1);
}

function parseVersion(version) {
	const match = version.match(/^(\d+)\.(\d+)\.(\d+)(?:-.+)?$/);
	if (!match) fail(`Invalid semver version: ${version}`);
	return {
		major: Number(match[1]),
		minor: Number(match[2]),
		patch: Number(match[3]),
	};
}

function bumpVersion(version, type) {
	const parsed = parseVersion(version);
	if (type === 'major') return `${parsed.major + 1}.0.0`;
	if (type === 'minor') return `${parsed.major}.${parsed.minor + 1}.0`;
	if (type === 'patch') return `${parsed.major}.${parsed.minor}.${parsed.patch + 1}`;
	fail(`Invalid bump type: ${type}`);
}

if (explicitVersion && bumpType) {
	fail('Use either --set <version> or --bump <patch|minor|major>, not both.');
}
if (setIndex !== -1 && !explicitVersion) {
	fail('Usage: node scripts/sync-versions.js --set <version>');
}
if (bumpIndex !== -1 && !validBumps.has(bumpType)) {
	fail('Usage: node scripts/sync-versions.js --bump <patch|minor|major>');
}
if (explicitVersion) {
	parseVersion(explicitVersion);
}

const packagesDir = join(process.cwd(), 'packages');
const packageDirs = readdirSync(packagesDir, { withFileTypes: true })
	.filter(dirent => dirent.isDirectory())
	.map(dirent => dirent.name);

// Read all package.json files and build version map
const packages = {};
const versionMap = {};

for (const dir of packageDirs) {
	const pkgPath = join(packagesDir, dir, 'package.json');
	try {
		const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));
		packages[dir] = { path: pkgPath, data: pkg };
	} catch (e) {
		console.error(`Failed to read ${pkgPath}:`, e.message);
	}
}

if (explicitVersion || bumpType) {
	const currentVersions = new Set(Object.values(packages).map(pkg => pkg.data.version));
	if (currentVersions.size > 1) {
		fail('Cannot bump versions because workspace packages are not currently in lockstep.');
	}
	const currentVersion = [...currentVersions][0];
	const nextVersion = explicitVersion ?? bumpVersion(currentVersion, bumpType);
	for (const pkg of Object.values(packages)) {
		pkg.data.version = nextVersion;
	}
}

for (const pkg of Object.values(packages)) {
	versionMap[pkg.data.name] = pkg.data.version;
}

console.log('Current versions:');
for (const [name, version] of Object.entries(versionMap).sort()) {
	console.log(`  ${name}: ${version}`);
}

// Verify all versions are the same (lockstep)
const versions = new Set(Object.values(versionMap));
if (versions.size > 1) {
	console.error('\n❌ ERROR: Not all packages have the same version!');
	console.error('Expected lockstep versioning. Run one of:');
	console.error('  npm run version:patch');
	console.error('  npm run version:minor');
	console.error('  npm run version:major');
	process.exit(1);
}

console.log('\n✅ All packages at same version (lockstep)');

// Update all inter-package dependencies
let totalUpdates = 0;
for (const [dir, pkg] of Object.entries(packages)) {
	let updated = explicitVersion || bumpType;

	// Check dependencies
	if (pkg.data.dependencies) {
		for (const [depName, currentVersion] of Object.entries(pkg.data.dependencies)) {
			if (versionMap[depName]) {
				const newVersion = `^${versionMap[depName]}`;
				if (currentVersion !== newVersion) {
					console.log(`\n${pkg.data.name}:`);
					console.log(`  ${depName}: ${currentVersion} → ${newVersion}`);
					pkg.data.dependencies[depName] = newVersion;
					updated = true;
					totalUpdates++;
				}
			}
		}
	}

	// Check devDependencies
	if (pkg.data.devDependencies) {
		for (const [depName, currentVersion] of Object.entries(pkg.data.devDependencies)) {
			if (versionMap[depName]) {
				const newVersion = `^${versionMap[depName]}`;
				if (currentVersion !== newVersion) {
					console.log(`\n${pkg.data.name}:`);
					console.log(`  ${depName}: ${currentVersion} → ${newVersion} (devDependencies)`);
					pkg.data.devDependencies[depName] = newVersion;
					updated = true;
					totalUpdates++;
				}
			}
		}
	}

	// Write if updated
	if (updated) {
		writeFileSync(pkg.path, JSON.stringify(pkg.data, null, '\t') + '\n');
	}
}

if (totalUpdates === 0) {
	console.log('\nAll inter-package dependencies already in sync.');
} else {
	console.log(`\n✅ Updated ${totalUpdates} dependency version(s)`);
}
