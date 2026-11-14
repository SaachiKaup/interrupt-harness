# Interrupt harness workspace

Keep new interrupt-harness plans, code, tests, and teammate-facing documentation in this directory. Use `open-math-experiment` and `Danus` as references; do not implement this harness inside either project unless the user explicitly changes that direction.

Read `plans/current.md` before working on the first stage. The user chose an in-host conversational control with approximately one-minute progress reports. Preserve and explain its limitation: it cannot stop work while Codex or Antigravity is unable to process a new request. `plans/previous-drafts/` holds historical proposals, including the later independent-control UI. Support macOS and Windows.

## Using the OpenMathOS tools

- For a mathematical investigation in this project, send the task to OpenMathOS with `interrupt-harness.start`; do not solve it in Codex unless the user asks for a local solution.
- For status requests, use `interrupt-harness.progress` with the session ID and summarize only its published records. Do not run Lean, compile, inspect local math libraries, or reproduce the remote work.
- Do not start a new investigation or stop one unless the user asks. Do not invent updates or present unverified claims as proved.
- Use the default Caltech Mathathon SPA team and project unless the user names another target.
