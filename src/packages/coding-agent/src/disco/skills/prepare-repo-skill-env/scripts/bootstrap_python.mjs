#!/usr/bin/env node
/**
 * Resolve or install a host Python used to run DisCo's Python inspection
 * helper scripts.
 *
 * This is not the target repository inspection environment. It only ensures
 * DisCo can run its standard-library helper when an npm-installed machine
 * has no usable Python on PATH.
 */

import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import https from "node:https";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import zlib from "node:zlib";

const DEFAULT_MIN_VERSION = "3.10";
const DEFAULT_PYTHON_FAMILY = "3.11";
const DEFAULT_DOWNLOAD_TIMEOUT_SECONDS = 300;
const RELEASE_API = "https://api.github.com/repos/astral-sh/python-build-standalone/releases/latest";
const RELEASES_DOWNLOAD_PREFIX = "https://github.com/astral-sh/python-build-standalone/releases/download";
const SCRIPT_PATH = fileURLToPath(import.meta.url);

function defaultAgentDir() {
	return process.env.DISCO_CODING_AGENT_DIR || path.join(os.homedir(), ".disco", "agent");
}

function expandHome(value) {
	return value.replace(/^~(?=$|[\\/])/, os.homedir());
}

function parseArgs(argv) {
	const args = {
		agentDir: defaultAgentDir(),
		installDir: undefined,
		minVersion: DEFAULT_MIN_VERSION,
		pythonFamily: DEFAULT_PYTHON_FAMILY,
		requireFamily: undefined,
		requireVenv: false,
		archive: undefined,
		assetUrl: undefined,
		assetDigest: undefined,
		downloadTimeout: DEFAULT_DOWNLOAD_TIMEOUT_SECONDS,
		print: false,
		noDownload: false,
		command: [],
	};
	for (let index = 0; index < argv.length; index += 1) {
		const item = argv[index];
		if (item === "--") {
			args.command = argv.slice(index + 1);
			return args;
		}
		if (item === "--agent-dir") {
			args.agentDir = argv[++index];
		} else if (item === "--install-dir") {
			args.installDir = argv[++index];
		} else if (item === "--min-version") {
			args.minVersion = argv[++index];
		} else if (item === "--python-family") {
			args.pythonFamily = argv[++index];
		} else if (item === "--require-family") {
			args.requireFamily = argv[++index];
		} else if (item === "--require-venv") {
			args.requireVenv = true;
		} else if (item === "--archive") {
			args.archive = argv[++index];
		} else if (item === "--asset-url") {
			args.assetUrl = argv[++index];
		} else if (item === "--asset-digest") {
			args.assetDigest = argv[++index];
		} else if (item === "--download-timeout") {
			args.downloadTimeout = Number(argv[++index]);
		} else if (item === "--print") {
			args.print = true;
		} else if (item === "--no-download") {
			args.noDownload = true;
		} else if (item === "-h" || item === "--help") {
			printHelp();
			process.exit(0);
		} else {
			args.command = argv.slice(index);
			return args;
		}
	}
	return args;
}

function printHelp() {
	console.log(`Usage: node bootstrap_python.mjs [options] [-- COMMAND [ARGS...]]

Options:
  --agent-dir DIR          DisCo agent directory
  --install-dir DIR        Directory for the managed host Python
  --min-version VERSION    Minimum acceptable Python version, default ${DEFAULT_MIN_VERSION}
  --python-family VERSION  Standalone Python family to install, default ${DEFAULT_PYTHON_FAMILY}
  --require-family VERSION Require an existing/downloaded Python major.minor family
  --require-venv           Require venv and ensurepip support in the host Python
  --archive FILE           Use a local python-build-standalone .tar.gz archive
  --asset-url URL          Download the standalone Python archive from this URL
  --asset-digest DIGEST    Expected archive digest, format sha256:<hex>
  --download-timeout SEC   Timeout for release metadata and archive downloads, default ${DEFAULT_DOWNLOAD_TIMEOUT_SECONDS}
  --print                  Print the resolved Python executable path
  --no-download            Fail instead of downloading when no Python is found

When COMMAND is provided, occurrences of {python} are replaced with the resolved
Python executable path. If {python} is absent, the executable is prepended.`);
}

