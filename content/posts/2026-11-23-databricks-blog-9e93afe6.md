---
title: What 5,400 Malicious npm Packages Reveal about Software Supply Chain Risk in
  2026
title_original: What 5,400 Malicious npm Packages Reveal about Software Supply Chain
  Risk in 2026
date: '2026-11-23'
source: Databricks Blog
source_url: https://www.databricks.com/blog/what-5400-malicious-npm-packages-reveal-about-software-supply-chain-risk-2026
author: ''
summary: '[翻译失败，原文如下]


  - Hijacked real packages cause nearly all the exposure. Compromised legitimate packages
  are only 7% of the 5,400 malicious packages, but ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-24T12:13:05.909999'
---

[翻译失败，原文如下]

- Hijacked real packages cause nearly all the exposure. Compromised legitimate packages are only 7% of the 5,400 malicious packages, but they account for over 99% of downloads.
- Attackers have moved from stolen tokens to build pipelines. After npm revoked long-lived tokens, attackers took over CI environments and published through trusted publishing; 85% of trusted-published packages in the set are compromises.
- AI development tools are a new target. Malicious MCP servers, packages that tamper with AI assistant configuration, and stealers of AI service keys are going after an attack surface that didn't exist two years ago.

## Executive summary

This report is the first of a series of blogs analyzing the supply chain threat landscape. In this first part, we analyzed approximately 5,400 confirmed malicious npm packages published between December 2025 and October 2026, the first year following npm's revocation of long-lived authentication tokens [1]. Eight findings follow.

1. Exposure is concentrated in compromised legitimate packages.Attacker-created malware packages constitute 89% of the set but 0.2% of its recorded downloads. Compromised legitimate packages constitute 7% of the set and over 99% of downloads.
2. Install-script controls address roughly half of observed malware.54% of packages declare a lifecycle script; the remainder execute on import or invocation. The largest campaign of the period, exceeding one thousand packages directed at a single organization, declared a lifecycle script in 1% of packages and alternated between import-time execution and postinstall hooks across successive waves.
3. Account compromise has shifted from stolen tokens to compromised build pipelines.The highest-exposure victims of the August 2026 self-replicating worm campaign were republished through OIDC trusted publishing from compromised CI environments. Of packages in the set published via trusted publishing, 85% are compromised legitimate packages; attacker-created packages use trusted publishing in 0.1% of cases.
4. Attacker infrastructure is predominantly legitimate shared services.38% of malicious packages communicate with a legitimate third-party service: serverless hosting, chat-platform webhooks, code-hosting and paste sites, request-capture endpoints, and in a small number of cases public blockchain RPC nodes used as dead-drop resolvers. Domain reputation does not distinguish this traffic from normal developer traffic.
5. A distinct class of activity targets AI development tooling.MCP server packages that harvest credentials from the agent host, packages that modify AI assistant configuration and instruction files, and credential stealers specialized in AI service keys together form a population whose principal targets, MCP hosts and assistant configuration, did not exist as an attack surface two years ago.
6. Offensive-security frameworks marketed as AI agents are distributed through npm.Agentic offensive security frameworks have begun appearing on the registry for open source distribution, bundling remote-access, cloud-credential and enterprise-identity tooling with modules for adversarial testing of AI systems. Public reporting has already observed threat actors making use of agentic tooling against exposed secrets.
7. The registry is used as a distribution channel for payloads unrelated to the software supply chain.The registry offers attackers free, highly available hosting under a trusted domain, and its content is redistributed by public CDNs and mirrors; victims who never run the package manager can therefore be served a payload directly from npm infrastructure.
8. Removal is slower than reporting, and attackers remove their own packages faster than the registry does.87% of confirmed packages have a public advisory; unattributed packages receive one at a median of 1.7 days after publication. The registry's security takedown follows at a median of 7 days, with 10% exceeding 59 days. 37% of attacker-created packages were unpublished by their own publisher, at a median of seven hours, before any takedown. 16% remained installable at the time of this analysis.

## Scope

