import { describe, expect, it } from "vitest";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DefaultPackageManager } from "../../core/package-manager.ts";
import type { SettingsManager } from "../../core/settings-manager.ts";
import { buildSystemPrompt } from "../../core/system-prompt.ts";
import { WorkflowAgent } from "./agent.ts";
import { createWorkflowTool } from "./workflow-tool.ts";

function createSettingsManagerStub(globalSettings: Record<string, unknown> = {}): SettingsManager {
  return {
    getGlobalSettings: () => globalSettings,
    getProjectSettings: () => ({}),
    isProjectTrusted: () => false,
    setProjectTrusted: () => {},
  } as unknown as SettingsManager;
}

describe("WorkflowAgent sub-skill prompting", () => {
  it("tells sub-skill agents to write files directly instead of returning draft bodies", () => {
    const agent = new WorkflowAgent({ cwd: process.cwd(), tools: [] });
    const prompt = (
      agent as unknown as {
        buildPrompt(task: string, options: { label: string; subSkill: string }, structured: boolean): string;
      }
    ).buildPrompt("Draft the assigned sub-skill.", { label: "draft data", subSkill: "data-indexing" }, false);

    expect(prompt).toContain("Assigned sub-skill: data-indexing.");
    expect(prompt).toContain("write the runtime files directly in the planned output subtree before returning");
    expect(prompt).toContain("propose one or two difficult synthetic usability cases for this sub-skill");
    expect(prompt).toContain("Concrete cases belong under the artifact root's `test-cases/`");
    expect(prompt).toContain("Do not return full Markdown or script bodies for the parent/main agent to write later");
  });

  it("keeps structured output as a handoff manifest after file creation", () => {
    const agent = new WorkflowAgent({ cwd: process.cwd(), tools: [] });
    const prompt = (
      agent as unknown as {
        buildPrompt(task: string, options: { label: string; subSkill: string }, structured: boolean): string;
      }
    ).buildPrompt(
      "Draft the assigned sub-skill and return a manifest.",
      { label: "draft data", subSkill: "data-indexing" },
      true,
    );

    expect(prompt).toContain("Your final action MUST be a structured_output tool call.");
    expect(prompt).toContain("write those files with the available file tools before structured_output");
    expect(prompt).toContain("not contain drafts for a parent agent to write later");
  });
});

describe("workflow tool DisCo generation guidance", () => {
  it("requires source-script import planning and troubleshooting coverage in sub-skill briefs", () => {
    const tool = createWorkflowTool({ cwd: process.cwd() });
    const guidelines = tool.promptGuidelines?.join("\n") ?? "";

    expect(guidelines).toContain("source-script import/adaptation plan");
    expect(guidelines).toContain("troubleshooting failure modes to cover");
    expect(guidelines).toContain("one or two difficult synthetic usability case ideas for that sub-skill");
    expect(guidelines).toContain("Paper2Skills module-skill generation");
    expect(guidelines).toContain("module drafting/revision agents must write their assigned generated module skill files directly");
    expect(guidelines).toContain("sub-skill drafting/revision agents must write their assigned files directly");
    expect(guidelines).toContain("concrete usability/native-backed/synthetic cases belong under the artifact root's test-cases/ subtree");
    expect(guidelines).toContain("plan one or two integrated difficult cases");
  });
});