function compareVersions(left, right) {
	const a = left.split(".").map((part) => Number(part) || 0);
	const b = right.split(".").map((part) => Number(part) || 0);
	for (let index = 0; index < Math.max(a.length, b.length); index += 1) {
		const diff = (a[index] || 0) - (b[index] || 0);
		if (diff !== 0) {
			return diff;
		}
	}
	return 0;
}

function pythonVersion(command, args = []) {
	const result = spawnSync(command, [...args, "-c", "import sys; print('.'.join(map(str, sys.version_info[:3])))"], {
		encoding: "utf8",
		stdio: ["ignore", "pipe", "ignore"],
	});
	if (result.status !== 0) {
		return undefined;
	}
	return result.stdout.trim();
}

function pythonHasVenv(command, args = []) {
	const result = spawnSync(command, [...args, "-c", "import venv, ensurepip"], {
		encoding: "utf8",
		stdio: ["ignore", "ignore", "ignore"],
	});
	return result.status === 0;
}

function matchesRequiredFamily(version, requiredFamily) {
	return !requiredFamily || version === requiredFamily || version.startsWith(`${requiredFamily}.`);
}

function isUsablePython(command, args, minVersion, requiredFamily, requireVenv) {
	const version = pythonVersion(command, args);
	if (!version || compareVersions(version, minVersion) < 0 || !matchesRequiredFamily(version, requiredFamily)) {
		return undefined;
	}
	if (requireVenv && !pythonHasVenv(command, args)) {
		return undefined;
	}
	return version;
}

function findUsablePython(minVersion, requiredFamily, requireVenv) {
	if (process.env.DISCO_PYTHON) {
		const version = isUsablePython(process.env.DISCO_PYTHON, [], minVersion, requiredFamily, requireVenv);
		if (version) {
			return { command: process.env.DISCO_PYTHON, args: [], version, source: "DISCO_PYTHON" };
		}
		return undefined;
	}

	const candidates = process.platform === "win32"
		? [
			{ command: "py", args: ["-3.13"] },
			{ command: "py", args: ["-3.12"] },
			{ command: "py", args: ["-3.11"] },
			{ command: "py", args: ["-3"] },
			{ command: "python", args: [] },
		]
		: [
			{ command: "python3.13", args: [] },
			{ command: "python3.12", args: [] },
			{ command: "python3.11", args: [] },
			{ command: "python3", args: [] },
			{ command: "python", args: [] },
		];

	for (const candidate of candidates) {
		const version = isUsablePython(candidate.command, candidate.args, minVersion, requiredFamily, requireVenv);
		if (version) {
			return { ...candidate, version, source: "PATH" };
		}
	}
	return undefined;
}

function platformTarget() {
	const arch = os.arch();
	if (process.platform === "linux") {
		if (arch === "x64") return "x86_64-unknown-linux-gnu";
		if (arch === "arm64") return "aarch64-unknown-linux-gnu";
	}
	if (process.platform === "darwin") {
		if (arch === "x64") return "x86_64-apple-darwin";
		if (arch === "arm64") return "aarch64-apple-darwin";
	}
	if (process.platform === "win32") {
		if (arch === "x64") return "x86_64-pc-windows-msvc";
		if (arch === "arm64") return "aarch64-pc-windows-msvc";
	}
	throw new Error(`automatic Python download is not supported for ${process.platform}/${arch}`);
}

