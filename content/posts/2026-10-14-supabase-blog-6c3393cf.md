---
title: A local Supabase project per agent, with or without Docker
title_original: A local Supabase project per agent, with or without Docker
date: '2026-10-14'
source: Supabase Blog
source_url: https://supabase.com/blog/local-supabase-project-per-agent-with-or-without-docker
author: ''
summary: '[翻译失败，原文如下]


  The Supabase CLI now runs several local projects on one machine, one per git worktree,
  and runs them without Docker. Each coding agent ge...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-16T06:41:16.415557'
---

[翻译失败，原文如下]

The Supabase CLI now runs several local projects on one machine, one per git worktree, and runs them without Docker. Each coding agent gets its own database to reset, migrate, and test against while the others keep working. Local projects start in seconds and use about a tenth of the memory, and the remote branch that picks up the work when a pull request opens is nearly five times faster.

Multiple projects and the native runtime ship in CLI v2.119.0 behind an experimental flag. Faster branches are on for every project today.

## Each agent gets its own project#

Suppose one agent is adding billing while another reworks signup. Give each one a git worktree and runsupabase startin both:

Each worktree gets its own Postgres, Storage, Edge Functions, and MCP server, on ports the CLI picks and remembers across restarts. The billing agent can runsupabase db resetwhenever it likes and the signup agent's tests never notice. Agents read their URLs and keys fromsupabase start --output-format jsoninstead of assuming the defaults, and withDeclarative Schemas 2.0they edit schema files and let the CLI write the migration.

No more coordinating project IDs or ports by hand, which has been one of themost requested changesto the CLI.

## Projects start in seconds and stay small#

supabase startbrings up Postgres and leaves every other service asleep until its first request. If your task never touches Storage, Storage never runs. Sleeping services use no CPU or memory, stop again when idle, and wake on the next request. Pass--eagerif you want everything up front.

Nine idle projects now fit in the memory one used to take, which is what makes a project per worktree practical on a laptop.

## No Docker required#

Agents increasingly work in hosted sandboxes and CI runners that have no container engine. The native runtime runs all 13 Supabase services as plain processes, at the same pinned versions as the Docker images, with the full Postgres extension set including pgvector. When Docker isn't available the CLI picks it for you, or select it directly:

It runs on Linux (amd64 and arm64, glibc 2.35 or later) and macOS 14 or later on Apple silicon. Docker stays the default when it's present and is still the better fit for several projects on one laptop, since each container gets its own network and file system. Think of native as one project per sandbox. Running Supabase locally without Docker has been along-running requesttoo.

## Branches are ready nearly five times faster#

When the pull request opens, a remote branch gives reviewers a URL to point a build at, and that branch now arrives configured like the project it came from. Auth, Storage, network restrictions, and deployed Edge Functions all carry over at creation, with function bundles copied in parallel so a project with 40 functions comes up as fast as one with two. Secrets stay behind and production data stays out unless you choose to branch with it, so the branch is safe to hand to a reviewer the moment it's ready.

## Get started#

Update to CLI v2.119.0 or later and turn on the experimental engine. For a new app:

For an existing app, addstack = trueunder[experimental]insupabase/config.tomland follow theport-removal checklistbefore your first start. Commit the file so every worktree gets the setting.

Then pick the setup that matches where your agents work:

- Several agents on your computer: run Docker or Podman, give each agent its own worktree, and runsupabase startin each. Themultiple local projects guidecovers listing, stopping, and removing projects.
- One project in a sandbox or CI runner: runsupabase start --runtime nativeon a supported platform. No container engine needed. Theruntimes guidecovers sandbox setup and download allowlists.
- A branch on a pull request: nothing to turn on. Branches already inherit their base project's configuration, and theBranching guidecovers each way to create one.

The experimental engine keeps its data separate from your existing local project, and its flags and output can still change, so read thedifferences and limitationsbefore moving a workflow over.

Have feedback?Please share it in theCLI repo.

---

> 本文由AI自动翻译，原文链接：[A local Supabase project per agent, with or without Docker](https://supabase.com/blog/local-supabase-project-per-agent-with-or-without-docker)
> 
> 翻译时间：2026-10-16 06:41