The dataset comprises packages detected by our scanner, which analyzes npm publish events for suspicious packages, with results filtered for precision by retaining only packages with at least one independent source: a public advisory, a vendor-published campaign report, an npm security takedown, or analyst review. Time is measured by npm publish date. The unit of record is the package version; a package is dated by its first malicious version. Download counts are monthly snapshots recorded at scan time. Registry active status was checked against the public registry on November 6, 2026.

![image3.png](/images/posts/e9f91c6defd3.png)

Figure 1: Verdict Type by Month (%)

## Volume

Monthly counts of confirmed malicious packages vary by a factor of fifteen across the period. The variation is attributable to a small number of campaigns: in August 2026 a single dependency-confusion campaign accounts for 78% of confirmed versions. When each campaign is counted as a single actor, activity is stable: several hundred new publisher accounts per month, a flat rate of malicious packages relative to total packages published, and spikes attributable to named campaigns.

![image9.png](/images/posts/07d098f5a171.png)

Figure 2: Verified Malicious npm Packages by First-Publish Month

Three changes are observable after this normalization:

Compromise of legitimate packages is episodic.Activity is negligible in most months. Three waves of a single worm family occurred in May, June and August 2026; the May and August waves each compromised more than one hundred packages, and the June wave republished a vendor's entire scope in one day.

![image12.png](/images/posts/ad18b61dee0a.png)

Figure 3: Legitimate-Package Compromise, Poisoned Versions by Month

Dependency-confusion reconnaissance is continuous, present in every month at a consistent level.

Obfuscation increased.The share of actors whose packages trigger an obfuscation rule more than doubled between May and August 2026.

Targeting of AI-developer credentialsremained at 1-4% of packages throughout the year; absolute counts rose with volume. Theft of npm authentication tokens peaked at 22% of packages in March 2026 and fell below 5% from May. Classic long-lived tokens had been revoked on December 9, 2025; the tokens targeted in this period were plausibly granular access tokens and CI secrets.

![image4.png](/images/posts/8513928b8f6b.png)

Figure 4: Share of Verified Packages Targeting Each Credential Class, by Month

![image13.png](/images/posts/ed89f252b837.png)

Figure 5: Cloud and AI-Dev Targeting: Packages vs. Actors (% of month)

## Anatomy of a malicious package

![image7.png](/images/posts/89723d3b3cbd.png)

Figure 6: Profiles of Verified Malicious npm Publishing, May–October 2026

Publisher account.99% of malicious packages are published by single-maintainer accounts; 55% of accounts use a free-mail address. Two thirds of accounts publish exactly one malicious package; among accounts publishing more than one, the median interval from first to last malicious publish is under one day. DPRK-nexus campaigns are the exception, operating several hundred accounts at one to two packages each, 83% on free-mail addresses. Other named campaigns use free-mail addresses in 15% of cases, consistent with procured account pools.

![image14.png](/images/posts/14cf2e803502.png)

Figure 7: Publisher accounts behind Verified Malicious npm Packages

[翻译失败，原文如下]

Package metadata.88% of packages are under thirty days old at the malicious publish; 75% declare no repository; 66% have a single version; 65% retainnpm inittemplate values in the author, description or repository fields. 54% declare a lifecycle script. 17% carry an internal-looking name (core, utils, sdk, config). Typosquatting is a minority tactic: 13% embed a popular package name and under 5% are within two character edits of one.

![image19.png](/images/posts/2e8131191a46.png)

Figure 8: Author and Repository Spoofing in package.json file (%)

![image17.png](/images/posts/779158af54fd.png)

Figure 9: Ecosystem Keywords Used in Malicious Package Names

Compromise indicators.Compromised legitimate packages differ from attacker-created packages on the version-level change signals. 78% of compromised versions add or modify a lifecycle script, compared with 4% of attacker-created packages. 23% show a change of maintainer or publisher. The majority of compromises are published through the legitimate account and leave ownership records unchanged.

![image8.png](/images/posts/59a925361d6d.png)

Figure 10: Takeover Shape, Compromised Legitimate Packages vs Attacker-Published

