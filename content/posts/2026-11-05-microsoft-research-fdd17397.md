---
title: Formally verifying agent-written full-stack web apps with PDD Kit - Microsoft
  Research
title_original: Formally verifying agent-written full-stack web apps with PDD Kit
  - Microsoft Research
date: '2026-11-05'
source: Microsoft Research
source_url: https://www.microsoft.com/en-us/research/blog/formally-verifying-agent-written-full-stack-web-apps-with-pdd-kit/
author: ''
summary: '[翻译失败，原文如下]


  ![PDDKit decision flowchart on green gradient background](/images/posts/9cec1be357df.jpg)


  ## At a glance


  - Formal methods for everyday ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-10T09:31:26.172481'
---

[翻译失败，原文如下]

![PDDKit decision flowchart on green gradient background](/images/posts/9cec1be357df.jpg)

## At a glance

- Formal methods for everyday software.PDD Kit helps you turn your intent into a formal spec, then proves the code your agent writes for every input and uses tests where a proof can’t reach. It takes formal methods beyond niche, specialist work to engineers without a formal methods background and to everyday applications, like the full-stack web app shown here.
- Exhaustive line-by-line human review can become difficult to scale asAIagents generate increasingly large amounts of code.The plan is supposed to be the contract between you and a coding agent, but nothing actually forces the agent to follow it. The tests it writes usually check what it built, rather than what you asked for.
- PDD Kit makes the agent keep the plan.It works with you to turn your intent into a formal specification inVerus(opens in new tab), proves the agent’s code meets that spec for every input, and falls back to tests where a proof can’t reach.
- We tried it on a full-stack web app.Inside GitHub Next’sChopin(opens in new tab), we used PDD Kit to formally verify the login logic of Pet Store, aRust(opens in new tab)storefront. Verus hardened the code and uncovered existing bugs, proving the absence of login bugs with respect to the specification. The developer reviewed the intent and never read the generated code line-by-line.

## The plan is the contract the agent should follow, but nothing constrains the agent to follow it.

Coding agents now ship whole features in one sitting often spanning tens of thousands or hundreds of thousands of lines of code. As a result, reading every line of the pull request doesn’t scale to this new way of work. Now, most teams invest in the plan and relevant testing instead: describe to an agent what they want, go back and forth until the plan and proposed tests look right, and hand them off to the agent for implementation.

This plan or natural language spec is meant to be the contract that an agent holds. However, in practice, the agent can drift from it. It implements something slightly different, then writes tests that pass for its implementation rather than the code you intended it to write. Continuous integration (CI) grows due to a profusion of low quality and high quantity of tests, coverage looks healthy, and the gap between what you asked for and what shipped stays hidden until a bug report or a nasty edge case shows up.

So, how do you reliably scale review as agents generate increasingly large amounts of code? Agent code fails in two ways a careful reviewer would usually catch: it leaves out something obviously necessary, or it does something obviously wrong. Tests alone don’t close that gap, because they only exercise a tiny slice of what a program can do. Closing it needs a different kind of machinery, which is where proofs come in.

Microsoft Research StorY

![Abstract teal-toned image of aluminum cans viewed from above, overlaid with a network of connected flowchart shapes (rectangles, rounded nodes, and diamonds) linked by thin line.](/images/posts/358807830109.jpg)

## OptiMind: When the system meets the floor

A three‑month pilot in a Midwestern bottling plant shows what happens when AI moves beyond chat and into decision-making, where constraints shift, stakes are real, and answers must hold.

Review asks “does this look right?” A proof answers “is this right?” A mathematical proof shows that code meets its specification foreveryinput, including the ones your test suite can miss. That provides stronger assurance for specified properties than testing alone, especially when line-by-line review isn’t practical.

Proofs used to be too expensive for everyday software. You needed specialists, unfamiliar languages, proofs many times larger than the code, and proofs took years to develop, but two things have changed since. First, recent advances in coding agents have made it increasingly practical for them to help generate formal proofs from well-defined specs. Secondly, agents can now better help you write formal specs. We call this new software development paradigmProof-Driven Development(PDD). PDD Kit is our toolkit for it.

## How PDD Kit works

PDD Kit is to formal methods roughly whatSpec Kit(opens in new tab)is to Spec-Driven Development. It runs as a partner insideChopin(opens in new tab), GitHub Next’s real-time, multiplayer planning environment, where a team and agents can plan in one shared document.

