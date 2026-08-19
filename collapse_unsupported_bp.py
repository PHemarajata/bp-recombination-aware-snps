#!/usr/bin/env python3
"""Tier 0.1 -- collapse poorly-supported branches into polytomies.

WHY. The pipeline previously DROPPED any unit whose median ultrafast-bootstrap
support fell below a threshold (A.11v). That threw away 8 units and 225 genomes
because part of each tree was uncertain, when the uncertain part is identifiable
branch by branch. Worse, the threshold was on the wrong scale -- 70 is the
standard-bootstrap convention, while UFBoot's own is 95 -- and coverage moved
5.3x across the range of defensible choices, which means the headline was
reporting a convention rather than a measurement.

The standard remedy for an unsupported branch is not to discard the tree. It is
to COLLAPSE that branch, turning the unresolved node into a polytomy, so the
tree asserts only what the data support and the uncertainty is carried forward
into whatever consumes it.

WHAT IT DOES. Reads an IQ-TREE Newick with `)SUPPORT:LENGTH` at internal nodes,
deletes every internal edge whose support is below the threshold, and reattaches
that node's children to its parent. Branch lengths are PRESERVED ADDITIVELY: a
collapsed child keeps its own length plus the length of the edge removed above
it, so root-to-tip distances are unchanged. Terminal branches are never touched
(a tip has no support value and collapsing one would delete a genome), and the
root is never collapsed.

WHAT IT DOES NOT DO. Collapsing does not rescue a unit whose recombination was
never detected properly -- that is what the r/m screen is for, and it still
applies. This step only stops tree uncertainty from being laundered into a
pass/fail verdict.

Usage:
    python3 collapse_unsupported_bp.py --prefix prod_          # all units
    python3 collapse_unsupported_bp.py --support 95            # UFBoot's own line
    python3 collapse_unsupported_bp.py --selftest
"""

import argparse
import os
import re
import sys

SELF = os.path.dirname(os.path.abspath(__file__))

# Default collapse line. Unlike the withdrawn ACCEPTANCE gate, the choice here is
# low-stakes and reversible: it changes how much resolution a tree asserts, not
# which units exist. 95 is UFBoot's own "supported" convention (Minh 2013) and is
# the honest default; the old 70 is offered for comparison.
DEFAULT_SUPPORT = 95.0


class Node(object):
    __slots__ = ("children", "name", "length", "support", "parent")

    def __init__(self):
        self.children = []
        self.name = ""
        self.length = 0.0
        self.support = None
        self.parent = None

    @property
    def is_leaf(self):
        return not self.children


def parse_newick(s):
    """Minimal Newick parser for IQ-TREE output.

    Internal labels are read as support values when numeric; a non-numeric
    internal label is kept as a name and treated as having no support, so it is
    never collapsed by accident.
    """
    s = s.strip()
    if not s.endswith(";"):
        raise ValueError("Newick must end with ';'")
    i = [0]
    txt = s

    def parse_node():
        node = Node()
        if txt[i[0]] == "(":
            i[0] += 1
            while True:
                child = parse_node()
                child.parent = node
                node.children.append(child)
                if txt[i[0]] == ",":
                    i[0] += 1
                    continue
                if txt[i[0]] == ")":
                    i[0] += 1
                    break
                raise ValueError("bad Newick at %d: %r" % (i[0], txt[i[0]]))
        # label
        start = i[0]
        while i[0] < len(txt) and txt[i[0]] not in "(),:;":
            i[0] += 1
        label = txt[start:i[0]].strip()
        if node.is_leaf:
            node.name = label
        elif label:
            try:
                node.support = float(label)
            except ValueError:
                node.name = label
        # length
        if i[0] < len(txt) and txt[i[0]] == ":":
            i[0] += 1
            start = i[0]
            while i[0] < len(txt) and txt[i[0]] not in "(),;":
                i[0] += 1
            node.length = float(txt[start:i[0]])
        return node

    root = parse_node()
    return root


def write_newick(node):
    def rec(n):
        if n.is_leaf:
            head = n.name
        else:
            head = "(" + ",".join(rec(c) for c in n.children) + ")"
            if n.support is not None:
                head += ("%g" % n.support)
            elif n.name:
                head += n.name
        return head + ":" + ("%.10g" % n.length)

    body = rec(node)
    # strip the root's own length, which Newick conventionally omits
    body = body.rsplit(":", 1)[0]
    return body + ";"


def collapse(root, threshold):
    """Collapse internal edges with support < threshold. Returns (#collapsed).

    Post-order so that a node is considered only after its children are final.
    """
    collapsed = [0]

    def rec(n):
        for c in list(n.children):
            rec(c)
        if n.parent is None or n.is_leaf:
            return
        if n.support is None or n.support >= threshold:
            return
        # Reattach children to the parent, preserving path lengths.
        idx = n.parent.children.index(n)
        for c in n.children:
            c.parent = n.parent
            c.length += n.length
        n.parent.children[idx:idx + 1] = n.children
        collapsed[0] += 1

    rec(root)
    return collapsed[0]


def count_internal(root):
    n = [0]

    def rec(x):
        if not x.is_leaf and x.parent is not None:
            n[0] += 1
        for c in x.children:
            rec(c)

    rec(root)
    return n[0]


def count_tips(root):
    n = [0]

    def rec(x):
        if x.is_leaf:
            n[0] += 1
        for c in x.children:
            rec(c)

    rec(root)
    return n[0]