Behavior.72% of packages have an obfuscation marker, and 30% retrieve a second stage. Credential and data theft is the predominant behavior in every month, except August. A significant number of packages in August stole credentials but ultimately aimed to deliver on the victim machine a Sliver command-and-control implant, changing its classification to Trojan / Downloader.

![image5.png](/images/posts/f68092979420.png)

Figure 11: Malware Packages by Behavior and Month

Of credential stealers, 45% target a single credential class and 36% target three or more. Single-class stealers are distributed evenly across cloud credentials, SSH keys, AI-developer credentials, npm tokens and.envfiles. In multi-class stealers, cloud credentials, SSH keys and.envfiles co-occur; wallet and browser-data theft occur separately. AI-developer credentials are the most specialized target: 80% of packages that target them target no other class.

![image11.png](/images/posts/8067e3611fef.png)

Figure 12: Co-occurrence of credential classes

Platform.55% of packages contain no operating-system-specific code. Among the remainder, droppers target Windows (PowerShell, scheduled tasks, executables) and credential stealers and backdoors target Linux (systemd, cron, shell configuration files). macOS-specific code appears in approximately one in eight stealers.

![image15.png](/images/posts/f3aeb58ab6b2.png)

Figure 13: Targeted OS

Lures.24% of packages are scoped, across more than three hundred distinct scopes, most of which contain a single malicious package: an organization's internal namespace registered once. 36% declare an author and 24% a repository; where present, approximately 80% of each refer to an identity other than the publishing account. 62% include a README; of these, 16% contain an installation command for a different package, in half of those cases a popular one. The majority of attacker-created packages employ no lure, consistent with the exposure finding: these packages are retrieved by misconfigured builds rather than selected by users.

![image16.png](/images/posts/f73c7cf4c738.png)

Figure 14: Package-name lures (%)

## Compromised legitimate packages

Compromised legitimate packages are 7% of the set and over 99% of its download exposure.

![image6.png](/images/posts/6f01342e9aa5.png)

Figure 15: Downloads per Month at Scan Time

All compromise waves in the period belong to one family, first the toolkit of a single threat actor and later open-sourced for free use in May. The May and August worms each compromised more than one hundred packages. In June 2026 the same open-source kit republished a single vendor's entire scope in one day through trusted publishing, followed within days by a small number of unrelated packages. Outside these waves, compromise occurs at a rate of a few packages per month.

Worm-compromised versions are distinguishable from attacker-created packages: all execute through a lifecycle script, one third read cloud credentials or the Kubernetes service-account token, and 44% trigger obfuscation rules. They receive public advisories within hours of publication.

The August wave's highest-exposure victims were republished through OIDC trusted publishing from compromised CI environments rather than through stolen tokens. Across the period, 85% of packages in the malicious set published via trusted publishing are compromises. The December 2025 token revocation directed maintainers toward trusted publishing; subsequent compromise activity targeted the publishing pipeline directly.

## Infrastructure, exposure and public reporting

Shared legitimate services.38% of packages, and 42% of those with a network indicator, communicate with a legitimate third-party service. Serverless hosting is most common; Cloudflare Workers alone serves several hundred packages from a comparable number of accounts. Code-hosting and paste sites follow, then Telegram, Discord and Slack webhooks. A small population retrieves its payload address from a smart contract via a public blockchain RPC endpoint; two thirds of these packages are heavily obfuscated and 42% ship a compiled binary. 8% of droppers carry no resolvable host, with the second-stage URL constructed at runtime.

![image18.png](/images/posts/8c4cfcd25d15.png)

Figure 16: Share of Packages Routing Through a Legitimate Service, by Month

Exposure.81% of attacker-created packages had no downloads at the time of scanning. The ten most-downloaded packages in the set account for over 99% of recorded downloads; all are compromised legitimate packages.

Time to public advisory.87% of the set has an OSV advisory. Named worm and dependency-confusion campaigns receive advisories on the day of publication. Unattributed packages receive advisories after a median of 1.7 days, with 10% exceeding one month. DPRK-nexus packages receive advisories after a median of 4.5 days, with 10% exceeding two months, the slowest of any developer-facing population.

