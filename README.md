# Interrupt Harness

This directory is the home for the OpenMathOS interrupt harness: its plans, implementation, tests, and teammate-facing setup material. Keep new harness work here rather than adding it to the Danus package.

The first stage is an in-host conversational control for Codex and Antigravity. Mathematicians ask their host agent to start, inspect, or stop an OpenMathOS chat. A visible, independent Stop control remains the later stage for cases where the host is busy or unresponsive.

## Local setup

Create `interrupt-harness/.env` with your OpenMathOS platform key, team ID, and project ID:

```env
OPENMATHOS_PLATFORM_KEY=your-platform-key
OPENMATHOS_TEAM=your-team-id
OPENMATHOS_PROJECT=your-project-id
```

The `.env` file is ignored by Git. Each teammate should use the IDs for their own team and project. Restart Codex after changing the file so its MCP server reloads the settings.

Use the `continue` tool with an existing session ID and a new prompt to send another turn without creating a new chat. It does not reject a session because of an earlier stop request.

Start with [the current end-to-end plan](plans/current.md). [Previous drafts](plans/previous-drafts/README.md) preserve the earlier CLI, tmux, visible UI, in-host, and monitoring proposals. Earlier investigation remains in [the OpenMathOS handoff](../open-math-experiment/docs/conversation-handoff.md); it is a source note, not the current implementation location.
