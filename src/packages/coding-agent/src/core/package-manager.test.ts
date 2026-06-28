import { describe, expect, it } from "vitest";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DefaultPackageManager } from "./package-manager.ts";
import { SettingsManager } from "./settings-manager.ts";

describe("DefaultPackageManager package manifest compatibility", () => {
	it("loads package resources declared with legacy pi manifest fields", async () => {
		const tempRoot = mkdtempSync(join(tmpdir(), "disco-package-manifest-"));
		try {
			const agentDir = join(tempRoot, "agent");
			const packageDir = join(tempRoot, "legacy-pi-package");
			const skillsDir = join(packageDir, "skills", "legacy-skill");
			const promptsDir = join(packageDir, "prompts");
			mkdirSync(skillsDir, { recursive: true });
			mkdirSync(promptsDir, { recursive: true });
			writeFileSync(
				join(packageDir, "package.json"),
				JSON.stringify(
					{
						name: "legacy-pi-package",
						version: "1.0.0",
						type: "module",
						pi: {
							extensions: ["./index.ts"],
							skills: ["./skills"],
							prompts: ["./prompts"],
						},
					},
					null,
					2,
				),
			);
			writeFileSync(join(packageDir, "index.ts"), "export default function extension() {}\n");
			writeFileSync(
				join(skillsDir, "SKILL.md"),
				"---\nname: legacy-skill\ndescription: Legacy package skill.\n---\n",
			);
			writeFileSync(join(promptsDir, "legacy-prompt.md"), "# Legacy Prompt\n");

			const manager = new DefaultPackageManager({
				cwd: tempRoot,
				agentDir,
				settingsManager: SettingsManager.inMemory({ packages: [packageDir] }),
			});

			const resolved = await manager.resolve(async () => "skip");

			expect(resolved.extensions.map((entry) => entry.path)).toContain(join(packageDir, "index.ts"));
			expect(resolved.skills.map((entry) => entry.path)).toContain(join(skillsDir, "SKILL.md"));
			expect(resolved.prompts.map((entry) => entry.path)).toContain(join(promptsDir, "legacy-prompt.md"));
		} finally {
			rmSync(tempRoot, { recursive: true, force: true });
		}
	});

	it("prefers disco manifest fields over legacy pi fields when both are present", async () => {
		const tempRoot = mkdtempSync(join(tmpdir(), "disco-package-manifest-"));
		try {
			const agentDir = join(tempRoot, "agent");
			const packageDir = join(tempRoot, "dual-manifest-package");
			mkdirSync(packageDir, { recursive: true });
			writeFileSync(
				join(packageDir, "package.json"),
				JSON.stringify(
					{
						name: "dual-manifest-package",
						version: "1.0.0",
						type: "module",
						disco: {
							extensions: ["./disco.ts"],
						},
						pi: {
							extensions: ["./pi.ts"],
						},
					},
					null,
					2,
				),
			);
			writeFileSync(join(packageDir, "disco.ts"), "export default function discoExtension() {}\n");
			writeFileSync(join(packageDir, "pi.ts"), "export default function piExtension() {}\n");

			const manager = new DefaultPackageManager({
				cwd: tempRoot,
				agentDir,
				settingsManager: SettingsManager.inMemory({ packages: [packageDir] }),
			});

			const resolved = await manager.resolve(async () => "skip");
			const extensionPaths = resolved.extensions.map((entry) => entry.path);

			expect(extensionPaths).toContain(join(packageDir, "disco.ts"));
			expect(extensionPaths).not.toContain(join(packageDir, "pi.ts"));
		} finally {
			rmSync(tempRoot, { recursive: true, force: true });
		}
	});
});
