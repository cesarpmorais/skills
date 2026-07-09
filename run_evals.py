#!/usr/bin/env python3
"""Shared regex/filesystem eval runner for the skills in this repo.

Point it at a skill by name; it runs that skill's cases from
<skill>/evals/evals.json and writes results to <skill>/evals/results/.

    python3 run_evals.py interviews
    python3 run_evals.py interviews --model claude-sonnet-5
    python3 run_evals.py interviews --trials 3 --case pos-add-auth
    python3 run_evals.py interviews --harness-cmd 'codex exec --full-auto {prompt}'

By default it runs the local Claude Code CLI on Claude Haiku (cheap/fast, fine
for trigger evals). Override the model with --model, or swap the whole harness
with --harness-cmd (must contain a {prompt} token). Each case's prompt is
substituted for {prompt}, run once per trial in an isolated empty temp workspace.

A trial ERRORS (not pass/fail) when the harness exits non-zero or times out, so a
broken/unauthenticated harness can never masquerade as passing results.
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
DEFAULT_MODEL = "claude-haiku-4-5-20251001"

PASS, FAIL, ERROR = "pass", "fail", "error"


def load_evals(skill: str) -> tuple[dict, Path]:
    evals_dir = HERE / skill / "evals"
    path = evals_dir / "evals.json"
    if not path.exists():
        sys.exit(f"No evals for '{skill}': expected {path}")
    with path.open(encoding="utf-8") as f:
        return json.load(f), evals_dir


def build_cmd(template: str, prompt: str) -> list[str]:
    """Split the harness template and substitute the {prompt} token."""
    tokens = shlex.split(template)
    return [prompt if t == "{prompt}" else t.replace("{prompt}", prompt) for t in tokens]


def run_once(cmd: list[str], timeout: int) -> tuple[str, list[str], int]:
    """Run the harness in an isolated temp cwd.

    Returns (transcript, files, returncode). returncode is -1 on timeout. files is
    the list of paths the run left in the (initially empty) workspace.
    """
    with tempfile.TemporaryDirectory(prefix="eval-") as workdir:
        wd = Path(workdir)
        try:
            proc = subprocess.run(
                cmd, cwd=workdir, capture_output=True, text=True, timeout=timeout,
            )
            transcript = (proc.stdout or "") + "\n" + (proc.stderr or "")
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            transcript, rc = "__TIMEOUT__", -1
        files = sorted(str(p.relative_to(wd)) for p in wd.rglob("*") if p.is_file())
        return transcript, files, rc


def regex_check(check: dict, transcript: str) -> bool:
    flags = re.IGNORECASE if "i" in check.get("flags", "") else 0
    n = len(re.findall(check["pattern"], transcript, flags))
    if check.get("negate"):
        return n == 0
    hi = check.get("max")
    # An upper-bound check ("max" set) treats zero matches as fine unless the
    # author also sets an explicit floor, so default min to 0 in that case.
    lo = check.get("min", 0 if hi is not None else 1)
    if n < lo:
        return False
    if hi is not None and n > hi:
        return False
    return True


def files_check(check: dict, files: list[str]) -> bool:
    """Assert on artifacts the run produced in the isolated workspace.

    One of:
      - "workspace_clean": true  -> no visible files created (agent only talked)
      - "workspace_clean": false -> at least one visible file created (agent built)
      - "exists": "path/to/file" -> that exact file was created
    Hidden files/dirs (segment starting with ".") are ignored unless
    "include_hidden": true, so harness scratch files don't read as dirtiness.
    """
    if "exists" in check:
        return check["exists"] in files
    if check.get("include_hidden"):
        visible = files
    else:
        visible = [f for f in files if not any(seg.startswith(".") for seg in Path(f).parts)]
    if "workspace_clean" in check:
        clean = len(visible) == 0
        return clean if check["workspace_clean"] else (not clean)
    return True


def check_passes(check: dict, transcript: str, files: list[str]) -> bool:
    if check.get("type") == "files":
        return files_check(check, files)
    return regex_check(check, transcript)


def describe_check(check: dict) -> str:
    return check.get("description") or check.get("pattern") or check.get("type", "check")


def eval_trial(case: dict, transcript: str, files: list[str], rc: int) -> tuple[str, list[dict]]:
    if rc != 0:
        return ERROR, []
    results, ok = [], True
    for chk in case.get("checks", []):
        passed = check_passes(chk, transcript, files)
        ok = ok and passed
        results.append({"description": describe_check(chk), "passed": passed})
    return (PASS if ok else FAIL), results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skill", help="Skill name — runs <skill>/evals/evals.json")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help=f"Model for the default Claude harness (default {DEFAULT_MODEL})")
    ap.add_argument("--harness-cmd", default=None,
                    help="Override the whole harness; must contain a {prompt} token")
    ap.add_argument("--trials", type=int, default=5, help="Trials per case (default 5)")
    ap.add_argument("--min-pass-rate", type=float, default=0.6,
                    help="Min fraction of trials that must pass (default 0.6)")
    ap.add_argument("--timeout", type=int, default=180, help="Per-trial timeout in seconds")
    ap.add_argument("--case", action="append", help="Run only these case id(s)")
    args = ap.parse_args()

    data, evals_dir = load_evals(args.skill)
    harness = args.harness_cmd or (
        f"claude -p --permission-mode acceptEdits --model {args.model} {{prompt}}")

    cases = data.get("cases", [])
    if args.case:
        cases = [c for c in cases if c["id"] in set(args.case)]
    if not cases:
        print("No cases to run.", file=sys.stderr)
        return 2

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = evals_dir / "results" / stamp
    out_dir.mkdir(parents=True, exist_ok=True)

    summary, all_ok, any_error = [], True, False
    print(f"Skill: {args.skill} | harness: {harness} | trials: {args.trials}\n")

    for case in cases:
        if not case.get("checks"):
            print(f"⚠️  {case['id']}: no checks — skipping (should_trigger={case.get('should_trigger')})")
            continue
        cmd = build_cmd(harness, case["prompt"])
        trials, n_pass, n_error = [], 0, 0
        for i in range(args.trials):
            transcript, files, rc = run_once(cmd, args.timeout)
            outcome, chk_results = eval_trial(case, transcript, files, rc)
            n_pass += int(outcome == PASS)
            n_error += int(outcome == ERROR)
            trials.append({"trial": i, "outcome": outcome, "returncode": rc,
                           "checks": chk_results, "files": files, "transcript": transcript[:4000]})

        tag = "trigger" if case.get("should_trigger") else "NO-trigger"
        if n_error:
            any_error = all_ok = False
            print(f"⚠️  {case['id']} [{tag}] — {n_error}/{args.trials} trials ERRORED "
                  f"(harness exited non-zero — broken/unauthenticated?)")
            case_ok = False
            rate = None
        else:
            rate = n_pass / args.trials
            case_ok = rate >= args.min_pass_rate
            all_ok = all_ok and case_ok
            print(f"{'✅' if case_ok else '❌'} {case['id']} [{tag}] — {n_pass}/{args.trials} trials ({rate:.0%})")
        summary.append({"id": case["id"], "should_trigger": case.get("should_trigger"),
                        "pass_rate": rate, "errored": n_error, "passed": case_ok, "trials": trials})

    (out_dir / "results.json").write_text(
        json.dumps({"skill": args.skill, "harness": harness, "min_pass_rate": args.min_pass_rate,
                    "cases": summary}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nResults written to {out_dir / 'results.json'}")
    if any_error:
        print("ERROR — harness failed on one or more cases; results are not valid. Fix the harness (e.g. `claude` login/model) and rerun.")
        return 3
    print("PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