The workflow has two halves (Figure 1). First, team members review intent in plain language. PDD Kit asks the questions a careful reviewer would ask, explains the relevant code as it goes, and records the answers in anintentartifact, a document that bridges the user’s intent with the formal specification or tests. The parts of the user’s intent that can be formalized are converted into formal specifications and the rest, which must be taken on trust, are converted to informal specifications for tests. PDD Kit automatically generates proofs that the code satisfies the derived formal specs and high-quality tests for the informal specs. You don’t need a formal methods background for any of it.

Consequently, every result in PDD Kit says which kind of verification it rests on:

- Formal verificationis a mathematical proof that code satisfies its specification for every possible input, checked by a tool called a verifier. For PDD Kit today, that verifier isVerus(opens in new tab), a proof language for Rust co-developed by Microsoft Research, Carnegie Mellon University, VMware Research, ETH Zurich, MPI-SWS, UNSW Sydney, the University of Texas at Austin, the University of Michigan, the University of British Columbia, the University of Wisconsin–Madison and the Weizmann Institute of Science.
- Empirical verificationchecks code by running it and observing what it does. It covers what a proof can’t reach, such as a third-party cryptography library or a user interface. It uses unit and end-to-end tests, terminal automation, browser agents, and computer-use agents for anything a browser can’t drive. A passing test only shows the code worked on the inputs it tried, so PDD Kit labels it as evidence rather than proof.

The line between the two is theTrusted Computing Base (TCB): the code that the proof assumes behaves as described. PDD Kit makes that line explicit and asks you to sign off on each piece.

## The capstone: a full-stack web app

To show PDD Kit integrating with existing codebases, we built Pet Store, a full-stack web app written entirely inRust(opens in new tab). The backend usesAxum(opens in new tab)andSQLite(opens in new tab)and handles inventory, promotions, orders and checkout. The storefront is aLeptos(opens in new tab)app compiled toWebAssembly(opens in new tab). Together they come to about 5,000 lines of Rust.

For brevity in this blog, we focus on formally verifying the login logic of the app, but the same process can be used to verify functional correctness of the entire app. PDD Kit recommends starting with the most sensitive parts of your application and incrementally verifying your application. A login bug can hand an attacker a customer’s account or an admin’s controls, so that’s where proof effort pays off first. The developer’s whole request in Chopin was two sentences:

Verify the login logic in backend/src/handlers/auth.rs. Here are my requirements:

1. You only get a token with the right password.
2. Only admin accounts get admin tokens.

We kept the request rough on purpose. Capturing the intent of the user and turning the user request into something a proof can check is PDD Kit’s job.

### Step 1: Questions before code

[翻译失败，原文如下]

PDD Kit’s planning workflow, pdd-plan, reads the code and comes back, before writing anything, with questions in aDecisionstab. When a question depends on how the code works, the card explains that part first: the goal, how the pieces fit, and the exact function involved, so you can answer without opening the source.

![Figure 2. The first decision card. “Only with the right password” on its own is also met by a login that refuses everyone. Proving both ways rules that out.](/images/posts/fdd54f56f19a.png)

The question looks pedantic, but it matters. “You only get a token with the right password” rules out the bad case, a wrong password getting a token, and a login that refuses everyone keeps that promise perfectly. “The right password always works” is the half that rules it out. Formally, the first is an implication (token ⇒ right password) and the second is its converse. Together they make an “if and only if.” An agent left alone would pick one without telling you, but here the developer picked both ways.

### Step 2: A human readable intent map

As the conversation goes on, PDD Kit keeps arough worksection at the top of the plan current, so a user can keep track of important concepts without having to scroll back through a long chat to find what was agreed. It includes a flowchart of the login being specified, a spec landscape of what will be proved and what will be trusted, and, when a picture helps, a mental model. For login, PDD Kit drew a ticket desk (Figure 3).

![Figure 3. PDD Kit’s mental model for login. The field you send picks the window, the window picks the table and with it the role, and nothing prints until the password matches.](/images/posts/743023dbb271.png)

Below it, theintent mapties each requirement back to the developer’s own words and records how it was settled (Figure 4). Each entry links to the section of the formal spec that models it and to the tests that cover it, and the spec section shows snippets of the Verus contract, annotated so the developer can see how the formal spec models their intent.

The decision card in Figure 2 is the kind of ambiguity an agent would otherwise settle silently. Figure 5 shows how small the difference looks on paper: the two readings disagree in a single cell, a right password that gets no token.

![Figure 5. Two readings of the same sentence. They differ in one cell, and that cell changes what the proof has to establish.](/images/posts/95569e79f29a.png)

### Step 3: Proving the login function

