import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { describe, expect, it } from "vitest";

const scriptPath = path.join(
	process.cwd(),
	"src/disco/skills/verify-repo-skill/scripts/update_repo_skills_router.mjs",
);

type ScenarioMetadata = {
	id: string;
	title?: string;
	when_to_read?: string;
	role?: string;
	read_when?: string;
	best_for?: string;
	avoid_when?: string;
	useful_entry_points?: string[];
	selection_guidance?: string;
};

type ScenarioDefinition = {
	title?: string;
	when_to_read?: string;
	how_to_choose?: string;
	selection_guidance?: string;
	aliases?: string[];
	allow_new?: boolean;
	why_not_existing?: string;
	expected_future_reuse?: string;
};

function runUpdater(
	agentDir: string,
	extraArgs: string[] = [],
	extraEnv: Record<string, string> = {},
): Promise<{ stdout: string; stderr: string; code: number }> {
	return new Promise((resolve, reject) => {
		const templateArgs = extraArgs.includes("--template-dir")
			? []
			: ["--template-dir", path.join(agentDir, ".empty-router-template")];
		const child = spawn(process.execPath, [scriptPath, "--agent-dir", agentDir, ...templateArgs, ...extraArgs], {
			env: { ...process.env, ...extraEnv },
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

async function writeScenarioRegistryTemplate(
	tempRoot: string,
	scenarios: Record<string, ScenarioDefinition> = {
		"agent-workflows": {
			title: "Agent Workflows",
			when_to_read: "Agent framework, tool calling, and agent workflow tasks.",
			how_to_choose: "Choose by the named framework, runtime, protocol, or agent execution surface.",
			aliases: ["agent-apps"],
		},
	},
): Promise<string> {
	const templateDir = path.join(tempRoot, "router-template");
	await mkdir(path.join(templateDir, "references"), { recursive: true });
	await writeFile(
		path.join(templateDir, "references", "scenario-registry.json"),
		JSON.stringify(
			{
				version: 1,
				enforce_known_scenarios: true,
				scenarios,
			},
			null,
			2,
		),
		"utf-8",
	);
	return templateDir;
}

async function writeSkill(
	agentDir: string,
	skillId: string,
	scenarios: ScenarioMetadata[],
	scenarioDefinitions: Record<string, ScenarioDefinition> = {},
): Promise<void> {
	const skillDir = path.join(agentDir, "skills", skillId);
	await mkdir(path.join(skillDir, "references"), { recursive: true });
	await mkdir(path.join(skillDir, "sub-skills", "setup"), { recursive: true });
	await writeFile(
		path.join(skillDir, "SKILL.md"),
		[
			"---",
			`name: ${skillId}`,
			`description: "Use ${skillId} for focused repository workflows."`,
			"disable-model-invocation: true",
			"---",
			"",
			`# ${skillId}`,
		].join("\n"),
		"utf-8",
	);
	await writeFile(
		path.join(skillDir, "sub-skills", "setup", "SKILL.md"),
		[
			"---",
			"name: setup",
			"description: \"Setup workflow.\"",
			"disable-model-invocation: true",
			"---",
			"",
			"# Setup",
		].join("\n"),
		"utf-8",
	);
	await writeFile(
		path.join(skillDir, "references", "repo-routing-metadata.json"),
		JSON.stringify(
			{
				...(Object.keys(scenarioDefinitions).length ? { scenarios: scenarioDefinitions } : {}),
				skills: {
					[skillId]: {
						scenarios,
					},
				},
			},
			null,
			2,
		),
		"utf-8",
	);
}

async function writeMalformedRouter(agentDir: string): Promise<void> {
	const routerDir = path.join(agentDir, "skills", "repo-skills-router");
	await mkdir(path.join(routerDir, "references", "scenarios"), { recursive: true });
	await writeFile(
		path.join(routerDir, "SKILL.md"),
		[
			"---",
			"name: repo-skills-router",
			"description: malformed",
			"---",
			"",
			"# Repo Skills Router",
			"",
			"## Scenario Router",
			"### `old-skill`",
			"Role: stale root detail that should be removed.",
		].join("\n"),
		"utf-8",
	);
	await writeFile(
		path.join(routerDir, "references", "usage-scenarios.md"),
		[
			"# Usage Scenarios",
			"| Usage scenario | When to read | Scenario page | Representative repo skills |",
			"| --- | --- | --- | --- |",
			"| `broken` | Bad row | `scenarios/broken.md` | `old-skill` |",
			"",
			"## Interrupted prose inside a table",
			"| `broken` | Duplicate row | `references/scenarios/broken.md` | `old-skill` |",
		].join("\n"),
		"utf-8",
	);
	await writeFile(path.join(routerDir, "references", "repo-skills.md"), "legacy\n", "utf-8");
	await writeFile(
		path.join(routerDir, "references", "scenarios", "old.md"),
		[
			"# Old Scenario",
			"",
			"## When To Read",
			"Old tasks.",
			"",
			"## Repo Skill Options",
			"<!-- DISCO_SCENARIO:old:START -->",
			"### `old-skill`",
			"Role: Old.",
			"<!-- DISCO_SCENARIO:old:END -->",
		].join("\n"),
		"utf-8",
	);
}

describe("update_repo_skills_router.mjs", () => {
	it("rebuilds a malformed router into the canonical two-layer shape", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			await writeSkill(agentDir, "alpha-skill", [
				{
					id: "alpha-workflows",
					title: "Alpha Workflows",
					when_to_read: "Alpha repository tasks.",
					role: "Routes alpha setup and troubleshooting.",
					read_when: "The user names alpha APIs, CLIs, configs, or errors.",
					best_for: "Alpha setup and focused workflows.",
					avoid_when: "The request names beta more directly.",
					useful_entry_points: ["alpha-skill/SKILL.md", "alpha-skill/sub-skills/setup/"],
					selection_guidance: "Choose `alpha-skill` for alpha-specific work.",
				},
			]);
			await writeMalformedRouter(agentDir);

			const result = await runUpdater(agentDir);
			expect(result.code, result.stderr).toBe(0);
			expect(result.stdout).toContain("1 skills across 1 scenarios");

			const root = await readFile(path.join(agentDir, "skills", "repo-skills-router", "SKILL.md"), "utf-8");
			const usage = await readFile(
				path.join(agentDir, "skills", "repo-skills-router", "references", "usage-scenarios.md"),
				"utf-8",
			);
			const page = await readFile(
				path.join(agentDir, "skills", "repo-skills-router", "references", "scenarios", "alpha-workflows.md"),
				"utf-8",
			);

			expect(root).toContain("Usage Scenario Quick Map");
			expect(root).toContain("`references/scenarios/alpha-workflows.md`");
			expect(root).not.toContain("## Scenario Router");
			expect(root).not.toContain("### `alpha-skill`");
			expect(root.split(/\r?\n/).length).toBeLessThan(180);
			expect(usage).toContain("`scenarios/alpha-workflows.md`");
			expect(page).toContain("### `alpha-skill`");
			expect(page).toContain("Useful entry points: `alpha-skill/SKILL.md`, `alpha-skill/sub-skills/setup/`.");
			expect(existsSync(path.join(agentDir, "skills", "repo-skills-router", "references", "repo-skills.md"))).toBe(
				false,
			);
			expect(existsSync(path.join(agentDir, "skills", "repo-skills-router", "references", "scenarios", "old.md"))).toBe(
				false,
			);
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("deduplicates repeated imports and supports multiple scenarios per skill", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			await writeSkill(agentDir, "multi-skill", [
				{
					id: "training-workflows",
					title: "Training Workflows",
					when_to_read: "Training tasks.",
					role: "Handles model training.",
					selection_guidance: "Choose it for training.",
				},
				{
					id: "serving-workflows",
					title: "Serving Workflows",
					when_to_read: "Serving tasks.",
					role: "Handles model serving.",
					selection_guidance: "Choose it for serving.",
				},
			]);

			expect((await runUpdater(agentDir)).code).toBe(0);
			expect((await runUpdater(agentDir)).code).toBe(0);

			const trainingPage = await readFile(
				path.join(agentDir, "skills", "repo-skills-router", "references", "scenarios", "training-workflows.md"),
				"utf-8",
			);
			const servingPage = await readFile(
				path.join(agentDir, "skills", "repo-skills-router", "references", "scenarios", "serving-workflows.md"),
				"utf-8",
			);
			expect((trainingPage.match(/### `multi-skill`/g) ?? [])).toHaveLength(1);
			expect((servingPage.match(/### `multi-skill`/g) ?? [])).toHaveLength(1);
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("normalizes scenario aliases through the scenario registry", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			const templateDir = await writeScenarioRegistryTemplate(tempRoot);
			await writeSkill(agentDir, "agent-skill", [
				{
					id: "agent-apps",
					title: "Agent Apps",
					when_to_read: "Agent app tasks.",
					role: "Routes agent app development workflows.",
					read_when: "The request names agent apps, tool calls, or hosted agent runtimes.",
					best_for: "Agent app setup and routing decisions.",
					avoid_when: "The request is about a model serving backend.",
					useful_entry_points: ["agent-skill/SKILL.md"],
					selection_guidance: "Choose `agent-skill` for agent app workflows.",
				},
			]);

			const result = await runUpdater(agentDir, ["--template-dir", templateDir]);
			expect(result.code, result.stderr).toBe(0);
			expect(result.stdout).toContain("1 skills across 1 scenarios");

			const canonicalPage = path.join(
				agentDir,
				"skills",
				"repo-skills-router",
				"references",
				"scenarios",
				"agent-workflows.md",
			);
			const aliasPage = path.join(
				agentDir,
				"skills",
				"repo-skills-router",
				"references",
				"scenarios",
				"agent-apps.md",
			);
			const page = await readFile(canonicalPage, "utf-8");
			const usage = await readFile(
				path.join(agentDir, "skills", "repo-skills-router", "references", "usage-scenarios.md"),
				"utf-8",
			);
			const registry = JSON.parse(
				await readFile(
					path.join(agentDir, "skills", "repo-skills-router", "references", "scenario-registry.json"),
					"utf-8",
				),
			);
			expect(existsSync(canonicalPage)).toBe(true);
			expect(existsSync(aliasPage)).toBe(false);
			expect(page).toContain("# Agent Workflows");
			expect(page).toContain("### `agent-skill`");
			expect(usage).toContain("`scenarios/agent-workflows.md`");
			expect(registry.scenarios["agent-workflows"].aliases).toContain("agent-apps");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("merges duplicate entries that normalize to the same canonical scenario", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			const templateDir = await writeScenarioRegistryTemplate(tempRoot);
			await writeSkill(agentDir, "agent-skill", [
				{
					id: "agent-workflows",
					role: "Routes canonical agent workflows.",
					read_when: "The request names agent framework APIs.",
					useful_entry_points: ["agent-skill/SKILL.md"],
					selection_guidance: "Choose it for canonical agent workflows.",
				},
				{
					id: "agent-apps",
					role: "Routes alias agent app workflows.",
					read_when: "The request names agent apps or tool calling.",
					useful_entry_points: ["agent-skill/SKILL.md", "agent-skill/sub-skills/setup/"],
					selection_guidance: "Choose it for alias agent app workflows.",
				},
			]);

			const result = await runUpdater(agentDir, ["--template-dir", templateDir]);
			expect(result.code, result.stderr).toBe(0);

			const page = await readFile(
				path.join(agentDir, "skills", "repo-skills-router", "references", "scenarios", "agent-workflows.md"),
				"utf-8",
			);
			expect((page.match(/### `agent-skill`/g) ?? [])).toHaveLength(1);
			expect(page).toContain("The request names agent framework APIs. The request names agent apps or tool calling.");
			expect(page).toContain("Useful entry points: `agent-skill/SKILL.md`, `agent-skill/sub-skills/setup/`.");
			expect(page).toContain(
				"Choose `agent-skill` for canonical agent workflows. Choose `agent-skill` for alias agent app workflows.",
			);
			expect(page).not.toContain("Choose it");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("renders concrete skill ids when metadata says choose this skill", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			await writeSkill(agentDir, "alpha-skill", [
				{
					id: "alpha-workflows",
					title: "Alpha Workflows",
					when_to_read: "Alpha tasks.",
					role: "Handles alpha tasks.",
					selection_guidance: "Choose this skill when alpha configs, artifacts, workflow steps, or errors are central. Use it for alpha-specific logs.",
				},
			]);

			const result = await runUpdater(agentDir);
			expect(result.code, result.stderr).toBe(0);

			const page = await readFile(
				path.join(agentDir, "skills", "repo-skills-router", "references", "scenarios", "alpha-workflows.md"),
				"utf-8",
			);
			expect(page).toContain(
				"Choose `alpha-skill` when alpha configs, artifacts, workflow steps, or errors are central.",
			);
			expect(page).toContain("Use `alpha-skill` for alpha-specific logs.");
			expect(page).not.toContain("Choose this skill");
			expect(page).not.toContain("Use it");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("keeps dotted API names intact when merging scenario selection guidance", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			await writeSkill(agentDir, "dvc-like", [
				{
					id: "mlops-workflows",
					title: "MLOps Workflows",
					when_to_read: "MLOps tasks.",
					role: "Handles DVC-like workflows.",
					selection_guidance:
						"Choose `dvc-like` when command syntax, file formats, cache/remotes, experiment semantics, public dvc.api behavior, or repository tests matter; then route to the most specific sub-skill by task family.",
				},
			]);
			await writeSkill(agentDir, "nni-like", [
				{
					id: "mlops-workflows",
					title: "MLOps Workflows",
					when_to_read: "MLOps tasks.",
					role: "Handles NNI-like workflows.",
					selection_guidance: "Choose `nni-like` for NNI APIs and configs.",
				},
			]);

			const result = await runUpdater(agentDir);
			expect(result.code, result.stderr).toBe(0);

			const page = await readFile(
				path.join(agentDir, "skills", "repo-skills-router", "references", "scenarios", "mlops-workflows.md"),
				"utf-8",
			);
			expect(page).toContain("public dvc.api behavior");
			expect(page).not.toMatch(/(?:^|\n|\.\s+)api behavior, or repository tests matter/);
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("rejects unknown scenarios when the registry enforces canonical scenario IDs", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			const templateDir = await writeScenarioRegistryTemplate(tempRoot);
			await writeSkill(agentDir, "novel-skill", [
				{
					id: "novel-workflows",
					title: "Novel Workflows",
					when_to_read: "Novel workflow tasks.",
					role: "Routes a new unsupported workflow family.",
				},
			]);

			const result = await runUpdater(agentDir, ["--template-dir", templateDir]);
			expect(result.code).toBe(2);
			expect(result.stderr).toContain("uses unknown scenario novel-workflows");
			expect(result.stderr).toContain("scenario-registry.json");
			expect(result.stderr).toContain("allow_new");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("allows explicitly justified new scenarios and persists them to the registry", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			const templateDir = await writeScenarioRegistryTemplate(tempRoot);
			await writeSkill(
				agentDir,
				"robot-skill",
				[
					{
						id: "robot-planning-workflows",
						role: "Routes robot planning workflows.",
						read_when: "The request names robot planning, task planning, or manipulator policies.",
						selection_guidance: "Choose `robot-skill` for robot planning tasks.",
					},
				],
				{
					"robot-planning-workflows": {
						title: "Robot Planning Workflows",
						when_to_read: "Robot task planning, policy configuration, and manipulator workflow tasks.",
						how_to_choose: "Choose this skill by the named robot planning package, planner API, or task policy. Use it for planner tasks. Route here for robot planning errors.",
						allow_new: true,
						why_not_existing: "Existing agent workflow scenarios cover LLM agent runtimes, not robot planning stacks.",
						expected_future_reuse: "Future robotics repositories can route here for planner and policy workflow skills.",
					},
				},
			);

			const result = await runUpdater(agentDir, ["--template-dir", templateDir]);
			expect(result.code, result.stderr).toBe(0);
			expect(result.stdout).toContain("1 skills across 1 scenarios");

			const registry = JSON.parse(
				await readFile(
					path.join(agentDir, "skills", "repo-skills-router", "references", "scenario-registry.json"),
					"utf-8",
				),
			);
			const page = await readFile(
				path.join(
					agentDir,
					"skills",
					"repo-skills-router",
					"references",
					"scenarios",
					"robot-planning-workflows.md",
				),
				"utf-8",
			);
			expect(registry.scenarios["robot-planning-workflows"].title).toBe("Robot Planning Workflows");
			expect(registry.scenarios["robot-planning-workflows"].split_guidance).toContain(
				"Existing agent workflow scenarios cover LLM agent runtimes",
			);
			expect(registry.scenarios["robot-planning-workflows"].split_guidance).toContain(
				"Future robotics repositories can route to the matching scenario for planner and policy workflow skills.",
			);
			expect(registry.scenarios["robot-planning-workflows"].split_guidance).not.toContain("route here");
			expect(registry.scenarios["robot-planning-workflows"].how_to_choose).toContain(
				"Choose the matching repo skill by the named robot planning package",
			);
			expect(registry.scenarios["robot-planning-workflows"].how_to_choose).not.toContain("Choose this skill");
			expect(registry.scenarios["robot-planning-workflows"].how_to_choose).not.toContain("Use it");
			expect(page).toContain("### `robot-skill`");
			expect(page).toContain("Choose the matching repo skill by the named robot planning package");
			expect(page).toContain("Use the matching repo skill for planner tasks.");
			expect(page).toContain("Route to the matching scenario for robot planning errors.");
			expect(page).not.toContain("Choose this skill");
			expect(page).not.toContain("Use it");
			expect(page).not.toContain("Route here");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("preserves existing scenario entries recovered from the live router", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			await writeSkill(agentDir, "old-skill", [
				{
					id: "old-workflows",
					title: "Old Workflows",
					when_to_read: "Old tasks.",
					role: "Handles old tasks.",
					selection_guidance: "Choose old for old tasks.",
				},
			]);
			expect((await runUpdater(agentDir)).code).toBe(0);

			await rm(path.join(agentDir, "skills", "old-skill", "references", "repo-routing-metadata.json"));
			await writeSkill(agentDir, "new-skill", [
				{
					id: "new-workflows",
					title: "New Workflows",
					when_to_read: "New tasks.",
					role: "Handles new tasks.",
					selection_guidance: "Choose new for new tasks.",
				},
			]);

			const result = await runUpdater(agentDir);
			expect(result.code, result.stderr).toBe(0);
			expect(result.stdout).toContain("backfilled 1 routing metadata files");

			const oldPage = await readFile(
				path.join(agentDir, "skills", "repo-skills-router", "references", "scenarios", "old-workflows.md"),
				"utf-8",
			);
			const newPage = await readFile(
				path.join(agentDir, "skills", "repo-skills-router", "references", "scenarios", "new-workflows.md"),
				"utf-8",
			);
			expect(oldPage).toContain("### `old-skill`");
			expect(newPage).toContain("### `new-skill`");
			expect((oldPage.match(/Choose old for old tasks\./g) ?? [])).toHaveLength(1);

			const recoveredMetadata = JSON.parse(
				await readFile(path.join(agentDir, "skills", "old-skill", "references", "repo-routing-metadata.json"), "utf-8"),
			);
			expect(recoveredMetadata).not.toHaveProperty("scenarios");
			expect(recoveredMetadata.skills["old-skill"].scenarios).toEqual([
				expect.objectContaining({
					id: "old-workflows",
					role: "Handles old tasks.",
					selection_guidance: expect.stringContaining("Choose `old-skill`"),
				}),
			]);
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("can generate a router view for only selected skills without mutating the live router", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			await writeSkill(agentDir, "alpha-skill", [
				{
					id: "shared-workflows",
					title: "Shared Workflows",
					when_to_read: "Shared tasks.",
					role: "Handles alpha shared tasks.",
					selection_guidance: "Choose `alpha-skill` for alpha-owned task shapes.",
				},
			]);
			await writeSkill(agentDir, "beta-skill", [
				{
					id: "shared-workflows",
					title: "Shared Workflows",
					when_to_read: "Shared tasks.",
					role: "Handles beta shared tasks.",
					selection_guidance: "Choose `beta-skill` for beta-owned task shapes.",
				},
			]);
			await writeSkill(agentDir, "gamma-skill", [
				{
					id: "shared-workflows",
					title: "Shared Workflows",
					when_to_read: "Shared tasks.",
					role: "Handles gamma shared tasks.",
					selection_guidance: "Choose `gamma-skill` for gamma-owned task shapes.",
				},
			]);

			const fullResult = await runUpdater(agentDir);
			expect(fullResult.code, fullResult.stderr).toBe(0);

			const outputRouterDir = path.join(tempRoot, "filtered-router");
			const filteredResult = await runUpdater(agentDir, [
				"--include-skill",
				"alpha-skill,beta-skill",
				"--output-router-dir",
				outputRouterDir,
			]);
			expect(filteredResult.code, filteredResult.stderr).toBe(0);
			expect(filteredResult.stdout).toContain("for alpha-skill, beta-skill: 2 skills across 1 scenarios");

			const filteredRoot = await readFile(path.join(outputRouterDir, "SKILL.md"), "utf-8");
			const filteredSharedPage = await readFile(
				path.join(outputRouterDir, "references", "scenarios", "shared-workflows.md"),
				"utf-8",
			);
			expect(filteredRoot).toContain("`alpha-skill`, `beta-skill`");
			expect(filteredRoot).not.toContain("gamma-skill");
			expect(filteredSharedPage).toContain("### `alpha-skill`");
			expect(filteredSharedPage).toContain("### `beta-skill`");
			expect(filteredSharedPage).not.toContain("gamma-skill");

			const liveSharedPage = await readFile(
				path.join(agentDir, "skills", "repo-skills-router", "references", "scenarios", "shared-workflows.md"),
				"utf-8",
			);
			expect(liveSharedPage).toContain("### `gamma-skill`");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("does not feed recovered scenario How To Choose back into every recovered skill", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			await writeSkill(agentDir, "old-alpha", [
				{
					id: "shared-workflows",
					title: "Shared Workflows",
					when_to_read: "Shared tasks.",
					role: "Handles alpha shared tasks.",
					selection_guidance: "Choose alpha for alpha-owned task shapes.",
				},
			]);
			await writeSkill(agentDir, "old-beta", [
				{
					id: "shared-workflows",
					title: "Shared Workflows",
					when_to_read: "Shared tasks.",
					role: "Handles beta shared tasks.",
					selection_guidance: "Choose beta for beta-owned task shapes.",
				},
			]);
			expect((await runUpdater(agentDir)).code).toBe(0);

			await rm(path.join(agentDir, "skills", "old-alpha", "references", "repo-routing-metadata.json"));
			await rm(path.join(agentDir, "skills", "old-beta", "references", "repo-routing-metadata.json"));
			await writeSkill(agentDir, "new-gamma", [
				{
					id: "shared-workflows",
					title: "Shared Workflows",
					when_to_read: "Shared tasks.",
					role: "Handles gamma shared tasks.",
					selection_guidance: "Choose gamma for gamma-owned task shapes.",
				},
			]);

			const result = await runUpdater(agentDir);
			expect(result.code, result.stderr).toBe(0);

			const page = await readFile(
				path.join(agentDir, "skills", "repo-skills-router", "references", "scenarios", "shared-workflows.md"),
				"utf-8",
			);
			expect((page.match(/Choose alpha for alpha-owned task shapes\./g) ?? [])).toHaveLength(1);
			expect((page.match(/Choose beta for beta-owned task shapes\./g) ?? [])).toHaveLength(1);
			expect((page.match(/Choose gamma for gamma-owned task shapes\./g) ?? [])).toHaveLength(1);
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("fails validation when a live skill has no routing metadata or recovered router entry", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			const skillDir = path.join(agentDir, "skills", "unrouted-skill");
			await mkdir(skillDir, { recursive: true });
			await writeFile(
				path.join(skillDir, "SKILL.md"),
				[
					"---",
					"name: unrouted-skill",
					"description: \"Missing routing metadata.\"",
					"disable-model-invocation: true",
					"---",
					"",
					"# Unrouted",
				].join("\n"),
				"utf-8",
			);

			const result = await runUpdater(agentDir);
			expect(result.code).toBe(2);
			expect(result.stderr).toContain("routing metadata is missing live repo skills");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("fails validation when a non-router repo skill is model-visible", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			const skillDir = path.join(agentDir, "skills", "visible-skill");
			await mkdir(path.join(skillDir, "references"), { recursive: true });
			await writeFile(
				path.join(skillDir, "SKILL.md"),
				[
					"---",
					"name: visible-skill",
					"description: \"Visible repo skill should fail router preflight.\"",
					"---",
					"",
					"# Visible Skill",
				].join("\n"),
				"utf-8",
			);
			await writeFile(
				path.join(skillDir, "references", "repo-routing-metadata.json"),
				JSON.stringify({
					skills: {
						"visible-skill": {
							scenarios: [{ id: "visible-workflows", role: "Handles visible workflows." }],
						},
					},
				}),
				"utf-8",
			);

			const result = await runUpdater(agentDir);
			expect(result.code).toBe(2);
			expect(result.stderr).toContain("frontmatter must contain disable-model-invocation: true");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("fails validation when the existing router is hidden from model invocation", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			await writeSkill(agentDir, "alpha-skill", [
				{
					id: "alpha-workflows",
					title: "Alpha Workflows",
					when_to_read: "Alpha tasks.",
					role: "Handles alpha tasks.",
				},
			]);
			const routerDir = path.join(agentDir, "skills", "repo-skills-router");
			await mkdir(routerDir, { recursive: true });
			await writeFile(
				path.join(routerDir, "SKILL.md"),
				[
					"---",
					"name: repo-skills-router",
					"description: \"Router should stay visible.\"",
					"disable-model-invocation: true",
					"---",
					"",
					"# Repo Skills Router",
				].join("\n"),
				"utf-8",
			);

			const result = await runUpdater(agentDir);
			expect(result.code).toBe(2);
			expect(result.stderr).toContain("must stay model-visible");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("fails validation when routing metadata points at a missing entry point", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			await writeSkill(agentDir, "alpha-skill", [
				{
					id: "alpha-workflows",
					title: "Alpha Workflows",
					when_to_read: "Alpha tasks.",
					role: "Handles alpha tasks.",
					useful_entry_points: ["alpha-skill/SKILL.md", "alpha-skill/sub-skills/missing/"],
				},
			]);

			const result = await runUpdater(agentDir);
			expect(result.code).toBe(2);
			expect(result.stderr).toContain("useful entry point for alpha-skill/alpha-workflows does not exist");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("serializes concurrent router updates through the import lock by default", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			await writeSkill(agentDir, "alpha-skill", [
				{
					id: "shared-workflows",
					title: "Shared Workflows",
					when_to_read: "Shared tasks.",
					role: "Handles alpha shared tasks.",
				},
			]);
			await writeSkill(agentDir, "beta-skill", [
				{
					id: "shared-workflows",
					title: "Shared Workflows",
					when_to_read: "Shared tasks.",
					role: "Handles beta shared tasks.",
				},
			]);

			const [first, second] = await Promise.all([runUpdater(agentDir), runUpdater(agentDir)]);
			expect(first.code, first.stderr).toBe(0);
			expect(second.code, second.stderr).toBe(0);

			const page = await readFile(
				path.join(agentDir, "skills", "repo-skills-router", "references", "scenarios", "shared-workflows.md"),
				"utf-8",
			);
			expect((page.match(/### `alpha-skill`/g) ?? [])).toHaveLength(1);
			expect((page.match(/### `beta-skill`/g) ?? [])).toHaveLength(1);
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});

	it("requires an actual lock when --already-locked is used", async () => {
		const tempRoot = await mkdtemp(path.join(tmpdir(), "disco-router-"));
		try {
			const agentDir = path.join(tempRoot, "agent");
			await writeSkill(agentDir, "alpha-skill", [
				{
					id: "alpha-workflows",
					title: "Alpha Workflows",
					when_to_read: "Alpha tasks.",
					role: "Handles alpha tasks.",
				},
			]);
			const result = await runUpdater(agentDir, ["--already-locked"]);
			expect(result.code).toBe(2);
			expect(result.stderr).toContain("--already-locked requires DISCO_IMPORT_LOCK_PATH");
		} finally {
			await rm(tempRoot, { recursive: true, force: true });
		}
	});
});