function requestJson(url, timeoutSeconds = DEFAULT_DOWNLOAD_TIMEOUT_SECONDS) {
	return new Promise((resolve, reject) => {
		const request = https.get(
			url,
			{
				headers: {
					"Accept": "application/vnd.github+json",
					"User-Agent": "disco-python-bootstrap",
				},
			},
			(response) => {
				if (response.statusCode && response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
					response.resume();
					requestJson(response.headers.location, timeoutSeconds).then(resolve, reject);
					return;
				}
				let body = "";
				response.setEncoding("utf8");
				response.on("data", (chunk) => {
					body += chunk;
				});
				response.on("end", () => {
					if (!response.statusCode || response.statusCode < 200 || response.statusCode >= 300) {
						reject(new Error(`HTTP ${response.statusCode} from ${url}: ${body.slice(0, 300)}`));
						return;
					}
					try {
						resolve(JSON.parse(body));
					} catch (error) {
						reject(error);
					}
				});
			},
		);
		request.setTimeout(timeoutSeconds * 1000, () => {
			request.destroy(new Error(`timed out after ${timeoutSeconds}s while requesting ${url}`));
		});
		request.on("error", reject);
	});
}

function downloadFile(url, destination, timeoutSeconds = DEFAULT_DOWNLOAD_TIMEOUT_SECONDS) {
	return new Promise((resolve, reject) => {
		fs.mkdirSync(path.dirname(destination), { recursive: true });
		const file = fs.createWriteStream(destination);
		const request = https.get(url, { headers: { "User-Agent": "disco-python-bootstrap" } }, (response) => {
			if (response.statusCode && response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
				file.close();
				fs.rmSync(destination, { force: true });
				downloadFile(response.headers.location, destination, timeoutSeconds).then(resolve, reject);
				return;
			}
			if (!response.statusCode || response.statusCode < 200 || response.statusCode >= 300) {
				file.close();
				fs.rmSync(destination, { force: true });
				reject(new Error(`HTTP ${response.statusCode} while downloading ${url}`));
				return;
			}
			response.pipe(file);
			file.on("finish", () => {
				file.close(resolve);
			});
		});
		request.setTimeout(timeoutSeconds * 1000, () => {
			request.destroy(new Error(`timed out after ${timeoutSeconds}s while downloading ${url}`));
		});
		request.on("error", (error) => {
			file.close();
			fs.rmSync(destination, { force: true });
			reject(error);
		});
	});
}

function sha256(filePath) {
	const hash = createHash("sha256");
	const data = fs.readFileSync(filePath);
	hash.update(data);
	return hash.digest("hex");
}

function pickAsset(release, pythonFamily, target) {
	const tag = release.tag_name;
	const assets = Array.isArray(release.assets) ? release.assets : [];
	const escapedFamily = pythonFamily.replace(".", "\\.");
	const patterns = [
		new RegExp(`^cpython-${escapedFamily}\\.\\d+\\+${tag}-${target}-install_only_stripped\\.tar\\.gz$`),
		new RegExp(`^cpython-${escapedFamily}\\.\\d+\\+${tag}-${target}-install_only\\.tar\\.gz$`),
	];
	for (const pattern of patterns) {
		const asset = assets.find((item) => typeof item.name === "string" && pattern.test(item.name));
		if (asset) {
			return asset;
		}
	}
	throw new Error(`no python-build-standalone ${pythonFamily} install_only asset found for ${target} in release ${tag}`);
}

async function resolveReleaseAsset(pythonFamily, timeoutSeconds) {
	const target = platformTarget();
	const release = await requestJson(RELEASE_API, timeoutSeconds);
	const asset = pickAsset(release, pythonFamily, target);
	return {
		tag: release.tag_name,
		target,
		name: asset.name,
		url: asset.browser_download_url || `${RELEASES_DOWNLOAD_PREFIX}/${release.tag_name}/${asset.name}`,
		digest: asset.digest,
	};
}

function assetNameFromUrl(url) {
	try {
		const parsed = new URL(url);
		const basename = path.posix.basename(parsed.pathname);
		return decodeURIComponent(basename || "python-standalone.tar.gz");
	} catch {
		return "python-standalone.tar.gz";
	}
}