Before anything gets built, PDD Kit asks the team to sign off on the plan as a whole. Its first draft proved the decision at the center of login, picking the table and gating on the password, and kept the handler around it trusted and tested. That’s a sensible default, and it’s what PDD Kit recommended, but the developer wanted more. The handler is where the lookups get awaited and the token gets signed, and that glue is exactly where a refactor can quietly swap two lines. So at intent review the developer chose to give the login handler its own async spec, so the proof covers that glue too instead of trusting it (Figure 6).

![Figure 6. Proving more of login means trusting more small wrappers. The card says so before the developer chooses.](/images/posts/a98adb883972.png)

That choice moved almost everything into the proof and left the login handler with nothing to do but unpack the request. A new async function,login_flow, carries the contract from the request’s fields all the way to the token or the HTTP error. PDD Kit then brought the revised plan back for a fresh sign-off, because matching your intent isn’t proof, and it doesn’t approve new trust or a wider scope.

### Step 4: Where proof stops

There are plenty of things you can’t prove about a program, and login runs into most of them:

- Code the verifier can’t see.bcrypt’s hashing, sqlx’s queries and jsonwebtoken’s signing live in other crates, outside the proof.
- Facts about the outside world.What SQLite holds right now and what time the clock says are inputs to the program, not something its code can establish.
- Whether, and how fast, something finishes.The spec says what you get if login answers. A hung query, or a slow one, breaks nothing in it.
- Anything a person has to judge, like whether an error message helps or a screen makes sense.
- Whatever nobody wrote down.A proof covers its spec and says nothing about requirements outside it.

That’s where empirical verification comes in. PDD Kit spells out the trusted boundary, the part of the TCB this proof leans on. It wraps each trusted piece in a small function with an assumed contract, using Verus’s#[verifier::external_body]orexternal_fn_specification, asks the developer to accept each one on its own, and writes a test for every assumed clause into the plan. For login, the developer signed off on six pieces:

- The two lookups,Customer::find_by_emailandAdmin::find_by_username. Each awaited, successful lookup returns exactly the row its own table holds for that email or username, or none.
- check_password, a thin wrapper aroundbcrypt::verify. It errors only on a stored hash bcrypt can’t read, andOk(true)means exactly the right password.
- generate_token, which signs exactly the claims it is given under the configured secret and reports a signing failure as a 500.
- expiry_from_now, which reads the clock and writes an expiry exactly 24 hours later.
- database_error, which turns a failed lookup into today’s 500 with sqlx’s message.
- The login handler shell, which unpacks the request and passes its fields tologin_flowunchanged.

In the spec, a lookup keeps its code where it is and gets a contract from the outside withexternal_fn_specification:

/// Looks up a customer by exact email./// Trusted, not proved: the SQL query runs in sqlx, which Verus cannot check./// Every customer promise of `login_flow` rests on it.#[verifier::external_fn_specification]pub async fn ex_customer_find_by_email(pool: &sqlx::SqlitePool, email: &str)-> (r: Result, sqlx::Error>)ensures// When the query succeeds, it returns the customers row on// file for exactly this email, or None when there is none.r matches Ok(found) ==> found == customer_on_file(email@),{Customer::find_by_email(pool, email).await}

The clock is a small wrapper marked#[verifier::external_body]. Verus uses its ensures clause and never reads the body:

/// Reads the clock and computes a token's expiry 24 hours ahead./// Trusted, not proved: chrono's clock is outside the proof./// It panics if the time is out of range, as today's login does;/// that panic is not promised against.#[verifier::external_body]pub fn expiry_from_now() -> (r: Expiry)ensures// The expiry is exactly 24 hours (86,400 seconds) after the clock reading.r.exp as int == r.now as int + 86_400,{...}

Figure 7 puts the three layers together: what Verus proves, what people accept and tests check, and what nobody is promising.

![Figure 7. Where the login proof stops. Verus proves the core for every input. People accept the trusted ring and tests check it. The plan lists what nobody is promising.](/images/posts/e8bf373f4d97.png)

Figure 8 maps what gets proved and what gets trusted. Each trust decision is its own card. It shows the clauses Verus will take on faith, what the developer is accepting, and which promise falls apart if the assumption is wrong (Figure 9). Every assumed clause then gets an empirical check in the plan’s Empirical verification section, written as Given/When/Then scenarios before any test exists (Figure 10). An entry saysplanneduntil it has run, and then it records the command’s result and the commit it ran against.

![Figure 8. What gets proved and what gets trusted in login. Green functions are proved by Verus for every input. Amber pieces are trusted, accepted by the developer, and checked by the planned tests in the plan’s §4.1.](/images/posts/8067228f7601.png)

[翻译失败，原文如下]

