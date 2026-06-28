import { defineTool, type ToolDefinition } from "../../core/extensions/types.ts";
import { Text } from "@auto-ml-skills/disco-tui";
import { Type } from "typebox";
import { listAvailableModelSpecs } from "./agent.ts";
import { listAgentTypes, loadAgentRegistry } from "./agent-registry.ts";
import {
  createToolUpdateWorkflowDisplay,
  createWorkflowSnapshot,
  recomputeWorkflowSnapshot,
  renderWorkflowText,
  type WorkflowSnapshot,
} from "./display.ts";
import { WorkflowError, WorkflowErrorCode } from "./errors.ts";
import { parseWorkflowScript, type WorkflowRunResult } from "./workflow.ts";
import { WorkflowManager } from "./workflow-manager.ts";
import { createWorkflowStorage, type WorkflowStorage } from "./workflow-saved.ts";
import { loadWorkflowSettings } from "./workflow-settings.ts";

/**
 * Model routing guideline for workflow authors.
 * Tells the LLM about opts.tier (small/medium/big) for runtime-enforced
 * model selection, and opts.model for an exact provider/id override.
 *
 * This string is injected into the workflow tool's promptGuidelines and
 * therefore appears in the LLM's system prompt for every workflow execution.
 */
export function modelRoutingGuideline(): string {
  const available = listAvailableModelSpecs();
  const list = available.length
    ? `The user's currently available models (route only to these) are: ${available.join(", ")}.`
    : "Use models the user has configured.";
  return [
    "For workflow, the user configures per-tier models (/workflows-models), so TAG EVERY agent with opts.tier by role so those models are actually used.",
    "opts.tier accepts 'small', 'medium', or 'big' and is enforced at runtime.",
    "Small tier: lightweight exploration/search/inventory agents.",
    "Medium tier: balanced analysis agents.",
    "Big tier: synthesis/judgment/decision agents spanning the full context.",
    "An agent with no opts.tier and no opts.model falls back to the user's medium tier; do not rely on that — tag agents explicitly so small/big are used where they fit.",
    "If the user named a specific model, use opts.model with that exact provider/id; opts.model always takes precedence over opts.tier.",
    list,
  ].join(" ");
}

/**
 * Tells the LLM which named subagent definitions (agentType) are available, so
 * it can route an agent() to a reusable role that binds tools+model+prompt.
 * Returns undefined when no definitions are registered (nothing to advertise).
 */
export function agentTypeGuideline(cwd: string = process.cwd()): string | undefined {
  let types: Array<{ name: string; description?: string }>;
  try {
    types = listAgentTypes(loadAgentRegistry(cwd));
  } catch {
    return undefined;
  }
  if (!types.length) return undefined;
  const list = types.map((t) => (t.description ? `${t.name} (${t.description})` : t.name)).join(", ");
  return `For workflow, opts.agentType routes an agent to a named definition that binds its tools, model, and role prompt. Available agentTypes: ${list}. An explicit opts.model still overrides the definition's model.`;
}

const workflowToolSchema = Type.Object({
  script: Type.String({
    description: [
      "Required raw JavaScript workflow script, with no Markdown fences.",
      "First statement: export const meta = { name: 'short_snake_case', description: 'non-empty description', phases: [{ title: 'Phase' }] }",
      "Use phase('Name'), agent(prompt, opts), parallel(arrayOfFunctions), pipeline(items, ...stages), log(message), args, and budget. DisCo also supports agent(prompt, { subSkill: 'planned-sub-skill-id' }) for progress display. The workflow must call agent() at least once.",
      "parallel() requires functions, not promises: await parallel(items.map(item => () => agent(...))).",
    ].join(" "),
  }),
  args: Type.Optional(
    Type.Any({ description: "Optional JSON value exposed to the workflow script as global `args`." }),
  ),
  background: Type.Optional(
    Type.Boolean({
      description:
        "Run the workflow in the background. Default: true — the tool returns immediately with a run ID, the turn ends so the user isn't blocked, and the result is delivered back into the conversation when it finishes. Set to false only when you need the result inline in this same turn (the call will block until the workflow completes).",
    }),
  ),
  maxAgents: Type.Optional(
    Type.Number({
      description: "Maximum number of agents allowed in this run. Default: 1000.",
    }),
  ),
  concurrency: Type.Optional(
    Type.Number({
      description:
        "Maximum concurrent agents for this run. Clamped to the runtime maximum. Use when provider/transport stability matters.",
    }),
  ),
  agentRetries: Type.Optional(
    Type.Number({
      description:
        "Retry attempts for recoverable agent failures such as timeout, connection failure, or empty assistant output. Default 0 unless configured.",
    }),
  ),
  agentTimeoutMs: Type.Optional(
    Type.Number({
      description:
        "Timeout per agent in milliseconds. Omit for no hard timeout by default. Set only when the user asks to bound time.",
    }),
  ),
  tokenBudget: Type.Optional(
    Type.Number({
      description:
        "Hard total-token budget for the whole run. Once spent reaches it, further agent() calls fail and the run stops. Omit for no limit. Set it when the user asks to cap spend.",
    }),
  ),
});

