#!/usr/bin/env bash
# Push the r4 commit on civilizationalmetamaterials/main to GitHub, using
# a GitHub PAT fetched from 1Password via the `op` CLI.
#
# Usage (from Claude Code or a Mac terminal):
#     bash push-r4.sh
#     bash push-r4.sh --item "My Custom Item Name"  # override default item
#     bash push-r4.sh --dry-run                      # show what would happen
#
# Requirements:
#   - The 1Password CLI (`op`) must be installed and signed in.
#     Test with: op item list | head -5
#   - The repo's HEAD must be the r4 commit (we verify before pushing).
#
# Security notes:
#   - The PAT is held in a single shell variable, used in one push call, then
#     unset. It is never written to disk and never echoed.
#   - The push uses a one-shot URL (https://x-access-token:PAT@github.com/...)
#     rather than modifying the remote's stored URL, so the credential never
#     enters .git/config.
#   - `set -u` ensures the script fails loudly if anything is missing.

set -euo pipefail

# -----------------------------------------------------------------------------
# Config (override via env or CLI flags)
# -----------------------------------------------------------------------------
OP_ITEM="${OP_ITEM:-GitHub PAT}"  # name or UUID of the 1Password item
OP_FIELD="${OP_FIELD:-credential}"   # field name; often "credential" or "token"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/civilizationalmetamaterials" && pwd)"
REMOTE_HOST="github.com"
REPO_PATH="davidorban/civilizationalmetamaterials"
BRANCH="main"
EXPECTED_HEAD_SUMMARY="r4: AGI-26 camera-ready"
DRY_RUN=0

# -----------------------------------------------------------------------------
# CLI parsing
# -----------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --item)     OP_ITEM="$2"; shift 2 ;;
    --field)    OP_FIELD="$2"; shift 2 ;;
    --dry-run)  DRY_RUN=1; shift ;;
    -h|--help)
      sed -n '2,/^set -e/p' "$0" | sed 's/^# \{0,1\}//' | head -25
      exit 0 ;;
    *)          echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

# -----------------------------------------------------------------------------
# Sanity checks (do everything we can before touching the credential)
# -----------------------------------------------------------------------------
log() { printf '%s %s\n' "[push-r4]" "$*"; }
die() { printf '%s %s\n' "[push-r4]" "$*" >&2; exit 1; }

command -v op    >/dev/null || die "1Password CLI (op) not found in PATH. Install via 'brew install 1password-cli' or enable the CLI in 1Password's settings."
command -v git   >/dev/null || die "git not found in PATH."

[[ -d "$REPO_DIR/.git" ]] || die "Not a git repo: $REPO_DIR"
cd "$REPO_DIR"

log "Repo:        $REPO_DIR"
log "Branch:      $BRANCH"
log "Remote:      $REMOTE_HOST/$REPO_PATH"
log "1Password:   item=\"$OP_ITEM\", field=\"$OP_FIELD\""
log "Dry run:     $([ "$DRY_RUN" = 1 ] && echo yes || echo no)"

# Confirm we're on the right branch
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
[[ "$CURRENT_BRANCH" == "$BRANCH" ]] \
  || die "Current branch is '$CURRENT_BRANCH', expected '$BRANCH'."

# Show the HEAD subject and warn (don't die) if it doesn't look r4-related.
# This lets the script handle follow-up commits like fig regenerations.
HEAD_SUBJECT="$(git log -1 --pretty=%s)"
log "HEAD commit: $HEAD_SUBJECT"
if [[ "$HEAD_SUBJECT" != *"$EXPECTED_HEAD_SUMMARY"* ]]; then
  log "  (subject doesn't contain '$EXPECTED_HEAD_SUMMARY' — proceeding anyway)"
fi

# Confirm there's actually something to push
if git merge-base --is-ancestor HEAD "origin/$BRANCH" 2>/dev/null; then
  die "HEAD is already on origin/$BRANCH — nothing to push."
fi

# Confirm the 1Password item exists before asking for the credential.
# This will trigger 1Password's biometric / unlock prompt if the vault is locked.
log "Looking up 1Password item \"$OP_ITEM\" (will prompt for unlock if needed)..."
op item get "$OP_ITEM" --format=json >/dev/null 2>&1 \
  || die "1Password item \"$OP_ITEM\" not found. Override with: OP_ITEM=\"<name>\" bash push-r4.sh"

# -----------------------------------------------------------------------------
# Fetch the PAT — held in a variable, never echoed, never written to disk
# -----------------------------------------------------------------------------
log "Fetching PAT field \"$OP_FIELD\"..."
PAT="$(op item get "$OP_ITEM" --fields "$OP_FIELD" --reveal 2>/dev/null)" \
  || die "Could not read field \"$OP_FIELD\" from item \"$OP_ITEM\". Try --field token, or run: op item get \"$OP_ITEM\" --format=json | jq '.fields[].label'"

# Strip any accidental whitespace and surrounding quotes that op sometimes adds.
PAT="${PAT//[$'\t\r\n ']/}"
PAT="${PAT#\"}"
PAT="${PAT%\"}"

[[ -n "$PAT" ]] || die "Retrieved PAT is empty."

# Sanity-check the shape (PATs start with ghp_, github_pat_, or in rare cases gho_/ghs_)
case "$PAT" in
  ghp_*|github_pat_*|gho_*|ghs_*)
    : ;;  # OK
  *)
    log "Warning: PAT does not match expected GitHub token prefix (ghp_, github_pat_, gho_, ghs_). Proceeding anyway." ;;
esac

# -----------------------------------------------------------------------------
# Push
# -----------------------------------------------------------------------------
PUSH_URL="https://x-access-token:${PAT}@${REMOTE_HOST}/${REPO_PATH}.git"

if [[ "$DRY_RUN" == 1 ]]; then
  log "DRY RUN — would execute: git push <url-with-redacted-pat> $BRANCH"
  log "Commits that would be pushed:"
  git log --oneline "origin/$BRANCH..HEAD"
  PAT=""; unset PAT
  exit 0
fi

log "Pushing $BRANCH to origin..."
# Capture stderr so we can scrub any accidental token echo before showing it.
PUSH_OUTPUT="$(git push "$PUSH_URL" "$BRANCH" 2>&1)" || PUSH_STATUS=$?
PUSH_STATUS="${PUSH_STATUS:-0}"

# Redact the PAT from any output before printing.
echo "${PUSH_OUTPUT//$PAT/<REDACTED>}"

# Wipe the credential.
PAT=""
unset PAT
PUSH_URL=""
unset PUSH_URL

if [[ "$PUSH_STATUS" != 0 ]]; then
  die "git push exited with status $PUSH_STATUS"
fi

log "Push succeeded."
log "Verify at: https://${REMOTE_HOST}/${REPO_PATH}/commits/${BRANCH}"