![image1.png](/images/posts/c99b6ef42300.png)

Figure 17: Exposure Before Public Reporting

Registry outcome.Each attacker-created package was checked against the registry at the time of analysis. 40% had been replaced by npm's security placeholder, at a median of 7.1 days after publication and 10% after more than 59 days. 37% had been unpublished by their own publisher, at a median of 0.3 days; attackers withdraw packages faster than the registry removes them, and the share of self-removal rose through the year. 7% had been deleted without a recoverable timestamp. 16% remained installable. Removal rates vary by actor: 64% of DPRK-nexus packages were removed by npm, at a median lag of 19.5 days, and 5% remain installable; individual DPRK-nexus campaigns range from 16.4 to 65.9 days. Of unattributed packages, 21% remain installable. The registry takedown is a slower control than public reporting: from March 2026 onward the median advisory preceded the median takedown in every month.

![image10.png](/images/posts/e836e0c32180.png)

Figure 18: Where Malicious Packages Ended Up

![image2.png](/images/posts/fdea7f27df49.png)

Figure 20: Days from Publish to Removal or Advisory, by Publish Month

Outcomes differ sharply by campaign. Campaigns that received same-day advisories had median takedown lags of a few days or less. DPRK-nexus campaigns received advisories within days but remained installable for weeks to months; every DPRK-nexus tag in the dataset has a median takedown lag above two weeks. A further group of campaigns, including five crypto-wallet stealer families, was never removed by the registry: the publishers withdrew every package themselves, typically within a day, and the registry recorded no security action.

## Recommendations

[翻译失败，原文如下]

1. Install-script blocking is a partial control.It addresses the half of attacker-created packages that execute through a lifecycle script and all worm-compromised versions, and none of the packages that execute on import. Combine it with lockfile integrity enforcement and a registry proxy applying an allowlist or minimum-age policy.
2. Monitor lifecycle-script changes between versions of existing dependencies.78% of compromised versions add or modify a lifecycle script; 23% change maintainer or publisher.
3. Restrict credentials available to build environments.One third of worm victims and half of MCP-abuse packages read cloud credentials. Short-lived, job-scoped credentials limit the impact.
4. Treat trusted publishing as provenance, not assurance.It attests that a package originated from a pipeline, not that the pipeline was uncompromised. Pin CI actions, exclude secrets from pull-request builds, and review provenance attestations at publish time.
5. Do not rely on domain reputation for build-time egress control.38% of malicious packages communicate with Cloudflare, Vercel, GitHub, Telegram or public blockchain nodes. Egress policy must be allowlist-based.
6. Register organizational scopes on the public registry.More than three hundred scopes were registered by attackers in the period, most once. Configure package managers to resolve internal scopes exclusively from internal registries.
7. Protect AI assistant configuration as a credential store.Assistant configuration directories, MCP host configuration and instruction files are read and written by malicious packages. Apply file-integrity monitoring equivalent to that for SSH keys.
8. Prepare for agent-operated intrusions.Autonomous offensive frameworks are now one npm install command away from a motivated actor. Plant content that trips an attacking agent's guardrails or diverts its plan, deploy canary credentials where an agent will enumerate them, and add agent-driven patterns to SOC detection: bursts of API calls with changing parameters, enumeration from one principal across many services, and credential use seconds after discovery.

This is the first in a series of posts on supply chain threats. In our next report, we will discuss emerging threats identified in the dataset that we believe are expanding the role of the npm registry beyond traditional malware distribution.

## References

[1] GitHub (2025). “npm classic tokens revoked, session-based auth and CLI token management now available”.

https://github.blog/changelog/2025-12-09-npm-classic-tokens-revoked-session-based-auth-and-cli-token-management-now-available/

---

> 本文由AI自动翻译，原文链接：[What 5,400 Malicious npm Packages Reveal about Software Supply Chain Risk in 2026](https://www.databricks.com/blog/what-5400-malicious-npm-packages-reveal-about-software-supply-chain-risk-2026)
> 
> 翻译时间：2026-11-24 12:13
