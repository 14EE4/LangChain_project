_store = {
    "drafts": [],
    "sent": []
}


def get_store():
    return _store


def save_draft(draft: dict) -> None:
    _store["drafts"].append(draft)


def get_draft(draft_id: str) -> dict | None:
    for draft in _store["drafts"]:
        if draft.get("draft_id") == draft_id:
            return draft
    return None


def save_sent(sent_item: dict) -> None:
    _store["sent"].append(sent_item)


def list_drafts(limit: int = 5) -> list[dict]:
    if limit <= 0:
        return []
    return _store["drafts"][-limit:]