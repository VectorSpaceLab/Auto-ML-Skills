import { describe, expect, it } from "vitest";
import { parseArgs } from "./args.ts";
import { buildInitialMessage } from "./initial-message.ts";
import { buildSourceRoutingPrompt } from "./source-routing.ts";

describe("source workflow routing", () => {
	it("uses auto classification guidance when --source is omitted", () => {
		const parsed = parseArgs(["-p", "Create a skill for /path/to/repo"]);

		expect(parsed.source).toBeUndefined();
		const prompt = buildSourceRoutingPrompt(parsed.source);
		expect(prompt).toContain("source=auto");
		expect(prompt).toContain("make an explicit source workflow decision");
		expect(prompt).toContain("create-repo-skill");
		expect(prompt).toContain("create-paper-skills");
		expect(prompt).toContain("Ask the user to confirm");
	});

	it("parses explicit package source mode", () => {
		const parsed = parseArgs(["--source", "package", "-p", "Create a skill for /path/to/repo"]);

		expect(parsed.source).toBe("package");
		const prompt = buildSourceRoutingPrompt(parsed.source);
		expect(prompt).toContain("source=package");
		expect(prompt).toContain("selected the package/repo skill workflow");
	});

	it("parses explicit paper source mode", () => {
		const parsed = parseArgs(["--source=paper", "-p", "Use Distiller to process this paper"]);

		expect(parsed.source).toBe("paper");
		const prompt = buildSourceRoutingPrompt(parsed.source);
		expect(prompt).toContain("source=paper");
		expect(prompt).toContain("create-paper-skills");
		expect(prompt).toContain("paper-skills-distiller");
		expect(prompt).toContain("default to 10 refine cycles");
		expect(prompt).toContain("discover an implementation repo only when authorized");
		expect(prompt).toContain("<workspace_root>/<slug>/");
		expect(prompt).toContain("distillation/");
		expect(prompt).toContain("skills/");
		expect(prompt).toContain("prepare-paper-recovery-env before recovery");
		expect(prompt).toContain("reports/final");
	});

	it("rejects invalid source mode", () => {
		const parsed = parseArgs(["--source", "repo"]);

		expect(parsed.diagnostics).toContainEqual({
			type: "error",
			message: 'Invalid source "repo". Valid values: package, paper',
		});
	});

	it("requires a source mode value", () => {
		const parsed = parseArgs(["--source"]);

		expect(parsed.diagnostics).toContainEqual({
			type: "error",
			message: "--source requires a value: package or paper",
		});
	});

	it("does not mutate the user initial message", async () => {
		const parsed = parseArgs(["--source", "paper", "-p", "Use Distiller to process this paper"]);
		const initial = await buildInitialMessage({ parsed });

		expect(initial.initialMessage).toBe("Use Distiller to process this paper");
		expect(buildSourceRoutingPrompt(parsed.source)).toContain("source=paper");
	});
});
