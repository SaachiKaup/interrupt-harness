import os
from pathlib import Path

from platform_api import post

ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


def env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value and ENV_FILE.exists():
        value = next((line.partition("=")[2].strip()
                      for line in ENV_FILE.read_text().splitlines()
                      if line.startswith(f"{name}=")), "")
    if not value:
        raise ValueError(f"Set {name} in interrupt-harness/.env")
    return value


DEFAULT_TEAM = env("OPENMATHOS_TEAM")
DEFAULT_PROJECT = env("OPENMATHOS_PROJECT")


def list_models() -> list[dict]:
    catalog = post("model_catalog", {})
    return [
        {"id": model["id"], "name": model["label"], "efforts": model["reasoning"]}
        for model in catalog["models"]
    ]


def create_chat(team: str, project: str, title: str) -> dict:
    return post("chat_create", {"team": team, "project": project, "title": title or None})


def send_prompt(team: str, project: str, session: str, prompt: str,
                model: str, effort: str) -> dict:
    return post("chat_say", {
        "team": team,
        "project": project,
        "session": session,
        "text": prompt,
        "model": model or None,
        "reasoning_effort": effort or None,
    })


def read_summary(team: str, project: str, session: str) -> dict:
    records = []
    after = None
    while True:
        history = post("session_history", {
            "team": team,
            "project": project,
            "session": session,
            "after": after,
            "limit": 200,
        })
        records.extend(history["records"])
        next_after = history.get("next")
        if next_after is None:
            break
        if next_after == after:
            raise ValueError("OpenMathOS history pagination did not advance")
        after = next_after
    return {
        "team": team,
        "project": project,
        "session": session,
        "records": records,
        "record_count": len(records),
    }


def stop_chat(team: str, project: str, session: str) -> dict:
    if not team.strip() or not project.strip() or not session.strip():
        raise ValueError("team, project, and session are required")
    post("chat_stop", {"team": team, "project": project, "session": session})
    return {"team": team, "project": project, "session": session, "status": "stop request accepted"}


def start_chat(prompt: str, team: str = "", project: str = "",
               title: str = "", model: str = "", effort: str = "") -> dict:
    team = team or DEFAULT_TEAM
    project = project or DEFAULT_PROJECT
    if not team.strip() or not project.strip() or not prompt.strip():
        raise ValueError("team, project, and prompt are required")

    chat = create_chat(team, project, title)
    try:
        answer = send_prompt(team, chat["project"], chat["session"], prompt, model, effort)
    except (ValueError, KeyError) as error:
        raise ValueError(
            f"Chat {team}/{chat['project']}/{chat['session']} was created, "
            f"but sending the prompt failed: {error}"
        ) from None

    return {
        "team": team,
        "project": chat["project"],
        "session": chat["session"],
        "title": chat.get("title"),
        "message_id": answer["message_id"],
        "requested_model": model or None,
        "requested_effort": effort or None,
    }


