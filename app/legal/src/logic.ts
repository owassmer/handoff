import type { Node } from "./schema.js";
import { type Truth, and3, not3, or3, unless3 } from "./values.js";

/** The value of a node from its leaves' values. */
export function combine(node: Node, valueOf: (leafId: string) => Truth): Truth {
  switch (node.type) {
    case "condition":
      return valueOf(node.id);
    case "all":
      return and3(node.children.map((c) => combine(c, valueOf)));
    case "any":
      return or3(node.children.map((c) => combine(c, valueOf)));
    case "not":
      return not3(combine(node.child, valueOf));
    case "unless":
      return unless3(combine(node.rule, valueOf), combine(node.exception, valueOf));
  }
}

/**
 * The leaves whose value can still change this node: those no known sibling has already decided
 * (a false child of an all, a true child of an any, a true exception or a false rule of an unless).
 * Each leaf appears once in a tree, so a leaf on such an open path can always turn the result
 * once the other unknowns fall the right way; any other leaf cannot.
 */
export function liveLeaves(node: Node, valueOf: (leafId: string) => Truth, out = new Set<string>()): Set<string> {
  switch (node.type) {
    case "condition":
      out.add(node.id);
      break;
    case "all":
    case "any": {
      const decides = node.type === "any";
      const values = node.children.map((c) => combine(c, valueOf));
      node.children.forEach((c, i) => {
        if (!values.some((v, j) => j !== i && v === decides)) liveLeaves(c, valueOf, out);
      });
      break;
    }
    case "not":
      liveLeaves(node.child, valueOf, out);
      break;
    case "unless":
      if (combine(node.exception, valueOf) !== true) liveLeaves(node.rule, valueOf, out);
      if (combine(node.rule, valueOf) !== false) liveLeaves(node.exception, valueOf, out);
      break;
  }
  return out;
}