![Figure 9. A trust card forcheck_password. Verus takes these two clauses on faith, so a person accepts them and two tests check them.](/images/posts/dee320a6a9be.png)

![Figure 10. A planned test for the trustedcheck_password, written before the test exists. The plan labels a passing test as evidence rather than proof.](/images/posts/b6f997d5b3a7.png)

The plan is just as explicit about what nobody is promising: that the login future ever completes, that an out-of-range clock won’t panic, anything about the timing or rate of attempts, and how other endpoints read the role.

### Step 5: Reading the spec

The intent artifact is what the team reviews. It’s the plain-language version of the formal spec PDD Kit writes as Verus contracts. You might be wondering whether someone now has to read the proof instead of the code. Nobody does, because the coding agent writes the proof and Verus checks every step of it. If Verus accepts the proof, it holds whether or not anyone reads it. The spec is what the proof is held to, so that’s what people review, and this one is short enough to learn to read in a few minutes. Each function gets an ensures block: statements about its result, r, that must hold for every possible input. Verus checks them when you build, and if any clause could fail for even one input, the build fails and Verus points at that clause. Each clause reads as an if-then, and Figure 11 takes apart the clause for the developer’s first requirement.

![Figure 11. The ensures clause on login_flow for “You only get a token with the right password.” The same account a appears on every line, which ties the password check to the token.](/images/posts/d8ebf8edb0e6.png)

Notice that the same a appears on every line, which ties the password check to the token. For example, imagine a bug where login checks the password against one account but signs the token for another. Bob logs in with his own, correct password and gets back a token for Alice’s account. Each step looks fine on its own, but this clause catches it, because the password check and the token have to name the same account. That’s the kind of wiring bug a test suite rarely thinks to look for. The spec also has to talk about SQLite, bcrypt and JWTs without running any of them. It does that withuninterpreted functions, names with no body:customer_on_file(email)andadmin_on_file(username)for the rows the database holds,bcrypt_verdict(password, hash)for what bcrypt would say, andtoken_claims(token, secret)for what a token carries. Verus knows nothing about them except what the trusted contracts from Step 4 promise. The proof says “whatever the database holds, login does the right thing with it,” and a trusted contract says “the lookup returns what the database holds.”

/// The customers row the database holds for/// exactly this email, if any, when login looks./// Left abstract: only `Customer::find_by_email`'s/// trusted contract says what it is.pub uninterp spec fn customer_on_file(email: Seq) -> Option;.../// What bcrypt says about `password` against a/// stored `hash`: Some(true) when it is the password/// the hash was made from, Some(false) when it is/// not, None when bcrypt cannot read the hash./// Left abstract: its meaning is bcrypt's, taken on trust through `check_password`.pub uninterp spec fn bcrypt_verdict(password: Seq, hash: Seq)-> Option;/// The password is the right one for the stored hash, by bcrypt's verdict.pub open spec fn password_matches(password: Seq, hash: Seq) -> bool {bcrypt_verdict(password, hash) == Some(true)}

On top of those,named_account(email, username)says which account a login names: the customers row for the email when one is sent, otherwise the admins row for the username, otherwise none. It’s written like Rust, but it’s a mathematical definition that never runs and only appears in contracts. Code like this is calledghost code, since the verifier checks it but the compiler erases it from the program. With it, the developer’s two-sentence request ends up as eight ensures clauses onlogin_flow(Figure 12).

/// The account a login names: the customers row for/// the email when one is sent (role "customer"),/// otherwise the admins row for the username (role "admin"), otherwise none.pub open spec fn named_account(email: Option, username: Option)-> Option{match email {Some(e) => match customer_on_file(e@) {Some(c) => Some(NamedAccount {id: c.id@, password_hash: c.password_hash@, role: customer_role() }),None => None,},None => match username {Some(u) => match admin_on_file(u@) {Some(a) => Some(NamedAccount {id: a.id@, password_hash: a.password_hash@, role: admin_role() }),None => None,},None => None,},}}

![Figure 12. The two-sentence request and the Both ways decision ended up as eight ensures clauses on login_flow. Four of them keep today’s refusals, so the storefront and the existing API tests keep working.](/images/posts/4147f09488d4.png)

Here’s the whole contract, with its doc comment trimmed. Each clause has the plain-English comment above it that the intent artifact shows the team:

/// The whole login, awaited end to end: from the/// request's fields to the token or the HTTP error./// ...pub async fn login_flow(pool: &sqlx::SqlitePool, config: &Config,email: Option, username: Option, password: &str)-> (r: Result)ensures// Neither an email nor a username: 400 with today's message.email is None && username is None==> (r matches Err(AppError::BadRequest(m))&& m@ == missing_identity_text()),// A token only for the account the login names, with its right// password; it carries that account's id and its table's role.r matches Ok(t) ==> (named_account(email, username) matches Some(a)&& password_matches(password@, a.password_hash)&& token_claims(t@, config.jwt_secret@) matches Some(c)&& c.sub@ == a.id && c.role@ == a.role),// The right password for the named account always gets a// token, unless a lookup or signing failure gives 500.(named_account(email, username) matches Some(a)&& password_matches(password@, a.password_hash))==> (r is Ok || r matches Err(AppError::Internal(_))),// A login naming an account nobody holds gets// 401, unless the lookup fails with 500.((email is Some || username is Some) && named_account(email, username) is None)==> (r matches Err(AppError::Unauthorized)|| r matches Err(AppError::Internal(_))),// A wrong password for an account whose hash bcrypt// can read gets 401, unless the lookup fails with 500.(named_account(email, username) matches Some(a)&& bcrypt_verdict(password@, a.password_hash) == Some(false))==> (r matches Err(AppError::Unauthorized)|| r matches Err(AppError::Internal(_))),// An account whose stored hash bcrypt cannot read gets 500 and no token.(named_account(email, username) matches Some(a)&& bcrypt_verdict(password@, a.password_hash) is None)==> r matches Err(AppError::Internal(_)),// The admin role only for an admins row// found by username, with no email sent.(r matches Ok(t) && token_claims(t@, config.jwt_secret@) matches Some(c)&& c.role@ == admin_role())==> (email is None && username matches Some(u)&& admin_on_file(u@) is Some),// An email login's token always carries the customer role.(r matches Ok(t) && email is Some)==> (token_claims(t@, config.jwt_secret@) matches Some(c)&& c.role@ == customer_role()),{unimplemented!()}

The trusted boundary shows up in the code too.check_passwordis one of the functions whose body Verus doesn’t check. Its contract ties it tobcrypt_verdict, an uninterpreted model of bcrypt with no axioms:

[翻译失败，原文如下]

/// Asks bcrypt whether `password` matches the stored `hash`./// Trusted, not proved: Verus cannot check bcrypt's hashing,/// so this wrapper's contract is assumed./// Every password promise of `login_flow` rests on it.#[verifier::external_body]pub fn check_password(password: &str, hash: &str) -> (r: Result)ensures// bcrypt answers (Ok) exactly when it can read the stored hash.r is Ok <==> bcrypt_verdict(password@, hash@) is Some,// Its answer is its verdict: true for the// right password, false for any other.r matches Ok(b) ==> bcrypt_verdict(password@, hash@) == Some(b),{bcrypt::verify(password, hash).map_err(|e| e.to_string())}

The doc comment above it says what rests on it: every password promise oflogin_flow. Every login ends in one of a handful of places, and only one of them has a token (Figure 13). The proof covers all of them at once.

![Figure 13. Every way a login can end, from the plan.](/images/posts/e05b50662117.png)

login_flowis async: it awaits a database query. Verus can put contracts on async functions, with one rule worth knowing (Figure 14). requires is checked when the call creates the future. ensures describes the value you get when you await it. Nothing promises the future finishes, so a hung query breaks no clause.

The doc comment onlogin_flowsays so in as many words:

/// ... No promise the future completes.pub async fn login_flow(...) -> (r: Result)

![Figure 14. When a contract is checked, for async fnand anasync fn.](/images/posts/2f724041296d.png)

login_flowstays short because it’s built from smaller proved pieces.lookup_targetpicks the table.login_coreawaits the lookup and callsdecide_login, the password gate.issue_tokensigns the token, or maps a refusal to today’s HTTP error. Each piece has its own contract, and Verus proveslogin_flowusing only those contracts, without re-reading their bodies. Change the body ofdecide_loginand onlydecide_logingets proved again.

Here’s the smallest piece, whole, and the start and end of the password gate:

pub fn lookup_target(email: Option, username: Option)-> (r: Result)ensures// An email, when sent, wins: customers are searched for exactly that email.email matches Some(e)==> r == Ok::(LookupTarget::CustomerByEmail(e)),// With no email, a username sends the search// to admins for exactly that username.email is None && username matches Some(u)==> r == Ok::(LookupTarget::AdminByUsername(u)),// With neither, the login is refused for missing an identity.email is None && username is None==> r == Err::(LoginError::MissingIdentity),