describe("DisCo agent positioning", () => {
	it("does not position DisCo as a runtime user of generated skills", () => {
		const prompt = buildSystemPrompt({ cwd: process.cwd(), selectedTools: [] });

		expect(prompt).toContain("creating, refreshing, extending, validating, importing, exporting, and maintaining Agent Skills");
		expect(prompt).toContain("AI research papers into high-quality skills");
		expect(prompt).toContain("Treat package/repo skill extraction and paper skill extraction as peer workflows");
		expect(prompt).toContain("make an explicit source decision");
		expect(prompt).toContain("start create-paper-skills first and then paper-skills-distiller");
		expect(prompt).toContain("During paper skill generation, the main agent owns the paper profile");
		expect(prompt).toContain("managed skill library and export source, not a runtime skill source");
		expect(prompt).toContain("explicit export of DisCo's managed skill library into another agent tool");
		expect(prompt).toContain("before creating, verifying, refreshing, extending, or exporting skills");
    expect(prompt).toContain("Do not automatically synchronize imported repo skills into other agent tools");
    expect(prompt).toContain("target repo-skills-router content must be generated from only the selected repo skills");
    expect(prompt).toContain("never copy the full DisCo-managed router into the target for a subset export");
    expect(prompt).toContain("verify-repo-skill/scripts/update_repo_skills_router.mjs");
    expect(prompt).toContain("Do not hand-edit router Markdown as the import mechanism");
    expect(prompt).toContain("Use the dedicated import-repo-skills-to-agent meta skill only when the user explicitly asks");
    expect(prompt).not.toContain("importing, and using Agent Skills");
    expect(prompt).not.toContain("use existing skills to complete tasks");
  });

  it("keeps the DisCo managed skills directory out of automatic runtime skill loading", async () => {
    const tempRoot = mkdtempSync(join(tmpdir(), "disco-test-"));
    try {
      const agentDir = join(tempRoot, "agent");
      const userSkillDir = join(agentDir, "skills", "managed-user-skill");
      mkdirSync(userSkillDir, { recursive: true });
      writeFileSync(
        join(userSkillDir, "SKILL.md"),
        [
          "---",
          "name: managed-user-skill",
          "description: This managed skill should stay in the library and not autoload.",
          "---",
          "",
          "# Managed User Skill",
        ].join("\n"),
      );

      const manager = new DefaultPackageManager({
        cwd: tempRoot,
        agentDir,
        settingsManager: createSettingsManagerStub(),
      });
      const resolved = await manager.resolve(async () => "skip");
      const resolvedSkillPaths = resolved.skills.map((entry) => entry.path);

      expect(resolvedSkillPaths.some((path) => path.includes("managed-user-skill"))).toBe(false);
      expect(resolvedSkillPaths.some((path) => path.includes("create-repo-skill"))).toBe(true);
      expect(resolvedSkillPaths.some((path) => path.includes("create-paper-skills"))).toBe(true);
      expect(resolvedSkillPaths.some((path) => path.includes("paper-skills-distiller"))).toBe(true);
      expect(resolvedSkillPaths.some((path) => path.includes("recover-paper-result"))).toBe(true);
    } finally {
      rmSync(tempRoot, { recursive: true, force: true });
    }
  });

  it("still honors explicitly configured skill paths", async () => {
    const tempRoot = mkdtempSync(join(tmpdir(), "disco-test-"));
    try {
      const agentDir = join(tempRoot, "agent");
      const explicitSkillDir = join(tempRoot, "explicit-skill");
      mkdirSync(explicitSkillDir, { recursive: true });
      writeFileSync(
        join(explicitSkillDir, "SKILL.md"),
        [
          "---",
          "name: explicit-skill",
          "description: This explicitly configured skill should load.",
          "---",
          "",
          "# Explicit Skill",
        ].join("\n"),
      );

      const manager = new DefaultPackageManager({
        cwd: tempRoot,
        agentDir,
        settingsManager: createSettingsManagerStub({ skills: [explicitSkillDir] }),
      });
      const resolved = await manager.resolve(async () => "skip");
      const resolvedSkillPaths = resolved.skills.map((entry) => entry.path);

      expect(resolvedSkillPaths.some((path) => path.includes("explicit-skill"))).toBe(true);
    } finally {
      rmSync(tempRoot, { recursive: true, force: true });
    }
  });
});

describe("create-repo-skill authoring constraints", () => {
  function readSkillReference(relativePath: string): string {
    return readFileSync(join(process.cwd(), "src/disco/skills/create-repo-skill", relativePath), "utf-8");
  }

  it("requires useful repo scripts to be imported, adapted, wrapped, or explicitly excluded", () => {
    const skill = readSkillReference("SKILL.md");
    const evidence = readSkillReference("references/repository-evidence.md");
    const planning = readSkillReference("references/planning-and-writing.md");

    expect(skill).toContain("source script inventory");
    expect(skill).toContain("Do not replace a useful, safe, repo-maintained script with prose-only Markdown");
    expect(evidence).toContain("Build a separate source script inventory");
    expect(evidence).toContain("Do not use `reference-only` merely because prose is easier");
    expect(planning).toContain("source script import map");
    expect(planning).toContain("Script import failure");
  });

  it("requires troubleshooting coverage maps and actionable troubleshooting references", () => {
    const skill = readSkillReference("SKILL.md");
    const planning = readSkillReference("references/planning-and-writing.md");

    expect(skill).toContain("Every generated package repo skill should include troubleshooting guidance");
    expect(skill).toContain("references/repo-routing-metadata.json");
    expect(skill).toContain("update_repo_skills_router.mjs");
    expect(planning).toContain("troubleshooting coverage map");
    expect(planning).toContain("Troubleshooting references should be actionable");
    expect(planning).toContain("Troubleshooting failure");
  });

  it("separates test cases from reports in the review artifact tree", () => {
    const skill = readSkillReference("SKILL.md");
    const structure = readSkillReference("references/input-output-and-structure.md");
    const planning = readSkillReference("references/planning-and-writing.md");

    expect(skill).toContain("with concrete cases in `test-cases/` and reports or review documents in `reports/`");
    expect(structure).toContain("<artifact-root>/");
    expect(structure).toContain("test-cases/              # concrete usability/native-backed/synthetic cases");
    expect(structure).toContain("reports/                 # review, verification, and final handoff documents");
    expect(structure).toContain("The artifact root should not contain loose case directories or a catch-all");
    expect(planning).toContain("reports/integration/coverage-depth-matrix.md");
    expect(planning).toContain("reports/integration/difficult-case-plan.md");
  });

  it("requires difficult synthetic cases per sub-skill and integrated hard cases", () => {
    const skill = readSkillReference("SKILL.md");
    const planning = readSkillReference("references/planning-and-writing.md");

    expect(skill).toContain("plan one or two integrated difficult usability cases");
    expect(skill).toContain("prefer adapting real repo tests/examples from the native candidate map");
    expect(planning).toContain("One or two new difficult synthetic usability case ideas for that sub-skill");
    expect(planning).toContain("Every sub-skill has one or two planned difficult synthetic cases");
    expect(planning).toContain("The whole-skill plan includes one or two integrated difficult cases");
  });
});

