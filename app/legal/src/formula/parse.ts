/**
 * The formula language of the trees: a small expression grammar, parsed by hand (no eval).
 *
 *   expr        := or ("if" or "else" expr)?
 *   or          := and ("or" and)*
 *   and         := not ("and" not)*
 *   not         := "not" not | comparison
 *   comparison  := additive (("==" | "!=" | "<" | "<=" | ">" | ">=" | "in" | "not" "in") additive)?
 *   additive    := term (("+" | "-") term)*
 *   term        := unary (("*" | "/") unary)*
 *   unary       := "-" unary | postfix
 *   postfix     := primary ("." name | "(" args? ")")*
 *   primary     := number | string | "true" | "false" | "null" | name | "(" expr ")" | "[" args? "]"
 *
 * Comparisons do not chain. A call on a bare name is a built-in function; a call on a path
 * (ledger.rentDueThrough(...)) is a method of a fact object supplied by the case binding.
 */

export type CompareOp = "==" | "!=" | "<" | "<=" | ">" | ">=" | "in" | "not in";
export type ArithOp = "+" | "-" | "*" | "/";

export type Expr =
  | { kind: "number"; value: number; pos: number }
  | { kind: "string"; value: string; pos: number }
  | { kind: "boolean"; value: boolean; pos: number }
  | { kind: "null"; pos: number }
  | { kind: "name"; name: string; pos: number }
  | { kind: "member"; object: Expr; property: string; pos: number }
  | { kind: "call"; callee: Expr; args: Expr[]; pos: number }
  | { kind: "list"; items: Expr[]; pos: number }
  | { kind: "negate"; arg: Expr; pos: number }
  | { kind: "not"; arg: Expr; pos: number }
  | { kind: "arith"; op: ArithOp; left: Expr; right: Expr; pos: number }
  | { kind: "compare"; op: CompareOp; left: Expr; right: Expr; pos: number }
  | { kind: "logical"; op: "and" | "or"; left: Expr; right: Expr; pos: number }
  | { kind: "conditional"; test: Expr; then: Expr; otherwise: Expr; pos: number };

export class FormulaSyntaxError extends Error {
  constructor(
    readonly formula: string,
    readonly pos: number,
    message: string,
  ) {
    super(`${message} at ${pos} in ${JSON.stringify(formula)}`);
  }
}

type Token =
  | { type: "number"; value: number; pos: number }
  | { type: "string"; value: string; pos: number }
  | { type: "name"; value: string; pos: number }
  | { type: "symbol"; value: string; pos: number }
  | { type: "end"; value: ""; pos: number };

const KEYWORDS = new Set(["and", "or", "not", "in", "true", "false", "null", "if", "else"]);
const SYMBOLS = ["==", "!=", "<=", ">=", "<", ">", "+", "-", "*", "/", "(", ")", "[", "]", ",", "."];

function tokenize(src: string): Token[] {
  const out: Token[] = [];
  let i = 0;
  while (i < src.length) {
    const c = src[i]!;
    if (/\s/.test(c)) {
      i++;
      continue;
    }
    const start = i;
    if (/[0-9]/.test(c)) {
      const m = /^[0-9]+(\.[0-9]+)?/.exec(src.slice(i))!;
      out.push({ type: "number", value: Number(m[0]), pos: start });
      i += m[0].length;
      if (i < src.length && /[A-Za-z_]/.test(src[i]!)) throw new FormulaSyntaxError(src, i, "unexpected letter after number");
      continue;
    }
    if (c === '"' || c === "'") {
      let s = "";
      i++;
      while (i < src.length && src[i] !== c) {
        if (src[i] === "\\" && i + 1 < src.length) i++;
        s += src[i];
        i++;
      }
      if (i >= src.length) throw new FormulaSyntaxError(src, start, "unterminated string");
      i++;
      out.push({ type: "string", value: s, pos: start });
      continue;
    }
    if (/[A-Za-z_]/.test(c)) {
      const m = /^[A-Za-z_][A-Za-z0-9_]*/.exec(src.slice(i))!;
      out.push({ type: "name", value: m[0], pos: start });
      i += m[0].length;
      continue;
    }
    const sym = SYMBOLS.find((s) => src.startsWith(s, i));
    if (!sym) throw new FormulaSyntaxError(src, i, `unexpected character ${JSON.stringify(c)}`);
    out.push({ type: "symbol", value: sym, pos: start });
    i += sym.length;
  }
  out.push({ type: "end", value: "", pos: src.length });
  return out;
}

class Parser {
  private i = 0;
  constructor(
    private readonly src: string,
    private readonly tokens: Token[],
  ) {}

  private peek(offset = 0): Token {
    return this.tokens[Math.min(this.i + offset, this.tokens.length - 1)]!;
  }
  private next(): Token {
    const t = this.peek();
    if (t.type !== "end") this.i++;
    return t;
  }
  private isSymbol(v: string, offset = 0): boolean {
    const t = this.peek(offset);
    return t.type === "symbol" && t.value === v;
  }
  private isKeyword(v: string, offset = 0): boolean {
    const t = this.peek(offset);
    return t.type === "name" && t.value === v;
  }
  private fail(message: string, pos = this.peek().pos): never {
    throw new FormulaSyntaxError(this.src, pos, message);
  }
  private expectSymbol(v: string): Token {
    if (!this.isSymbol(v)) this.fail(`expected "${v}"`);
    return this.next();
  }

