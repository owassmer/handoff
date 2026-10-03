/**
 * Handoff's legal engine: the compiled legal trees and their evaluator (DESIGN.md §5.3).
 *
 * - loadJurisdiction(dir) reads, validates and cross-checks a jurisdiction's trees.
 * - evaluate(tree, facts, options) runs one tree against a case's facts, three-valued.
 */
export { type CompiledTree, TreeValidationError, compileTree, compiled, formulasOf, requiredFacts, walkNodes } from "./compile.js";
export {
  type Answer,
  type AnswerContext,
  type AnswerProvider,
  type BranchResult,
  type ContestedResult,
  type DecisionRecord,
  type Decisions,
  type Diagnostic,
  type EffectResult,
  type EvaluateOptions,
  type EvaluationResult,
  type ExposureResult,
  type Facts,
  type FormulaOutcome,
  type InvestigationItem,
  type LeafBasis,
  type LeafTrace,
  type NodeTrace,
  type Settlement,
  evaluate,
} from "./evaluate.js";
export { BUILTINS, type FormulaAnalysis, analyzeFormula } from "./formula/analyze.js";
export { type FormulaRun, type FormulaScope, FormulaError, runFormula } from "./formula/evaluate.js";
export { type Expr, FormulaSyntaxError, parseFormula } from "./formula/parse.js";
export { Jurisdiction, type LoadOptions, buildJurisdiction, inForce, loadJurisdiction } from "./loader.js";
export { combine, liveLeaves } from "./logic.js";
export type { Branch, Condition, Contested, Effect, LeafKind, Node, Parameter, Question, Source, Tree } from "./schema.js";
export { TreeSchema } from "./schema.js";
export { BUSINESS_TIME_ZONE, addDays, businessDate, daysBetween, daysInMonth } from "./time.js";
export { Duration, type Truth, UNKNOWN, and3, not3, or3, unless3 } from "./values.js";