function findPythonInManagedInstall(root) {
	const candidates = process.platform === "win32"
		? [
			path.join(root, "python", "python.exe"),
			path.join(root, "python.exe"),
		]
		: [
			path.join(root, "python", "bin", "python3"),
			path.join(root, "python", "bin", "python"),
			path.join(root, "bin", "python3"),
			path.join(root, "bin", "python"),
		];
	for (const candidate of candidates) {
		if (fs.existsSync(candidate)) {
			return candidate;
		}
	}
	return undefined;
}

function parseTarString(buffer, start, length) {
	const raw = buffer.subarray(start, start + length);
	const end = raw.indexOf(0);
	return raw.subarray(0, end >= 0 ? end : raw.length).toString("utf8");
}

function parseTarNumber(buffer, start, length) {
	const text = parseTarString(buffer, start, length).trim();
	return text ? Number.parseInt(text, 8) || 0 : 0;
}

function safeTarPath(entryPath) {
	const cleaned = entryPath.replace(/\\/g, "/").replace(/^\.?\/*/, "");
	const parts = cleaned.split("/").filter(Boolean);
	if (!parts.length || parts.some((part) => part === "." || part === "..")) {
		throw new Error(`unsafe tar entry path: ${entryPath}`);
	}
	return parts.join(path.sep);
}

function assertInside(destination, target) {
	const relative = path.relative(destination, target);
	if (relative === ".." || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
		throw new Error(`tar entry escapes destination: ${target}`);
	}
}

function parsePaxRecords(buffer) {
	const records = {};
	let offset = 0;
	while (offset < buffer.length) {
		const space = buffer.indexOf(0x20, offset);
		if (space < 0) break;
		const length = Number.parseInt(buffer.subarray(offset, space).toString("utf8"), 10);
		if (!Number.isFinite(length) || length <= 0) break;
		const record = buffer.subarray(space + 1, offset + length - 1).toString("utf8");
		const equals = record.indexOf("=");
		if (equals >= 0) {
			records[record.slice(0, equals)] = record.slice(equals + 1);
		}
		offset += length;
	}
	return records;
}

function writeFileEntry(target, data, mode) {
	fs.mkdirSync(path.dirname(target), { recursive: true });
	fs.writeFileSync(target, data);
	if (process.platform !== "win32" && mode) {
		fs.chmodSync(target, mode & 0o777);
	}
}

function createDeferredLink(destination, link) {
	const target = path.join(destination, safeTarPath(link.name));
	assertInside(destination, target);
	const linkTarget = link.linkName.replace(/\\/g, "/");
	if (path.isAbsolute(linkTarget) || linkTarget.split("/").some((part) => part === "..")) {
		return;
	}
	fs.mkdirSync(path.dirname(target), { recursive: true });
	const resolvedSource = path.resolve(path.dirname(target), linkTarget);
	assertInside(destination, resolvedSource);
	if (link.type === "2") {
		try {
			fs.symlinkSync(linkTarget, target);
		} catch {
			if (fs.existsSync(resolvedSource) && fs.statSync(resolvedSource).isFile()) {
				fs.copyFileSync(resolvedSource, target);
			}
		}
	} else if (link.type === "1" && fs.existsSync(resolvedSource)) {
		try {
			fs.linkSync(resolvedSource, target);
		} catch {
			if (fs.statSync(resolvedSource).isFile()) {
				fs.copyFileSync(resolvedSource, target);
			}
		}
	}
}

export function extractTarGz(archive, destination) {
	fs.rmSync(destination, { recursive: true, force: true });
	fs.mkdirSync(destination, { recursive: true });
	const destinationRoot = path.resolve(destination);
	const tar = zlib.gunzipSync(fs.readFileSync(archive));
	const deferredLinks = [];
	let offset = 0;
	let nextPax = {};
	let nextLongName;
	let nextLongLink;

	while (offset + 512 <= tar.length) {
		const header = tar.subarray(offset, offset + 512);
		offset += 512;
		if (header.every((value) => value === 0)) {
			break;
		}

		let name = parseTarString(header, 0, 100);
		const mode = parseTarNumber(header, 100, 8);
		const size = parseTarNumber(header, 124, 12);
		const type = parseTarString(header, 156, 1) || "0";
		let linkName = parseTarString(header, 157, 100);
		const prefix = parseTarString(header, 345, 155);
		if (prefix) {
			name = `${prefix}/${name}`;
		}
		const data = tar.subarray(offset, offset + size);
		offset += Math.ceil(size / 512) * 512;

		if (type === "x") {
			nextPax = parsePaxRecords(data);
			continue;
		}
		if (type === "g") {
			continue;
		}
		if (type === "L") {
			nextLongName = data.toString("utf8").replace(/\0.*$/s, "");
			continue;
		}
		if (type === "K") {
			nextLongLink = data.toString("utf8").replace(/\0.*$/s, "");
			continue;
		}

		name = nextPax.path || nextLongName || name;
		linkName = nextPax.linkpath || nextLongLink || linkName;
		nextPax = {};
		nextLongName = undefined;
		nextLongLink = undefined;

		const relative = safeTarPath(name);
		const target = path.join(destinationRoot, relative);
		assertInside(destinationRoot, target);
		if (type === "5") {
			fs.mkdirSync(target, { recursive: true });
			if (process.platform !== "win32" && mode) {
				fs.chmodSync(target, mode & 0o777);
			}
		} else if (type === "0" || type === "") {
			writeFileEntry(target, data, mode);
		} else if (type === "2" || type === "1") {
			deferredLinks.push({ type, name, linkName });
		}
	}

	for (const link of deferredLinks) {
		createDeferredLink(destinationRoot, link);
	}
}

async function installManagedPython(installDir, pythonFamily, minVersion, requiredFamily, requireVenv, options = {}) {
	const marker = path.join(installDir, ".disco-python-bootstrap.json");
	const existing = findPythonInManagedInstall(installDir);
	if (existing) {
		const version = pythonVersion(existing);
		if (
			version &&
			compareVersions(version, minVersion) >= 0 &&
			matchesRequiredFamily(version, requiredFamily) &&
			(!requireVenv || pythonHasVenv(existing))
		) {
			return { command: existing, args: [], version, source: "managed", installed: false };
		}
	}

	const downloadDir = path.join(installDir, "downloads");
	let asset;
	let archive;
	if (options.archive) {
		archive = path.resolve(expandHome(options.archive));
		if (!fs.existsSync(archive)) {
			throw new Error(`local Python archive does not exist: ${archive}`);
		}
		asset = {
			tag: "local",
			target: platformTarget(),
			name: path.basename(archive),
			url: `file://${archive}`,
			digest: options.assetDigest,
		};
		console.error(`DisCo: using local Python archive ${archive}`);
	} else {
		asset = options.assetUrl
			? {
				tag: "custom",
				target: platformTarget(),
				name: assetNameFromUrl(options.assetUrl),
				url: options.assetUrl,
				digest: options.assetDigest,
			}
			: await resolveReleaseAsset(pythonFamily, options.downloadTimeout || DEFAULT_DOWNLOAD_TIMEOUT_SECONDS);
		archive = path.join(downloadDir, asset.name);
		console.error(`DisCo: downloading Python ${pythonFamily} for ${asset.target} from ${asset.url}`);
		await downloadFile(asset.url, archive, options.downloadTimeout || DEFAULT_DOWNLOAD_TIMEOUT_SECONDS);
	}
	if (asset.digest && asset.digest.startsWith("sha256:")) {
		const expected = asset.digest.slice("sha256:".length);
		const actual = sha256(archive);
		if (actual !== expected) {
			if (!options.archive) {
				fs.rmSync(archive, { force: true });
			}
			throw new Error(`downloaded Python archive checksum mismatch: expected ${expected}, got ${actual}`);
		}
	}

	const extractDir = path.join(installDir, "runtime");
	extractTarGz(archive, extractDir);
	const python = findPythonInManagedInstall(extractDir);
	if (!python) {
		throw new Error(`downloaded Python archive did not contain an expected Python executable under ${extractDir}`);
	}
	const version = pythonVersion(python);
	if (!version || compareVersions(version, minVersion) < 0 || !matchesRequiredFamily(version, requiredFamily)) {
		throw new Error(`downloaded Python ${version || "(unknown)"} does not satisfy required version constraints`);
	}
	if (requireVenv && !pythonHasVenv(python)) {
		throw new Error("downloaded Python does not provide venv and ensurepip support");
	}
	fs.mkdirSync(installDir, { recursive: true });
	fs.writeFileSync(
		marker,
		`${JSON.stringify({ installed_at: new Date().toISOString(), asset, python, version }, null, 2)}\n`,
		"utf8",
	);
	return { command: python, args: [], version, source: "managed", installed: true };
}

function shellQuote(value) {
	if (process.platform === "win32") {
		return `"${value.replace(/"/g, '\\"')}"`;
	}
	return `'${value.replace(/'/g, "'\\''")}'`;
}

function runCommand(command, python) {
	let finalCommand;
	if (command.includes("{python}")) {
		finalCommand = command.flatMap((item) => (item === "{python}" ? [python.command, ...python.args] : [item]));
	} else {
		finalCommand = [python.command, ...python.args, ...command];
	}
	const result = spawnSync(finalCommand[0], finalCommand.slice(1), {
		env: {
			...process.env,
			DISCO_BOOTSTRAP_PYTHON: python.command,
		},
		stdio: "inherit",
	});
	if (result.error) {
		throw result.error;
	}
	return result.status ?? 1;
}

async function main(argv) {
	const args = parseArgs(argv);
	if (!Number.isFinite(args.downloadTimeout) || args.downloadTimeout <= 0) {
		console.error("bootstrap_python.mjs: --download-timeout must be a positive number");
		return 2;
	}
	if (args.archive && args.assetUrl) {
		console.error("bootstrap_python.mjs: use only one of --archive or --asset-url");
		return 2;
	}
	const agentDir = path.resolve(expandHome(args.agentDir));
	const installDir = path.resolve(expandHome(args.installDir || path.join(agentDir, "runtimes", "python-host")));

	const requiredFamily = args.requireFamily;
	let python = findUsablePython(args.minVersion, requiredFamily, args.requireVenv);
	if (!python) {
		if (args.noDownload) {
			const familyText = requiredFamily ? ` in family ${requiredFamily}` : "";
			const venvText = args.requireVenv ? " with venv/ensurepip support" : "";
			console.error(`bootstrap_python.mjs: no Python >= ${args.minVersion}${familyText}${venvText} found on PATH and --no-download was set`);
			return 2;
		}
		python = await installManagedPython(installDir, args.pythonFamily, args.minVersion, requiredFamily, args.requireVenv, {
			archive: args.archive,
			assetUrl: args.assetUrl,
			assetDigest: args.assetDigest,
			downloadTimeout: args.downloadTimeout,
		});
	}

	if (args.print) {
		console.log(python.command);
	}

	if (!args.command.length) {
		if (!args.print) {
			console.log(`${python.command} (${python.version}, ${python.source})`);
		}
		return 0;
	}

	console.error(`DisCo: using Python ${python.version} at ${shellQuote(python.command)} (${python.source})`);
	return runCommand(args.command, python);
}

if (process.argv[1] && path.resolve(process.argv[1]) === SCRIPT_PATH) {
	try {
		process.exitCode = await main(process.argv.slice(2));
	} catch (error) {
		console.error(error instanceof Error ? error.message : String(error));
		process.exitCode = 1;
	}
}