  parse(): Expr {
    const e = this.expr();
    if (this.peek().type !== "end") this.fail("unexpected input");
    return e;
  }

  private expr(): Expr {
    const value = this.or();
    if (this.isKeyword("if")) {
      const pos = this.next().pos;
      const test = this.or();
      if (!this.isKeyword("else")) this.fail('expected "else"');
      this.next();
      const otherwise = this.expr();
      return { kind: "conditional", test, then: value, otherwise, pos };
    }
    return value;
  }

  private or(): Expr {
    let left = this.and();
    while (this.isKeyword("or")) {
      const pos = this.next().pos;
      left = { kind: "logical", op: "or", left, right: this.and(), pos };
    }
    return left;
  }

  private and(): Expr {
    let left = this.not();
    while (this.isKeyword("and")) {
      const pos = this.next().pos;
      left = { kind: "logical", op: "and", left, right: this.not(), pos };
    }
    return left;
  }

  private not(): Expr {
    if (this.isKeyword("not") && !this.isKeyword("in", 1)) {
      const pos = this.next().pos;
      return { kind: "not", arg: this.not(), pos };
    }
    return this.comparison();
  }

  private compareOp(): CompareOp | undefined {
    const t = this.peek();
    if (t.type === "symbol" && ["==", "!=", "<", "<=", ">", ">="].includes(t.value)) return t.value as CompareOp;
    if (this.isKeyword("in")) return "in";
    if (this.isKeyword("not") && this.isKeyword("in", 1)) return "not in";
    return undefined;
  }

  private comparison(): Expr {
    const left = this.additive();
    const op = this.compareOp();
    if (!op) return left;
    const pos = this.next().pos;
    if (op === "not in") this.next();
    const right = this.additive();
    if (this.compareOp()) this.fail("comparisons do not chain; use and");
    return { kind: "compare", op, left, right, pos };
  }

  private additive(): Expr {
    let left = this.term();
    while (this.isSymbol("+") || this.isSymbol("-")) {
      const t = this.next();
      left = { kind: "arith", op: t.value as ArithOp, left, right: this.term(), pos: t.pos };
    }
    return left;
  }

  private term(): Expr {
    let left = this.unary();
    while (this.isSymbol("*") || this.isSymbol("/")) {
      const t = this.next();
      left = { kind: "arith", op: t.value as ArithOp, left, right: this.unary(), pos: t.pos };
    }
    return left;
  }

  private unary(): Expr {
    if (this.isSymbol("-")) {
      const pos = this.next().pos;
      return { kind: "negate", arg: this.unary(), pos };
    }
    return this.postfix();
  }

  private postfix(): Expr {
    let e = this.primary();
    for (;;) {
      if (this.isSymbol(".")) {
        this.next();
        const t = this.next();
        if (t.type !== "name") this.fail("expected a name after '.'", t.pos);
        e = { kind: "member", object: e, property: t.value, pos: t.pos };
      } else if (this.isSymbol("(")) {
        const pos = this.next().pos;
        if (e.kind !== "name" && e.kind !== "member") this.fail("only a function or a fact method can be called", pos);
        e = { kind: "call", callee: e, args: this.args(")"), pos };
      } else {
        return e;
      }
    }
  }

  private args(close: string): Expr[] {
    const out: Expr[] = [];
    if (this.isSymbol(close)) {
      this.next();
      return out;
    }
    for (;;) {
      out.push(this.expr());
      if (this.isSymbol(",")) {
        this.next();
        continue;
      }
      this.expectSymbol(close);
      return out;
    }
  }

  private primary(): Expr {
    const t = this.next();
    switch (t.type) {
      case "number":
        return { kind: "number", value: t.value, pos: t.pos };
      case "string":
        return { kind: "string", value: t.value, pos: t.pos };
      case "name":
        if (t.value === "true" || t.value === "false") return { kind: "boolean", value: t.value === "true", pos: t.pos };
        if (t.value === "null") return { kind: "null", pos: t.pos };
        if (KEYWORDS.has(t.value)) this.fail(`unexpected "${t.value}"`, t.pos);
        return { kind: "name", name: t.value, pos: t.pos };
      case "symbol":
        if (t.value === "(") {
          const e = this.expr();
          this.expectSymbol(")");
          return e;
        }
        if (t.value === "[") return { kind: "list", items: this.args("]"), pos: t.pos };
        return this.fail(`unexpected "${t.value}"`, t.pos);
      case "end":
        return this.fail("unexpected end of formula", t.pos);
    }
  }
}

export function parseFormula(src: string): Expr {
  return new Parser(src, tokenize(src)).parse();
}

/** The dotted path of a name or member chain (ledger.payments), or undefined for anything else. */
export function pathOf(e: Expr): string | undefined {
  if (e.kind === "name") return e.name;
  if (e.kind === "member") {
    const base = pathOf(e.object);
    return base === undefined ? undefined : `${base}.${e.property}`;
  }
  if (e.kind === "call") {
    const base = pathOf(e.callee);
    return base === undefined ? undefined : `${base}(…)`;
  }
  return undefined;
}