def process_tree(path, threshold, out_path):
    with open(path) as fh:
        root = parse_newick(fh.read())
    tips_before = count_tips(root)
    internal_before = count_internal(root)
    n = collapse(root, threshold)
    tips_after = count_tips(root)
    if tips_before != tips_after:
        raise AssertionError("collapse changed the tip count in %s (%d -> %d)"
                             % (path, tips_before, tips_after))
    with open(out_path, "w") as fh:
        fh.write(write_newick(root) + "\n")
    return {"tips": tips_after, "internal_before": internal_before,
            "collapsed": n, "internal_after": count_internal(root)}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prefix", default="prod_")
    ap.add_argument("--support", type=float, default=DEFAULT_SUPPORT)
    ap.add_argument("--suffix", default=".collapsed.tre")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    total = {"trees": 0, "collapsed": 0, "internal": 0}
    print("collapsing internal branches with UFBoot < %g\n" % args.support)
    print("%-22s %-26s %5s %9s %9s %7s"
          % ("unit", "arm", "tips", "internal", "collapsed", "%"))
    for d in sorted(os.listdir(SELF)):
        if not d.startswith(args.prefix):
            continue
        armdir = os.path.join(SELF, d, "arms")
        if not os.path.isdir(armdir):
            continue
        for arm in sorted(os.listdir(armdir)):
            tf = os.path.join(armdir, arm, "tree.treefile")
            if not os.path.exists(tf):
                continue
            try:
                r = process_tree(tf, args.support, tf + args.suffix)
            except (ValueError, AssertionError) as e:
                print("%-22s %-26s  ERROR %s" % (d[len(args.prefix):], arm, e))
                continue
            total["trees"] += 1
            total["collapsed"] += r["collapsed"]
            total["internal"] += r["internal_before"]
            print("%-22s %-26s %5d %9d %9d %6.0f%%"
                  % (d[len(args.prefix):], arm, r["tips"], r["internal_before"],
                     r["collapsed"],
                     100.0 * r["collapsed"] / r["internal_before"]
                     if r["internal_before"] else 0.0))
    print("\n%d trees; %d of %d internal branches collapsed (%.0f%%)"
          % (total["trees"], total["collapsed"], total["internal"],
             100.0 * total["collapsed"] / total["internal"]
             if total["internal"] else 0.0))
    print("written alongside each tree.treefile with suffix %s" % args.suffix)
    print("\nNo unit was dropped. Every genome that passed detection is still "
          "represented;\nwhat changed is that the trees no longer assert "
          "relationships the data do not support.")
    return 0


def selftest():
    fails = []

    def chk(desc, got, want, tol=1e-9):
        ok = (abs(got - want) <= tol) if isinstance(want, float) else (got == want)
        print("%-58s %s" % (desc, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
        if not ok:
            fails.append(desc)

    # round trip
    t = "((A:0.1,B:0.2)95:0.3,(C:0.4,D:0.5)40:0.6):0.0;"
    r = parse_newick(t)
    chk("tips parsed", count_tips(r), 4)
    chk("internal parsed", count_internal(r), 2)

    # Collapsing at 90 removes the 40 node only.
    r = parse_newick(t)
    chk("one branch collapsed at 90", collapse(r, 90.0), 1)
    chk("tips preserved", count_tips(r), 4)
    chk("internal reduced", count_internal(r), 1)

    # Path lengths must be preserved additively: C was at 0.4 under an edge of
    # 0.6, so after collapsing it must sit at 1.0 from the root.
    def depth(node, name):
        if node.is_leaf:
            return node.length if node.name == name else None
        for c in node.children:
            d = depth(c, name)
            if d is not None:
                return d + node.length
        return None

    before = depth(parse_newick(t), "C")
    r = parse_newick(t)
    collapse(r, 90.0)
    chk("root-to-tip distance unchanged", depth(r, "C"), before, 1e-12)
    chk("... and it is the expected value", depth(r, "C"), 1.0, 1e-12)

    # A well-supported tree is untouched.
    r = parse_newick(t)
    chk("nothing collapsed at 30", collapse(r, 30.0), 0)

    # Collapsing everything yields a star, and STILL keeps every tip.
    r = parse_newick(t)
    collapse(r, 100.0)
    chk("star tree keeps all tips", count_tips(r), 4)
    chk("star tree has no internal branches", count_internal(r), 0)

    # Terminal branches must never be collapsed even at an absurd threshold --
    # a tip carries no support and dropping one would delete a genome.
    r = parse_newick("((A:0.1,B:0.2)10:0.3,C:0.4):0.0;")
    collapse(r, 999.0)
    chk("tips survive an absurd threshold", count_tips(r), 3)

    # Support exactly at the threshold is KEPT (>= is the contract).
    r = parse_newick("((A:0.1,B:0.2)70:0.3,C:0.4):0.0;")
    chk("support == threshold is kept", collapse(r, 70.0), 0)

    # A non-numeric internal label must not be read as support 0 and collapsed.
    r = parse_newick("((A:0.1,B:0.2)nodeX:0.3,C:0.4):0.0;")
    chk("non-numeric label is not collapsed", collapse(r, 95.0), 0)

    # Serialisation round-trips through the parser.
    r = parse_newick(t)
    collapse(r, 90.0)
    again = parse_newick(write_newick(r))
    chk("written tree re-parses", count_tips(again), 4)
    chk("written tree keeps topology", count_internal(again), 1)

    # Nested unsupported branches collapse into a single polytomy.
    nested = "(((A:0.1,B:0.1)10:0.1,C:0.1)20:0.1,D:0.1):0.0;"
    r = parse_newick(nested)
    chk("nested unsupported both collapse", collapse(r, 95.0), 2)
    chk("nested collapse gives a star", count_internal(r), 0)
    chk("nested collapse keeps tips", count_tips(r), 4)

    print("\n%d test(s) failed" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
