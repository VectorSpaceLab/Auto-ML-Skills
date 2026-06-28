import { spawn } from "node:child_process";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { describe, expect, it } from "vitest";

const scriptPath = path.join(
	process.cwd(),
	"src/disco/skills/prepare-repo-skill-env/scripts/setup_repo_conda_env.py",
);

function runSetup(args: string[]): Promise<{ stdout: string; stderr: string; code: number }> {
	return new Promise((resolve, reject) => {
		const child = spawn("python3", [scriptPath, ...args], {
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

describe("setup_repo_conda_env.py venv fallback", () => {
	it("creates and verifies a venv environment without conda", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-venv-env-"));
		try {
			const repo = path.join(tempRoot, "repo");
			await mkdir(path.join(repo, "sample_pkg"), { recursive: true });
			await writeFile(
				path.join(repo, "pyproject.toml"),
				[
					"[build-system]",
					'requires = ["setuptools>=61"]',
					'build-backend = "setuptools.build_meta"',
					"",
					"[project]",
					'name = "sample-pkg"',
					'version = "0.1.0"',
				].join("\n"),
				"utf-8",
			);
			await writeFile(path.join(repo, "sample_pkg", "__init__.py"), '__version__ = "0.1.0"\n', "utf-8");

			const prefix = path.join(tempRoot, "inspection-env");
			const report = path.join(tempRoot, "repo_env_report.json");
			const result = await runSetup([
				"--repo",
				repo,
				"--conda-prefix",
				prefix,
				"--env-manager",
				"venv",
				"--package",
				"sample-pkg",
				"--import",
				"sample_pkg",
				"--report",
				report,
				"--timeout",
				"300",
			]);

			expect(result.code, result.stderr).toBe(0);
			const parsed = JSON.parse(await readFile(report, "utf-8"));
			expect(parsed.status).toBe("ok");
			expect(parsed.inputs.environment_manager).toBe("venv");
			expect(parsed.handoff.environment_manager).toBe("venv");
			expect(parsed.handoff.ready_for_create_skill_for_a_repo).toBe(true);
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	}, 120_000);
});
