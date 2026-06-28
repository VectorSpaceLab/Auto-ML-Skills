import type { SourceKind } from "./args.ts";

export function buildSourceRoutingPrompt(source: SourceKind | undefined): string {
	if (source === "paper") {
		return [
			"source=paper",
			"The user selected the Paper2Skills Distiller workflow. Treat this as a peer workflow to the package/repo skill workflow, not as a repo-skill refresh or extension task.",
			"Use create-paper-skills as the entry skill, then paper-skills-distiller. Accept local PDFs/text, direct PDF URLs, arXiv ids/URLs, paper titles, or paper/repo pairs. Resolve and download/clone remote sources when permitted, discover an implementation repo only when authorized by config or user confirmation, and ask the user to choose when a title or repo search is ambiguous.",
			"Prefer a TOML run config for batch or repeatable work. If required paper, repository, recovery target, runtime constraints, or iteration budget fields are missing, ask concise clarification questions before expensive source acquisition or recovery work. If iteration_budget is omitted, default to 10 refine cycles after the first recovery.",
			"Paper runs must use the organized <workspace_root>/<slug>/ layout with distillation/ for process artifacts and skills/ for generated skills, validate every generated module skill with attempted tests, run prepare-paper-recovery-env before recovery, and write final_report.md/json under distillation/reports/final before reporting completion.",
			"Recovery must produce executable evidence unless a concrete blocker is recorded. In hard mode, do not accept reduced, proxy, toy, smaller-model, or fallback experiments as success. In soft mode, reduced/proxy recovery may count only when declared, justified, mechanism-checked, validator-approved, and logged.",
		].join("\n");
	}

	if (source === "package") {
		return [
			"source=package",
			"The user selected the package/repo skill workflow. This is DisCo's original workflow.",
			"For new repo/package skill creation, use create-repo-skill as the entry skill. If the user did not provide a repository path, use the current working directory; if they did not provide a Python inspection environment, first analyze the repository structure, confirm scope when needed, then use prepare-repo-skill-env before continuing.",
			"Keep the existing package workflow semantics for refresh, extension, verification, and import requests: use refresh-repo-skill, extend-repo-skill, verify-repo-skill, or import-repo-skills-to-agent when those are the user's actual request.",
		].join("\n");
	}

	return [
		"source=auto",
		"No --source value was provided. Before starting skill creation, make an explicit source workflow decision from the user's request and visible evidence.",
		"Classify the request as package/repo workflow when it asks to create, refresh, extend, verify, import, or export skills from a software repository/package, installed environment, source checkout, or current working directory. Then use create-repo-skill or the matching package workflow skill.",
		"Classify the request as paper workflow when it provides a paper PDF/text, paper URL, arXiv id/URL, paper title, Distiller config, or asks to convert/recover an AI research paper into skills. Then use create-paper-skills followed by paper-skills-distiller.",
		"At the start of the run, state the decision in one concise line such as `Source workflow decision: paper` or `Source workflow decision: package`, with the evidence. Ask the user to confirm the selected workflow before starting substantive skill generation unless the prompt/config already explicitly authorizes automatic decisions or this is a non-interactive batch request with an unambiguous source. Always ask when the classification is ambiguous, when both workflows are plausible, or when the next step would perform expensive source acquisition or recovery.",
		"If the request is clearly a repo/package task and the user gave no paper evidence, package/repo is the conservative fallback. If the request is clearly a paper task, do not route it through repo-skill refresh or extension just because an implementation repository is mentioned.",
	].join("\n");
}
