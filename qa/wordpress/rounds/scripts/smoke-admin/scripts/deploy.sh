#!/usr/bin/env bash
# deploy.sh <instance>: copy the worktree theme into the instance, without PROJECT.md and .wp-env.json
set -e
SRC=/home/user/Generation-Maine/.claude/worktrees/wf_d37d6ea6-cba-2/generation-maine
DST="/tmp/claude-0/wptest/inst/$1/core/wp-content/themes/generation-maine"
for f in "$SRC"/* ; do
  b=$(basename "$f")
  [ "$b" = PROJECT.md ] && continue
  cp -a "$f" "$DST/"
done
diff -rq "$SRC" "$DST" || true
