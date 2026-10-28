---
description: Review the diff, commit the project changes, then rebase onto origin/main
---

1. Run `git status` and `git diff HEAD` to review the changes. Flag anything that looks unintended (secrets, build artifacts, unrelated files) before continuing.
2. Stage the project changes with `git add`, then commit them with the message: $ARGUMENTS
3. Run `git pull --rebase origin main`.

If the rebase hits conflicts, stop and report them instead of resolving them.