export type WorkflowToolInput = {
  script: string;
  args?: unknown;
  background?: boolean;
  maxAgents?: number;
  concurrency?: number;
  agentRetries?: number;
  agentTimeoutMs?: number;
  tokenBudget?: number;
};

export interface WorkflowToolOptions {
  cwd?: string;
  concurrency?: number;
  /** Shared manager so background runs are reachable from the `/workflows` command. */
  manager?: WorkflowManager;
  /** Shared saved-workflow storage. */
  storage?: WorkflowStorage;
  /** Default per-agent timeout for runs created by this tool. null means no hard timeout. */
  defaultAgentTimeoutMs?: number | null;
  /** Default max concurrent agents when no tool-level concurrency is passed. */
  defaultConcurrency?: number;
  /** Default retry attempts after recoverable agent failures. */
  defaultAgentRetries?: number;
}

export function createWorkflowTool(options: WorkflowToolOptions = {}): ToolDefinition<typeof workflowToolSchema, any> {
  const storage = options.storage ?? createWorkflowStorage(options.cwd ?? process.cwd());
  const cwd = options.cwd ?? process.cwd();
  const defaults = resolveWorkflowToolDefaults(options, cwd);
  const manager =
    options.manager ??
    new WorkflowManager({
      cwd: options.cwd,
      concurrency: defaults.concurrency,
      loadSavedWorkflow: (name: string) => storage.load(name)?.script,
      defaultAgentTimeoutMs: defaults.agentTimeoutMs,
      defaultAgentRetries: defaults.agentRetries,
    });

  return defineTool({
    name: "workflow",
    label: "DisCo Workflow",
    description: [
      "Execute a deterministic JavaScript workflow that orchestrates multiple subagents with agent(), parallel(), and pipeline().",
      "Use this for DisCo skill generation, sub-skill extraction, repo-wide analysis, fan-out/fan-in review, or other explicitly decomposable multi-agent work.",
      "script is required raw JavaScript. It must start with export const meta = { name, description, phases? } and must call agent() at least once.",
    ].join(" "),
    promptSnippet:
      "Run a deterministic JavaScript workflow. Required script header: export const meta = { name: 'short_snake_case', description: 'non-empty description', phases: [{ title: 'Phase' }] }.",
    promptGuidelines: [
      "Use workflow for DisCo skill-generation phases that need coordinated parallel subagent extraction and main-agent review, including package/repo sub-skill extraction and Paper2Skills module-skill generation, even if the user's original wording did not literally say workflow.",
      "Use workflow when the user explicitly asks for fan-out, multi-agent orchestration, parallel investigation, or dynamic workflow execution. Do not use it merely because the user's sentence contains workflow/workflows in the ordinary English sense.",
      "For workflow, always pass one raw JavaScript string in the required script parameter; do not include Markdown fences or prose around the script.",
      "For workflow, the script's first statement must be `export const meta = { name: 'short_snake_case', description: 'non-empty human description', phases: [{ title: 'Phase name' }] }`; meta.name and meta.description are required non-empty strings.",
      "For workflow, write plain JavaScript after the meta export. Do not use TypeScript syntax, imports, require(), fs, Date.now(), Math.random(), or new Date().",
      "For workflow, available globals are agent(prompt, opts), parallel(thunks), pipeline(items, ...stages), phase(title), log(message), args, cwd, process.cwd(), and budget. Every workflow must call agent() at least once; do not use workflow only to declare phases or return a static object.",
      "For workflow, prefer the built-in quality helpers when they fit (each is built on agent()/parallel() and returns plain data): verify(item, {reviewers, threshold, lens}) for adversarial fact-checking; judgePanel(attempts, {judges, rubric}) to score N candidates and return the best; loopUntilDry({round, key, consecutiveEmpty}) to keep finding until rounds stop yielding new items; completenessCheck(args, results) as a final 'what's missing' critic.",
      "For workflow, when meta.phases declares more than one phase, call phase('Exact Title') at the start of each phase's work (or set opts.phase on each agent) so every agent groups under the correct phase; never declare a phase you don't switch into — a declared phase with no agents shows as 0/0 and any agent you forgot to move stays in the previous phase.",
      "For workflow, do not set tokenBudget or agentTimeoutMs unless the user explicitly asks to cap spend or time; the defaults are unbounded.",
      "For workflow, to bound spend: pass tokenBudget for a hard run-wide cap; carve a per-phase ceiling with phase('Name', {budget: N}) (that phase throws at its sub-budget without touching the run total — wrap its work in try/catch so later phases proceed); use retry(thunk, {attempts, until}) for bounded retry, and gate(thunk, validator, {attempts}) when a validator's feedback should steer the next attempt. To degrade gracefully, branch on budget.remaining() to skip optional rounds or choose a lighter tier.",
      "For workflow, prefer it for decomposable work: repository inspection, independent research/checks, sub-skill extraction, multi-perspective review, or fan-out/fan-in synthesis. Do not use it for a single quick file read/edit or when ordinary tools are enough.",
      "For workflow, parallel() takes functions, not promises: use `await parallel(items.map(item => () => agent('...', { label: '...' })))`, never `await parallel(items.map(item => agent(...)))`. Results are returned in input order.",
      "For workflow, pipeline(items, ...stages) runs each item through stages sequentially, while different items may run concurrently. Each stage receives (previousValue, originalItem, index).",
      "For workflow, every agent() call should include a unique short label option, 2-5 words, such as { label: 'draft training' }, { label: 'review api' }, or { label: 'source modules' }; for DisCo generation, also pass { subSkill: '<planned-sub-skill-id>' } so the live workflow tree clearly shows which sub-skill each subagent is writing or reviewing.",
      "For DisCo repo-skill generation, the prompt passed to each sub-skill agent must include the full sub-skill brief: canonical id, exact output subtree, frontmatter name requirement, responsibility, boundaries, evidence paths, installed-package facts, required references/scripts, source-script import/adaptation plan, troubleshooting failure modes to cover, one or two difficult synthetic usability case ideas for that sub-skill, exclusions, cross-links, and acceptance rubric. Do not rely on the subSkill option alone as the task description.",
      "For DisCo repo-skill generation, sub-skill drafting/revision agents must write their assigned files directly under the planned generated skill subtree with file tools. Do not design workflows where subagents return full sub-skill Markdown or script bodies in JSON/text for the main agent to write later; the main agent should receive only a concise handoff with file paths, evidence, checks, gaps, and questions.",
      "For DisCo repo-skill generation, keep verification artifacts organized: concrete usability/native-backed/synthetic cases belong under the artifact root's test-cases/ subtree, while integration notes, evals, verification reports, human-review notes, and final handoff documents belong under reports/.",
      "For DisCo repo-skill generation, after sub-skill integration plan one or two integrated difficult cases that exercise multiple sub-skills or root-plus-sub-skill routing; prefer adapting original repo tests/examples from the native candidate map before synthesizing new integrated cases.",
      "For Paper2Skills module-skill generation, use workflow after the main agent has a validated module_plan.json or a concrete module list. The prompt passed to each module agent must include the module id, exact generated skill directory, paper sections/equations/tables to use, optional pre-recovery repo evidence paths, forbidden recovery sources, required scripts/tests, recovery relevance, exclusions, cross-module contracts, and acceptance rubric. Do not rely on the subSkill option alone as the task description.",
      "For Paper2Skills module-skill generation, module drafting/revision agents must write their assigned generated module skill files directly under generated_skills_root with file tools. Do not design workflows where subagents return full SKILL.md or script bodies in JSON/text for the main agent to write later; the main agent should receive only a concise handoff with file paths, evidence, validation commands, recovery implications, gaps, and questions.",
      "For Paper2Skills workflows, the main agent must integrate module boundaries, run create-paper-module-skill validation for every generated module skill, prepare recovery, run the recovery gate, and analyze/refine after subagents finish. Subagent success is not a substitute for the Distiller validators or recovery evidence.",
      "For workflow, use low concurrency and agentRetries for unstable provider/transport fan-out runs; retries apply only to recoverable agent failures and still require explicit null handling after exhaustion.",
      "For workflow, failed agent(), parallel(), or pipeline() branches return null and log the failure unless the workflow is aborted. Check for nulls before synthesizing conclusions.",
      "For workflow, include a final synthesis/assertion agent when combining multiple subagent results; return a compact JSON-serializable value with ok/verdict plus the important outputs.",
      "For workflow, if agent() needs machine-readable output, pass a plain JSON Schema via opts.schema; agent() will return the validated object. Use JSON Schema syntax, not TypeScript or TypeBox constructors. For file-creation tasks, schema output is a handoff manifest after files are written, not a substitute for writing the files.",
      modelRoutingGuideline(),
      agentTypeGuideline(),
      "For workflow, do not assume the parent assistant has repository code context inside subagents; include enough task context and relevant paths in each agent prompt.",
      "For workflow, runs are background by default: the tool returns immediately with a run ID, the turn ends so the user isn't blocked, and the result is delivered back into the conversation when the run finishes. Pass background: false only when you must use the result inline in this same turn (it will block).",
      "For workflow, you may call `await workflow('saved-name', argsObject)` to run a saved workflow inline and use its result; nesting is one level deep only, and the global 16-concurrent / 1000-total caps hold across the nesting.",
    ].filter((g): g is string => typeof g === "string" && g.length > 0),
    parameters: workflowToolSchema,
    prepareArguments(args) {
      return normalizeWorkflowToolArgs(args);
    },
    async execute(_toolCallId, params, signal, onUpdate, ctx) {
      const script = normalizeWorkflowScript(params.script);
      const parsed = parseWorkflowScript(script);

      // checkpoint() reaches the human only on a UI-bearing foreground run; a
      // background run is detached, so checkpoint() falls back to its headless
      // default. Map a checkpoint to ctx.ui.confirm (a yes/no gate) when available.
      const uiCtx = ctx as
        | { hasUI?: boolean; ui?: { confirm?(title: string, message: string): Promise<boolean> } }
        | undefined;
      const uiConfirm = uiCtx?.hasUI ? uiCtx.ui?.confirm : undefined;
      const confirm = uiConfirm
        ? (promptText: string) => uiConfirm.call(uiCtx?.ui, "Workflow checkpoint", promptText)
        : undefined;

      // Background execution is the default: return immediately so the turn ends
      // and the user isn't blocked. The result is delivered back into the
      // conversation when the run finishes (see installResultDelivery). Only an
      // explicit `background: false` blocks for the result inline.
      if (params.background ?? true) {
        const { runId } = manager.startInBackground(script, params.args, {
          maxAgents: params.maxAgents,
          concurrency: params.concurrency,
          agentRetries: params.agentRetries,
          agentTimeoutMs: params.agentTimeoutMs,
          tokenBudget: params.tokenBudget,
        });
        return {
          content: [{ type: "text", text: backgroundStartedText(parsed.meta.name, runId) }],
          details: { runId, background: true },
        };
      }

      // Synchronous execution (blocking) — but routed through the manager so the
      // run shows up live in the /workflows navigator and the task panel while it
      // runs, then stays in history afterwards. We still block on the result and
      // return it inline, so the model gets the full output in the same turn.
      let snapshot: WorkflowSnapshot = createWorkflowSnapshot(parsed.meta);
      const display = createToolUpdateWorkflowDisplay(onUpdate, undefined, {
        key: "workflow",
        streamToolUpdates: true,
        maxAgents: 4,
        showResultPreviews: false,
      });

      let result: WorkflowRunResult;
      try {
        result = await manager.runSync(script, params.args, {
          maxAgents: params.maxAgents,
          concurrency: params.concurrency,
          agentRetries: params.agentRetries,
          agentTimeoutMs: params.agentTimeoutMs,
          tokenBudget: params.tokenBudget,
          confirm,
          externalSignal: signal,
          onProgress(live) {
            snapshot = recomputeWorkflowSnapshot(live);
            display.update(snapshot);
          },
        });
      } catch (error) {
        if (signal?.aborted || (error instanceof WorkflowError && error.code === WorkflowErrorCode.WORKFLOW_ABORTED)) {
          for (const agent of snapshot.agents) {
            if (agent.status === "running") {
              agent.status = "skipped";
              agent.error = "aborted";
            }
          }
          snapshot = recomputeWorkflowSnapshot(snapshot);
          display.complete(snapshot);
          throw new Error("Workflow was aborted");
        }
        throw error;
      }

      if (result.agentCount === 0) {
        throw new Error(
          "workflow scripts must call agent() at least once; this workflow declared phases but did not run any subagents",
        );
      }

      snapshot.result = result.result;
      snapshot.durationMs = result.durationMs;
      snapshot = recomputeWorkflowSnapshot(snapshot);
      display.complete(snapshot);

      // Format token usage (include cost when the provider reports it)
      const tokenInfo = result.tokenUsage
        ? `\n\nToken usage: ${result.tokenUsage.total.toLocaleString()} tokens${
            result.tokenUsage.cost ? ` ($${result.tokenUsage.cost.toFixed(4)})` : ""
          }`
        : "";

      const formattedResult =
        result.result !== undefined ? `\n\`\`\`json\n${JSON.stringify(result.result, null, 2)}\n\`\`\`` : "";

      return {
        content: [
          {
            type: "text",
            text: `Workflow **${result.meta.name}** completed with **${result.agentCount}** agent(s).${tokenInfo}\n\n## Result${formattedResult}`,
          },
        ],
        details: {
          ...snapshot,
          meta: result.meta,
          phases: result.phases,
          logs: result.logs,
          result: result.result,
          durationMs: result.durationMs,
          tokenUsage: result.tokenUsage,
          runId: result.runId,
        },
      };
    },
    renderCall(_args, theme) {
      return new Text(theme.fg("toolTitle", theme.bold("workflow")), 0, 0);
    },
    renderResult(result, { isPartial }, theme) {
      const snapshot = result.details as WorkflowSnapshot | undefined;
      if (snapshot?.name) {
        return new Text(renderWorkflowText(snapshot, !isPartial), 0, 0);
      }
      // Fallback: strip markdown syntax so the TUI doesn't display raw asterisks/hashes.
      // The `content` field is for the LLM (where markdown is preserved), but the TUI
      // renderer (Text component) shows text literally — so we strip markdown here.
      const text = result.content?.[0];
      const raw = text?.type === "text" ? text.text : theme.fg("muted", "workflow");
      const clean = raw
        .replace(/\*\*/g, "")
        .replace(/```[a-z]*\n/g, "")
        .replace(/```/g, "")
        .replace(/^##+\s*/gm, "")
        .trim();
      return new Text(clean || theme.fg("muted", "workflow"), 0, 0);
    },
  });
}

function resolveWorkflowToolDefaults(
  options: WorkflowToolOptions,
  cwd: string,
): { agentTimeoutMs: number | null; concurrency?: number; agentRetries: number } {
  const settings = loadWorkflowSettings({ cwd });
  return {
    agentTimeoutMs:
      options.defaultAgentTimeoutMs !== undefined
        ? options.defaultAgentTimeoutMs
        : (settings.defaultAgentTimeoutMs ?? null),
    concurrency: options.defaultConcurrency ?? options.concurrency ?? settings.defaultConcurrency,
    agentRetries: options.defaultAgentRetries ?? settings.defaultAgentRetries ?? 0,
  };
}

/**
 * The tool result returned when a workflow starts in the background. It both
 * informs the model and tells it to reassure the user: the run continues on its
 * own and the conversation will resume automatically when it finishes, so the
 * user can just wait here (or go do something else).
 */
export function backgroundStartedText(name: string, runId: string): string {
  return [
    `Workflow "${name}" started in the background.`,
    `Run ID: ${runId}`,
    "It keeps running on its own. When it finishes, the result is delivered back",
    "here and the conversation continues automatically — the user does not need to",
    "do anything. Tell the user they can simply wait here for it to finish (it will",
    "resume the conversation by itself), or keep chatting / working on other things",
    "in the meantime; either way the result will come back to this conversation.",
    `They can also track or cancel it with /workflows status ${runId} or /workflows stop ${runId}.`,
  ].join("\n");
}

function normalizeWorkflowToolArgs(args: unknown): WorkflowToolInput {
  if (!args || typeof args !== "object") throw new Error("workflow requires an object argument with a script string");
  const value = args as Record<string, unknown>;
  if (typeof value.script !== "string") throw new Error("workflow requires `script` to be a string");
  return { ...value, script: normalizeWorkflowScript(value.script) } as WorkflowToolInput;
}

function normalizeWorkflowScript(script: string): string {
  let text = script.trim();
  const fence = text.match(/^```(?:js|javascript)?\s*\n([\s\S]*?)\n```$/i);
  if (fence) text = fence[1].trim();
  return text;
}

function _isAbortError(error: unknown): boolean {
  if (!(error instanceof Error)) return false;
  return /\babort(?:ed)?\b/i.test(error.message);
}