pub fn decide_login(target: &LookupTarget, found: Option, password: &str)-> (r: Result)ensures// No row found: refused as Unauthorized,// the same answer as a wrong password.found is None==> r == Err::(LoginError::Unauthorized),// Claims come back only for a found row// whose stored hash matches the password.r is Ok ==> found is Some&& password_matches(password@, found->Some_0.password_hash@),// The right password for a found row always gets claims.found matches Some(a) && password_matches(password@, a.password_hash@)==> r is Ok,...// An admins-table search gives the role text "admin".r matches Ok(c) && target is AdminByUsername ==> c.role@ == admin_role(),// A customers-table search gives the role text "customer".r matches Ok(c) && target is CustomerByEmail ==> c.role@ == customer_role(),

An overview of login.rs

Figure 15 maps the whole spec file,verified/src/login.rs. It reads top to bottom in four layers: headers, imports and types Verus needs to know about, an abstract view of the outside world, the trusted contracts that connect that view to real code, and the five contracts the proof has to meet.

![Figure 15. The parts oflogin.rs, in file order. Gray is header and types, purple is math that only appears in contracts, amber is trusted, and green is proven.](/images/posts/7a46c8987946.png)

Here are two of the less obvious parts, abridged. external_type_specification introduces a type Verus didn’t define. The pool stays opaque, while a customers row keeps its fields visible:

/// The connection pool, opaque to the proof: only/// the lookups' contracts say what it returns.#[verifier::external_type_specification]#[verifier::external_body]#[verifier::reject_recursive_types(DB)]pub struct ExPool(sqlx::Pool);.../// A customers row, with its fields visible to the proof.#[verifier::external_type_specification]pub struct ExCustomer(Customer);

And LoginError keeps the decision separate from the HTTP response, which is what lets issue_token pin each refusal to today’s status code:

/// Why a login gets no token.pub enum LoginError {/// Neither an email nor a username was sent: 400 Bad Request.MissingIdentity,/// No such account, or the password does not match: 401 Unauthorized.Unauthorized,/// bcrypt could not read the stored hash, with its message: 500 Internal.UnreadableHash(String),/// The lookup query failed: 500 Internal, with sqlx's message.Database(sqlx::Error),}

Before the plan comes back to you, two reviewer agents poke holes in the derived formal spec from the intent artifact to ensure a high-quality translation, so that the spec matches what you asked for and doesn’t promise more than a proof could show. The spec refinement runs in the background and takes live user feedback, iterating until reviewers agree that the spec is sound.

## Step 6: Prove, check, close the gaps

Signing off on the spec is where the developer’s review ends. Everything after it, the implementation and the proof, is checked by machines, which is why this post spends its time on the spec and not the proof. Once the developer signs off, aBuild planstage (Figure 16) hands the approved plan to pdd-prove, which turns it into a small task graph (Figure 16). For login, that’s seven tasks: get login.rs building under Verus inside the backend crate, prove the decision, the token and the whole flow, then write the tests for the trusted wrappers and the end-to-end login.

![Figure 16. Build plan turns the approved spec into seven tasks on a development machine. The first gets login.rs building under Verus without changing what any contract promises, and stops to ask rather than weaken a contract.](/images/posts/7d49a49a159e.png)

Each task runs the same loop:

- A coding agent writes the implementation and the proof, and Verus checks them against the derived formal spec.
- Anything in the trusted boundary gets the tests the plan called for.
- An LLM verifier reads the plan, the specification and the results side by side, and looks for gaps: requirements with no proof and no passing check. Gaps go back to the coding agent until none remain. If the specification itself has a gap, such as two requirements that contradict each other, it comes back to the developer as a decision.

A proof is only as good as its spec, sopdd-provechecks the spec too. When a model writes its own spec, or is tuned to produce proofs, it tends to land on weak invariants: clauses that verify but rule out almost nothing. They prove something, just rarely the thing you care about. We call that “vibe verification.” That’s why it’s so important to make sure your intent is aligned with the agent and what PDD Kit is great for.

The loop is strict about not moving the goalposts. If an async construct can’t be expressed in the pinned Verus, the task stops and asks the team instead of switching to a non-async helper or weakening a contract.

How does PDD Kit remove classes of bugs? The mutation check is how PDD Kit guards against vibe verification. pdd-prove plants one bug per ensures clause in a scratch copy of the code, like refusing everyone or checking the username before the email, and Verus has to reject each mutant on the clause it targets. A mutant that gets through means that clause constrains nothing, and it comes back as a gap.

## Step 7: Review intent alongside verified code

[翻译失败，原文如下]

When the tasks pass,pdd-proveopens pull requests. They add a verified/ crate withlogin_flow, its pieces, their proofs, and the trusted wrappers with their tests, and route the real login handler throughlogin_flow, keeping the existing HTTP status codes. Your verified logic integrates with and hardens your production login path, not a copy of it.