describe("verify-repo-skill artifact constraints", () => {
  function readVerifyReference(relativePath: string): string {
    return readFileSync(join(process.cwd(), "src/disco/skills/verify-repo-skill", relativePath), "utf-8");
  }

  it("writes concrete cases under test-cases and review deliverables under reports", () => {
    const skill = readVerifyReference("SKILL.md");
    const cases = readVerifyReference("references/usability-test-cases.md");
    const handoff = readVerifyReference("references/evaluation-verification-and-handoff.md");
    const runner = readVerifyReference("scripts/run_native_cases.py");

    expect(skill).toContain("Write concrete test cases under `test-cases/` and reports or review");
    expect(skill).toContain("scripts/update_repo_skills_router.mjs");
    expect(skill).toContain("Do not hand-edit router Markdown as the import mechanism");
    expect(cases).toContain("<repository-path>/skills/tests/<chosen-skill-id>/test-cases/");
    expect(cases).toContain("sub-skills/<sub-skill-id>/<scenario-slug>/");
    expect(cases).toContain("integration/<scenario-slug>/");
    expect(handoff).toContain("reports/verification/native-verification-report.json");
    expect(handoff).toContain("reports/final/final-skill-report.md");
    expect(runner).toContain("--manifest reports/verification/native-ground-truth-candidates.json");
  });

  it("requires per-sub-skill difficult cases plus integrated difficult cases", () => {
    const skill = readVerifyReference("SKILL.md");
    const cases = readVerifyReference("references/usability-test-cases.md");
    const handoff = readVerifyReference("references/evaluation-verification-and-handoff.md");

    expect(skill).toContain("For every generated");
    expect(skill).toContain("create one or two new difficult synthetic cases");
    expect(skill).toContain("create one or two integrated difficult cases");
    expect(cases).toContain("For every generated sub-skill, create one or two new difficult synthetic case");
    expect(cases).toContain("After all sub-skills are integrated, create one or two integrated difficult");
    expect(handoff).toContain("Every generated sub-skill has one or two new difficult synthetic cases");
    expect(handoff).toContain("The complete integrated skill has one or two difficult integration cases");
  });
});

describe("repo skills router and export meta-skill constraints", () => {
  function readRepoRouter(relativePath: string): string {
    return readFileSync(join(process.cwd(), "src/disco/skills/repo-skills-router", relativePath), "utf-8");
  }

  function readImportSkill(relativePath: string): string {
    return readFileSync(join(process.cwd(), "src/disco/skills/import-repo-skills-to-agent", relativePath), "utf-8");
  }

  it("defines repo-skills-router as a two-layer usage-scenario router", () => {
    const skill = readRepoRouter("SKILL.md");
    const scenarios = readRepoRouter("references/usage-scenarios.md");
    const maintenance = readRepoRouter("references/maintenance.md");

    expect(skill).toContain("name: repo-skills-router");
    expect(skill).toContain("two-layer progressive disclosure");
    expect(skill).toContain("Usage Scenario Quick Map");
    expect(skill).toContain("references/scenarios/<scenario>.md");
    expect(skill).toContain("how similar repo skills differ");
    expect(skill).toContain("selection guideline");
    expect(scenarios).toContain("Repo Skill Options");
    expect(scenarios).toContain("## How To Choose");
    expect(scenarios).toContain("Do not create a separate third layer for");
    expect(scenarios).toContain("similar-skill differences");
    expect(maintenance).toContain("scripts/update_repo_skills_router.mjs");
    expect(maintenance).toContain("references/repo-routing-metadata.json");
    expect(maintenance).toContain("Do not hand-edit router Markdown as the import mechanism");
  });

  it("defines import-repo-skills-to-agent overwrite prompts and router merge behavior", () => {
    const skill = readImportSkill("SKILL.md");

    expect(skill).toContain("Use this meta skill to copy DisCo's managed skill library into another");
    expect(skill).toContain("agent tool");
    expect(skill).toContain("If the path basename is `skills`, treat it as the target skills root");
    expect(skill).toContain("Ask the user whether to overwrite the target copy");
    expect(skill).toContain("Never silently overwrite a non-router skill");
    expect(skill).toContain("If the target already");
    expect(skill).toContain("has `repo-skills-router`, merge the filtered");
    expect(skill).toContain("must be a filtered router for the selected import set");
    expect(skill).toContain("--include-skill <selected-skill-id>");
    expect(skill).toContain("--output-router-dir <temp-dir>/repo-skills-router");
    expect(skill).toContain("Do not copy");
    expect(skill).toContain("directly for a subset import");
    expect(skill).toContain("Preserve target-only scenario rows and scenario pages");
    expect(skill).toContain("the target router does not gain entries for unselected DisCo source");
    expect(skill).toContain("Keep the two-layer structure");
  });
});
