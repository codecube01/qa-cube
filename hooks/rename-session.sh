#!/usr/bin/env bash
# A hook that renames the session after the task number taken from /qa's arguments. Two launch
# paths mean two events:
#  - UserPromptSubmit (no matcher): the user typed «/qa …» or «/qa-cube:qa …» as a slash
#    command — the skill is injected into the context without invoking the Skill tool, so
#    PreToolUse does not fire here and we catch the prompt directly;
#  - PreToolUse (matcher: Skill): Claude invoked the qa skill through the tool (e.g. from the
#    phrase «test task X»).
set -euo pipefail

# The hook runs on EVERY prompt (UserPromptSubmit has no matcher) and the «is this /qa?»
# test below is made with jq — so without jq the script dies at the first parse, before the
# early exit, and every ordinary message in every project earns a «jq: command not found».
# jq is stock on recent macOS but is missing from older ones and from slim linux images, so
# its absence turns into a silent no-op: no session rename, nothing else affected.
command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)
event=$(jq -r '.hook_event_name // empty' <<<"$input")

if [ "$event" = "UserPromptSubmit" ]; then
  prompt=$(jq -r '.prompt // empty' <<<"$input")
  case "$prompt" in
    /qa|/qa\ *) args="${prompt#/qa}" ;;
    /qa-cube:qa|/qa-cube:qa\ *) args="${prompt#/qa-cube:qa}" ;;
    *) exit 0 ;;
  esac
else
  skill=$(jq -r '.tool_input.skill // empty' <<<"$input")
  case "$skill" in qa|qa-cube:qa) ;; *) exit 0 ;; esac
  args=$(jq -r '.tool_input.args // empty' <<<"$input")
fi

# Priority: a link to a work item / issue → the #<num> form → the last number.
# stageN is dropped in advance («ACME-449 on stage3» ≠ task 3); the last number rather than the
# first, because in a URL like .../group/team/project/-/work_items/676 the first number is the «2» in the group name.
args_clean=$(sed -E 's/stage[0-9]+//g' <<<"$args")
num=$(grep -oE '(work_items|issues)/[0-9]+' <<<"$args_clean" | grep -oE '[0-9]+' | head -1 || true)
[ -n "$num" ] || num=$(grep -oE '#[0-9]+' <<<"$args_clean" | head -1 | tr -d '#' || true)
[ -n "$num" ] || num=$(grep -oE '[0-9]+' <<<"$args_clean" | tail -1 || true)
[ -n "$num" ] || exit 0

sid=$(jq -r '.session_id // empty' <<<"$input")
transcript=$(jq -r '.transcript_path // empty' <<<"$input")
[ -n "$transcript" ] || exit 0

line=$(printf '{"type":"custom-title","customTitle":"%s","sessionId":"%s"}' "$num" "$sid")
if [ -f "$transcript" ]; then
  printf '%s\n' "$line" >> "$transcript"
else
  # /qa is the first prompt of a fresh session: the transcript file does not exist yet, it
  # appears only after this hook finishes. Wait for it in the background and append the title
  # once it shows up.
  nohup bash -c '
    for _ in $(seq 1 120); do
      [ -f "$1" ] && { printf "%s\n" "$2" >> "$1"; exit 0; }
      sleep 1
    done
  ' _ "$transcript" "$line" >/dev/null 2>&1 &
fi

echo "{\"systemMessage\": \"Session renamed: $num\"}"