The developer was able to merge without relying on exhaustive line-by-line review of the generated code. The review had already happened on the intent artifact this whole time, where the team has the final say. We shifted more of the review focus from code review to intent review. The pull request works as a receipt, and its description marks every login requirement as either formally verified or empirically checked.

Merging is where the proof joins the team’s normal workflow. PDD Kit’s pdd-ship workflow adds the Verus check to CI next to the empirical tests, so every later change to login, by a person or an agent, has to keep proving against the same spec, and a broken proof fails the build like a failing test. And because a proof covers every input, PDD Kit prunes tests that only re-check what’s already proved, such as example-based tests of the password gate, and keeps the ones that guard the trusted boundary, so CI gets stronger and leaner at the same time.

## What the proof does and doesn’t say

“Fully verified” is easy to oversell, so here’s exactly what we’re claiming.

- Proved.The bodies oflogin_flow,login_core,lookup_target,decide_loginandissue_tokenmeet their contracts for every input. Login picks the right table, compares the request’s password against the stored hash of the account it names, issues a token with that account’s id and the role its table gives, and refuses everything else with today’s 400, 401 or 500 and no token.
- Trusted and tested.The two database lookups,check_passwordover bcrypt, the clock, token signing, the database error message and the handler’s request unpacking sit outside the proof, each behind an assumed contract the developer accepted. Tests against the real bcrypt, the real SQLite schema and the real router cover them.
- Assumed.The Verus, Rust compiler andZ3(opens in new tab)toolchain, and Verus’s standard libraryvstd(opens in new tab).

## Why Rust

PDD Kit only verifies Rust today, since that’s the language Verus works on. If your codebase is already Rust, there’s nothing to migrate. Code in other languages can be ported to Rust and checked against the same spec, and non-Rust projects can call verified Rust through bindings.

There’s also a less obvious upside. Once reliance on exhaustive line-by-line review has been reduced, readability stops being the main reason to pick a language. You can pick one for speed and safety, and optimize as hard as you want, because any change that breaks the spec fails the proof.

## What to Expect from PDD Kit

PDD Kit is a research prototype, and it only verifies Rust today since that’s the language Verus works on. Code in other languages can be ported to Rust and checked against the same spec, and non-Rust projects can call verified Rust through bindings. Proofs still take real effort, mostly in producing the proof itself, and a clear spec is what keeps that effort down, which is why so much of PDD Kit is about getting intent right first. We’d start where a bug costs the most, such as login, payments, or permissions, and verify the rest of a codebase one piece at a time.

Pet Store’s login is one piece of one app: a spec anyone can read, a Verus proof that the code matches it, and tests for everything the proof takes on trust. We want to be upfront about the weakest links. The guarantees are only as strong as the six trusted pieces, and two carry most of the weight:check_passwordfor every password promise, and the two lookups for every promise about which account a token names. Tests support them, but nothing proves them. We expect that trusted boundary to shrink significantly over time, so a growing share of the code can be formally verified, and we want to find out how far this scales.

What we’re really changing is what people review. Instead of relying mainly on line-by-line review of agent-generated code, a team reviews what it meant, in plain language, and a proof holds the code to it. The plan was always supposed to be the contract, and now the agent actually has to keep it.

## Acknowledgments

This work is a collaboration between the Microsoft Research Catalyst Lab, GitHub Next, and the Research in Software Engineering (RiSE) group. We would like to thank Maggie Appleton and Krzysztof Cieślak of GitHub Next for their collaboration on Chopin, and Nikhil Swamy, Lef Ioannidis, Janardhan Kulkarni, and Shuvendu Lahiri for their feedback and discussions on formal verification and intent formalization. We also thank the F*/Pulse and Verus teams for their support. Finally, we thank Idan Gazit of GitHub Next for supporting this collaboration.

[翻译失败，原文如下]

