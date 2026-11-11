#!/usr/bin/env python3
"""非公開リポジトリ znenso-mentoring のカードから、公開ページ用の data.json を作る。

載せるのは：課題名・説明の1行目・チェックリスト・状態・締め切り・今岡のコメント。
井澤さんたちのコメントや本文の細部は載せない（公開ページのため）。
"""
import json, re, subprocess, datetime, pathlib

OWNER = "wimaoka51-blip"
REPO = f"{OWNER}/znenso-mentoring"
PROJECT = "1"
OUT = pathlib.Path(__file__).with_name("data.json")


def gh(*args):
    return json.loads(subprocess.check_output(["gh", *args], text=True))


def parse_body(body):
    steps, bullets, desc = [], [], []
    for line in (body or "").splitlines():
        s = line.strip()
        m = re.match(r"- \[( |x|X)\] (.+)", s)
        if m:
            steps.append([m.group(2).strip(), m.group(1).lower() == "x"])
        elif s.startswith("- "):
            bullets.append(s[2:].strip())
        elif s:
            desc.append(re.sub(r"\*\*(.+?)\*\*", r"\1", s))
    return steps, bullets, desc


issues = gh("issue", "list", "-R", REPO, "--state", "all", "--limit", "200",
            "--json", "number,title,state,labels,milestone,body,closedAt")
milestones = gh("api", f"repos/{REPO}/milestones?state=all")
items = gh("project", "item-list", PROJECT, "--owner", OWNER, "--format", "json", "--limit", "200")["items"]
status = {it["content"].get("number"): it.get("status") for it in items if it.get("content")}
comments = gh("api", f"repos/{REPO}/issues/comments?per_page=100")

cards = []
for i in issues:
    steps, bullets, desc = parse_body(i["body"])
    labels = [l["name"] for l in i["labels"]]
    st = status.get(i["number"]) or ("完了" if i["state"] == "CLOSED" else "未着手")
    if i["state"] == "CLOSED":
        st = "完了"
    cards.append({
        "number": i["number"],
        "title": i["title"],
        "labels": labels,
        "milestone": (i.get("milestone") or {}).get("title"),
        "status": st,
        "steps": steps,
        "bullets": bullets,
        "desc": desc[0] if desc else "",
        "closedAt": i.get("closedAt"),
    })

ms = [{
    "title": m["title"],
    "description": m.get("description") or "",
    "due": m.get("due_on"),
    "open": m["open_issues"],
    "closed": m["closed_issues"],
} for m in milestones]

title_of = {c["number"]: c["title"] for c in cards}
log = []
for c in comments:
    if c["user"]["login"] != OWNER:
        continue
    n = int(c["issue_url"].rsplit("/", 1)[1])
    first = c["body"].strip().splitlines()[0] if c["body"].strip() else ""
    log.append({"at": c["created_at"], "card": title_of.get(n, ""), "text": first})
for c in cards:
    if c["closedAt"] and "課題" in c["labels"]:
        log.append({"at": c["closedAt"], "card": c["title"], "text": "完了"})
log.sort(key=lambda x: x["at"], reverse=True)

OUT.write_text(json.dumps({
    "updated": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec="minutes"),
    "milestones": ms,
    "cards": cards,
    "log": log[:30],
}, ensure_ascii=False, indent=1))
print(f"data.json: cards {len(cards)}, milestones {len(ms)}, log {len(log[:30])}")
