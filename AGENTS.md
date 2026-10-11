# AGENTS.md — contract for agents working in this repository

Any AI agent or model may work here. Follow these rules; they exist to keep the
repo safe, reviewable and easy to hand off between sessions and models. The
human (Frank) has the final say.

## Hard rules

1. **Never commit secrets.** No tokens, keys, passwords, or personal credentials.
2. **Small, reviewable changes.** One topic per pull request or commit.
3. **Never rewrite history or force-push.** `git pull --rebase` before you push.
4. **Stay in scope.** Focus on the landing page, content, responsiveness, and performance.
5. **No invented facts.** Cite sources; reflect Daniel Cerezo's authentic work and values.
6. **100% Local-First Mandate** — prioritize local tooling and compute.

## Commit identity

Use Frank's identity for commits:

```bash
git -c user.name="Frank" \
    -c user.email="100420113+frankinkua@users.noreply.github.com" commit -m "..."
```

Add a trailer naming the agent so work is attributable:

```
Swarm-Agent: <Your Name> (<model, if known>)
```