- If AI writes the spec, who makes sure the spec is right, and doesn't a wrong spec just give me the wrong verified code?You do, and yes, it would. A proof shows the code meets the spec, not that the spec is what you meant. That’s why PDD Kit is built around existing research in intent formalization. Thepdd-planworkflow reads your code, asks questions before writing anything, and turns your answers into a Verus spec plus a plain-language plan you approve, flagging ambiguity instead of guessing. Two reviewer agents check the spec, and thepdd-proveworkflow plants one bug per clause to catch clauses that verify but rule out nothing. A wrong spec is still possible, which is why PDD Kit emphasizes making requirements explicit, identifying ambiguities, and keeping developers involved in reviewing and approving the spec before verification begins.
- How is this different from Spec-Driven Development (SDD), Test-Driven Development (TDD), or just telling the agent to check its own work?The difference is what holds the code to the plan.ApproachWhat checks the codeSpec-Driven DevelopmentNothing enforces the specTest-Driven DevelopmentTests on a sample of inputs, often written to match what was builtAgent checks its own workThe same model that wrote the codeProof-Driven DevelopmentVerus automatically verifies the proof that your code satisfies the spec your approvedPDD keeps the planning loop from SDD and still uses tests where a proof can’t reach. A test checks some inputs, while a proof establishes that the code satisfies specified properties for all inputs covered by the formal model, under its stated assumptions.
- What exactly is the proof? Where does it run? Is it deterministic or another language model (LM)? And how long does it take?The proof is Rust code annotated with Verus constructs, checked mechanically by Verus using the Z3 solver. It runs wherever your Rust builds: thepdd-proveworkflow runs it while proving, and thepdd-shipworkflow adds it to your build and CI so a broken proof fails the build. The check is deterministic, with no model involved. Models write the spec, code, and proof, but only a deterministic Verus run decides whether it passed. How long the check takes varies with the size of the code and how hard the proofs are: usually seconds for a small module, up to minutes for a larger codebase.
- If verification replaces line-by-line code review, what do I actually review?PDD Kit shifts more of the review process toward validating what the code should do, while using formal verification to provide additional assurance that the implementation meets those requirements. Developers review the natural-language plan, the formal spec, and the trusted components that fall outside the scope of the proof. The resulting pull request documents what was formally verified, what was tested, and where additional review may be needed. On the Pet Store full stack web app, this approach reduced reliance on exhaustive line-by-line review of the generated code.
- Is it Rust only? And why Verus instead of other verification tools or formal languages?We chose Verus because it allows us to verify Rust code directly, aligning with PDD Kit’s focus on integrating formal verification into existing Rust development workflows. Other proof languages (e.g., Lean, F*, Rocq) take different approaches to formal verification, each with its own tradeoffs. The techniques behind PDD Kit could help put them to work as well.

You do, and yes, it would. A proof shows the code meets the spec, not that the spec is what you meant. That’s why PDD Kit is built around existing research in intent formalization. Thepdd-planworkflow reads your code, asks questions before writing anything, and turns your answers into a Verus spec plus a plain-language plan you approve, flagging ambiguity instead of guessing. Two reviewer agents check the spec, and thepdd-proveworkflow plants one bug per clause to catch clauses that verify but rule out nothing. A wrong spec is still possible, which is why PDD Kit emphasizes making requirements explicit, identifying ambiguities, and keeping developers involved in reviewing and approving the spec before verification begins.

The difference is what holds the code to the plan.

PDD keeps the planning loop from SDD and still uses tests where a proof can’t reach. A test checks some inputs, while a proof establishes that the code satisfies specified properties for all inputs covered by the formal model, under its stated assumptions.

The proof is Rust code annotated with Verus constructs, checked mechanically by Verus using the Z3 solver. It runs wherever your Rust builds: thepdd-proveworkflow runs it while proving, and thepdd-shipworkflow adds it to your build and CI so a broken proof fails the build. The check is deterministic, with no model involved. Models write the spec, code, and proof, but only a deterministic Verus run decides whether it passed. How long the check takes varies with the size of the code and how hard the proofs are: usually seconds for a small module, up to minutes for a larger codebase.

PDD Kit shifts more of the review process toward validating what the code should do, while using formal verification to provide additional assurance that the implementation meets those requirements. Developers review the natural-language plan, the formal spec, and the trusted components that fall outside the scope of the proof. The resulting pull request documents what was formally verified, what was tested, and where additional review may be needed. On the Pet Store full stack web app, this approach reduced reliance on exhaustive line-by-line review of the generated code.

We chose Verus because it allows us to verify Rust code directly, aligning with PDD Kit’s focus on integrating formal verification into existing Rust development workflows. Other proof languages (e.g., Lean, F*, Rocq) take different approaches to formal verification, each with its own tradeoffs. The techniques behind PDD Kit could help put them to work as well.

## Meet the authors

### Alex Lavaee

Research Software Engineer

### Matthai Philipose

Senior Principal Researcher

---

> 本文由AI自动翻译，原文链接：[Formally verifying agent-written full-stack web apps with PDD Kit - Microsoft Research](https://www.microsoft.com/en-us/research/blog/formally-verifying-agent-written-full-stack-web-apps-with-pdd-kit/)
> 
> 翻译时间：2026-11-10 09:31
