#!/usr/bin/env python3
"""Regex-based eval runner for agent skills. Model-agnostic.

Runs each case's prompt through a harness command N times, applies regex checks
over the transcript, and reports a pass rate per case. There is no default
harness — you pass one so the runner never assumes a specific agent.

Examples:
    python run_evals.py --harness-cmd 'claude -p {prompt}'
    python run_evals.py --harness-cmd 'codex exec --full-auto {prompt}' --trials 5
    python run_evals.py --harness-cmd 'claude -p {prompt}' --case pos-add-auth

The {prompt} token in the command is replaced with each case's prompt.
A check passes when its regex matches the transcript within [min, max] counts
(default min=1). Set "negate": true to require zero matches.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_cases(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def build_cmd(template: str, prompt: str) -> list[str]:
    """Split the harness template and substitute the {prompt} token."""
    tokens = shlex.split(template)
    return [prompt if t == "{prompt}" else t.replace("{prompt}", prompt) for t in tokens]


def run_once(cmd: list[str], timeout: int) -> str:
    """Run the harness in an isolated temp cwd; return stdout+stderr as transcript."""
    with tempfile.TemporaryDirectory(prefix="eval-") as workdir:
        try:
            proc = subprocess.run(
                cmd,
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return (proc.stdout or "") + "\n" + (proc.stderr or "")
        except subprocess.TimeoutExpired:
            return "__TIMEOUT__"


def check_passes(check: dict, transcript: str) -> bool:
    flags = re.IGNORECASE if "i" in check.get("flags", "") else 0
    n = len(re.findall(check["pattern"], transcript, flags))
    if check.get("negate"):
        return n == 0
    if n < check.get("min", 1):
        return False
    hi = check.get("max")
    if hi is not None and n > hi:
        return False
    return True


def eval_trial(case: dict, transcript: str) -> tuple[bool, list[dict]]:
    results = []
    ok = True
    for chk in case.get("checks", []):
        passed = check_passes(chk, transcript)
        ok = ok and passed
        results.append({"description": chk.get("description", chk["pattern"]), "passed": passed})
    return ok, results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--harness-cmd", required=True,
                    help="Harness command with a {prompt} token, e.g. 'claude -p {prompt}'")
    ap.add_argument("--evals", default=str(HERE / "evals.json"), help="Path to evals.json")
    ap.add_argument("--trials", type=int, default=5, help="Trials per case (default 5)")
    ap.add_argument("--min-pass-rate", type=float, default=0.6,
                    help="Min fraction of trials that must pass (default 0.6)")
    ap.add_argument("--timeout", type=int, default=180, help="Per-trial timeout in seconds")
    ap.add_argument("--case", action="append", help="Run only these case id(s)")
    args = ap.parse_args()

    data = load_cases(Path(args.evals))
    cases = data.get("cases", [])
    if args.case:
        cases = [c for c in cases if c["id"] in set(args.case)]
    if not cases:
        print("No cases to run.", file=sys.stderr)
        return 2

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = HERE / "results" / stamp
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = []
    all_passed = True
    print(f"Skill: {data.get('skill', '?')} | harness: {args.harness_cmd} | trials: {args.trials}\n")

    for case in cases:
        if not case.get("checks"):
            print(f"⚠️  {case['id']}: no checks — skipping (should_trigger={case.get('should_trigger')})")
            continue
        cmd_preview = build_cmd(args.harness_cmd, case["prompt"])
        trials = []
        passed_n = 0
        for i in range(args.trials):
            transcript = run_once(cmd_preview, args.timeout)
            ok, chk_results = eval_trial(case, transcript)
            passed_n += int(ok)
            trials.append({"trial": i, "passed": ok, "checks": chk_results,
                           "transcript": transcript[:4000]})
        rate = passed_n / args.trials
        case_ok = rate >= args.min_pass_rate
        all_passed = all_passed and case_ok
        mark = "✅" if case_ok else "❌"
        tag = "trigger" if case.get("should_trigger") else "NO-trigger"
        print(f"{mark} {case['id']} [{tag}] — {passed_n}/{args.trials} trials ({rate:.0%})")
        summary.append({"id": case["id"], "should_trigger": case.get("should_trigger"),
                        "pass_rate": rate, "passed": case_ok, "trials": trials})

    (out_dir / "results.json").write_text(
        json.dumps({"harness": args.harness_cmd, "min_pass_rate": args.min_pass_rate,
                    "cases": summary}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nResults written to {out_dir / 'results.json'}")
    print("PASS" if all_passed else "FAIL")
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
