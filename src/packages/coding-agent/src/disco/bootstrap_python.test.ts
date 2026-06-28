import { spawn } from "node:child_process";
import { chmod, mkdir, mkdtemp, readFile, rm, stat, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import zlib from "node:zlib";
import { describe, expect, it } from "vitest";

const scriptPath = path.join(
	process.cwd(),
	"src/disco/skills/prepare-repo-skill-env/scripts/bootstrap_python.mjs",
);

type ExtractTarGz = (archive: string, destination: string) => void;

async function loadExtractTarGz(): Promise<ExtractTarGz> {
	const mod = await import(pathToFileURL(scriptPath).href) as { extractTarGz: ExtractTarGz };
	return mod.extractTarGz;
}

async function makeFakePython(options: { hasVenv?: boolean } = {}): Promise<{ tempRoot: string; executable: string }> {
	const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-fake-python-"));
	const executable = path.join(tempRoot, process.platform === "win32" ? "python.cmd" : "python");
	if (process.platform === "win32") {
		await writeFile(
			executable,
			[
				"@echo off",
				`"${process.execPath}" "${path.join(tempRoot, "fake-python.cjs")}" %*`,
			].join("\r\n"),
			"utf-8",
		);
	} else {
		await writeFile(
			executable,
			["#!/bin/sh", `exec "${process.execPath}" "${path.join(tempRoot, "fake-python.cjs")}" "$@"`].join("\n"),
			"utf-8",
		);
		await chmod(executable, 0o755);
	}
	await writeFile(
		path.join(tempRoot, "fake-python.cjs"),
		[
			"const args = process.argv.slice(2);",
			"if (args[0] === '-c' && args[1].includes('sys.version_info')) { console.log('3.11.9'); process.exit(0); }",
			`if (args[0] === '-c' && args[1] === 'import venv, ensurepip') { process.exit(${options.hasVenv === false ? 1 : 0}); }`,
			"if (args[0] === '-c' && args[1].includes(\"print('ok')\")) { console.log('ok'); process.exit(0); }",
			"console.error('unexpected fake python args: ' + JSON.stringify(args));",
			"process.exit(1);",
		].join("\n"),
		"utf-8",
	);
	return { tempRoot, executable };
}

function runBootstrap(
	args: string[] = [],
	env: Record<string, string> = {},
): Promise<{ stdout: string; stderr: string; code: number }> {
	return new Promise((resolve, reject) => {
		const child = spawn(process.execPath, [scriptPath, ...args], {
			env: { ...process.env, ...env },
			stdio: ["ignore", "pipe", "pipe"],
		});
		let stdout = "";
		let stderr = "";
		child.stdout.on("data", (chunk) => {
			stdout += String(chunk);
		});
		child.stderr.on("data", (chunk) => {
			stderr += String(chunk);
		});
		child.on("error", reject);
		child.on("close", (code) => resolve({ stdout, stderr, code: code ?? -1 }));
	});
}

function tarOctal(value: number, length: number): Buffer {
	const text = value.toString(8).padStart(length - 1, "0").slice(-(length - 1)) + "\0";
	return Buffer.from(text, "ascii");
}

function tarString(value: string, length: number): Buffer {
	const buffer = Buffer.alloc(length);
	buffer.write(value, 0, Math.min(Buffer.byteLength(value), length), "utf8");
	return buffer;
}

function tarEntry(name: string, body: Buffer, type = "0", mode = 0o644): Buffer {
	const header = Buffer.alloc(512);
	tarString(name, 100).copy(header, 0);
	tarOctal(mode, 8).copy(header, 100);
	tarOctal(0, 8).copy(header, 108);
	tarOctal(0, 8).copy(header, 116);
	tarOctal(body.length, 12).copy(header, 124);
	tarOctal(0, 12).copy(header, 136);
	Buffer.from("        ", "ascii").copy(header, 148);
	tarString(type, 1).copy(header, 156);
	tarString("ustar", 6).copy(header, 257);
	tarString("00", 2).copy(header, 263);
	let checksum = 0;
	for (const value of header) checksum += value;
	tarOctal(checksum, 8).copy(header, 148);
	const padding = Buffer.alloc((512 - (body.length % 512)) % 512);
	return Buffer.concat([header, body, padding]);
}

function makeTarGz(entries: Array<{ name: string; body?: string; type?: string; mode?: number }>): Buffer {
	const blocks = entries.map((entry) =>
		tarEntry(entry.name, Buffer.from(entry.body ?? "", "utf8"), entry.type ?? "0", entry.mode ?? 0o644),
	);
	return zlib.gzipSync(Buffer.concat([...blocks, Buffer.alloc(1024)]));
}

function paxRecord(key: string, value: string): string {
	const payload = `${key}=${value}\n`;
	let length = Buffer.byteLength(payload) + 3;
	for (;;) {
		const candidate = `${length} ${payload}`;
		const actual = Buffer.byteLength(candidate);
		if (actual === length) return candidate;
		length = actual;
	}
}

describe("bootstrap_python.mjs", () => {
	it("uses DISCO_PYTHON when it satisfies the requested version", async () => {
		const { tempRoot, executable } = await makeFakePython();
		try {
			const result = await runBootstrap(["--min-version", "3.10", "--print"], { DISCO_PYTHON: executable });
			expect(result.code, result.stderr).toBe(0);
			expect(result.stdout.trim()).toBe(executable);
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("rejects DISCO_PYTHON when it does not match the required family", async () => {
		const { tempRoot, executable } = await makeFakePython();
		try {
			const result = await runBootstrap(
				["--min-version", "3.10", "--require-family", "3.12", "--no-download", "--print"],
				{ DISCO_PYTHON: executable },
			);
			expect(result.code).toBe(2);
			expect(result.stderr).toContain("no Python >= 3.10 in family 3.12 found");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("rejects DISCO_PYTHON without venv support when required", async () => {
		const { tempRoot, executable } = await makeFakePython({ hasVenv: false });
		try {
			const result = await runBootstrap(
				["--min-version", "3.10", "--require-venv", "--no-download", "--print"],
				{ DISCO_PYTHON: executable, PATH: tempRoot, Path: tempRoot },
			);
			expect(result.code).toBe(2);
			expect(result.stderr).toContain("with venv/ensurepip support");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("runs a command with the resolved executable substituted", async () => {
		const { tempRoot, executable } = await makeFakePython();
		try {
			const result = await runBootstrap(
				[
					"--min-version",
					"3.10",
					"--",
					"{python}",
					"-c",
					"print('ok')",
				],
				{ DISCO_PYTHON: executable },
			);
			expect(result.code, result.stderr).toBe(0);
			expect(result.stdout.trim()).toBe("ok");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("rejects invalid download timeout values before attempting discovery", async () => {
		const result = await runBootstrap(["--download-timeout", "0", "--no-download", "--print"], {
			DISCO_PYTHON: "",
		});
		expect(result.code).toBe(2);
		expect(result.stderr).toContain("--download-timeout must be a positive number");
	});

	it("rejects using a local archive and asset URL together", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-bootstrap-args-"));
		try {
			const archive = path.join(tempRoot, "python.tar.gz");
			await writeFile(archive, makeTarGz([{ name: "python/readme.txt", body: "ok\n" }]));
			const result = await runBootstrap([
				"--archive",
				archive,
				"--asset-url",
				"https://example.com/python.tar.gz",
				"--no-download",
				"--print",
			]);
			expect(result.code).toBe(2);
			expect(result.stderr).toContain("use only one of --archive or --asset-url");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("can bootstrap from a local python-build-standalone archive", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-bootstrap-local-"));
		try {
			const fake = await makeFakePython();
			const archiveRoot = path.join(tempRoot, "archive");
			await mkdir(path.join(archiveRoot, "python", "bin"), { recursive: true });
			const archive = path.join(tempRoot, "python.tar.gz");
			const pythonEntry = process.platform === "win32" ? "python/python.exe" : "python/bin/python3";
			await writeFile(
				archive,
				makeTarGz([
					{ name: "python/bin/", type: "5", mode: 0o755 },
					{ name: pythonEntry, body: await readFile(fake.executable, "utf-8"), mode: 0o755 },
				]),
			);
			await writeFile(path.join(archiveRoot, "unused"), "unused", "utf-8");

			const result = await runBootstrap(
				[
					"--agent-dir",
					path.join(tempRoot, "agent"),
					"--archive",
					archive,
					"--min-version",
					"3.10",
					"--require-family",
					"3.11",
					"--require-venv",
					"--",
					"{python}",
					"-c",
					"print('ok')",
				],
				{ PATH: tempRoot, Path: tempRoot },
			);

			expect(result.code, result.stderr).toBe(0);
			expect(result.stdout.trim()).toBe("ok");
			expect(result.stderr).toContain("using local Python archive");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("extracts tar.gz archives without relying on a system tar command", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-bootstrap-tar-"));
		try {
			const extractTarGz = await loadExtractTarGz();
			const archive = path.join(tempRoot, "fixture.tar.gz");
			const output = path.join(tempRoot, "out");
			await writeFile(
				archive,
				makeTarGz([
					{ name: "python/bin/", type: "5", mode: 0o755 },
					{ name: "python/bin/python3", body: "#!/bin/sh\n", mode: 0o755 },
					{ name: "python/lib/readme.txt", body: "ok\n", mode: 0o644 },
				]),
			);

			extractTarGz(archive, output);

			expect(await readFile(path.join(output, "python", "lib", "readme.txt"), "utf-8")).toBe("ok\n");
			if (process.platform !== "win32") {
				expect((await stat(path.join(output, "python", "bin", "python3"))).mode & 0o111).not.toBe(0);
			}
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("rejects unsafe tar paths", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-bootstrap-tar-"));
		try {
			const extractTarGz = await loadExtractTarGz();
			const archive = path.join(tempRoot, "bad.tar.gz");
			await writeFile(archive, makeTarGz([{ name: "../escape.txt", body: "bad" }]));
			expect(() => extractTarGz(archive, path.join(tempRoot, "out"))).toThrow(/unsafe tar entry path/);
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("does not apply global pax path records to every subsequent tar entry", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-bootstrap-tar-"));
		try {
			const extractTarGz = await loadExtractTarGz();
			const archive = path.join(tempRoot, "global-pax.tar.gz");
			const output = path.join(tempRoot, "out");
			await writeFile(
				archive,
				makeTarGz([
					{ name: "global-pax", type: "g", body: paxRecord("path", "wrong.txt") },
					{ name: "first.txt", body: "first\n" },
					{ name: "second.txt", body: "second\n" },
				]),
			);

			extractTarGz(archive, output);

			expect(await readFile(path.join(output, "first.txt"), "utf-8")).toBe("first\n");
			expect(await readFile(path.join(output, "second.txt"), "utf-8")).toBe("second\n");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});
});
