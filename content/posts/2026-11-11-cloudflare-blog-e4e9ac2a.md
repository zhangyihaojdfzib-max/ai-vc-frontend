---
title: Choosing QuePaxa, an unusualÂ consensus algorithm
title_original: Choosing QuePaxa, an unusualÂ consensus algorithm
date: '2026-11-11'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/choosing-quepaxa/
author: ''
summary: '[翻译失败，原文如下]


  Cloudflarerecently announcedMeerkat, an experimental distributed consensus service
  designed to manage our internal global control plane. ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-13T09:19:31.328927'
---

[翻译失败，原文如下]

Cloudflarerecently announcedMeerkat, an experimental distributed consensus service designed to manage our internal global control plane. It is powered by a new consensus algorithm published by researchers Tennage & BÄsescu et al. calledQuePaxa(2023).

QuePaxa is an unusual choice; most consensus systems use well-established consensus algorithms like Raft, (Multi-)Paxos or Viewstamped Replication. These algorithms are well understood, have mature implementations, and usually work well.

Unfortunately, common consensus algorithms often suffer in wide-area networks with volatile network connectivity and latency, i.e., networks like the Internet, which is where Meerkat runs. These algorithms rely on a singleleaderprocess being available and having predictable latency. If the leader goes down, experiences higher latency than usual, or is disconnected, the entire consensus system slows down or becomes unavailable until the leader is replaced. This is unacceptable for Meerkat.

Meerkatâs global deployment environment led us to a newer consensus algorithm, QuePaxa, which promises better stability despite volatility, in large part by not relying on a leader to make progress. In this post weâll explainÂ why we choseÂ QuePaxa and how the QuePaxa algorithm works.

## What weâre building and why itâs unique

Meerkat is a distributed system in which replicas agree upon an ordered log of events, where each event is decided by a consensus algorithm.

Consensus algorithms allow a group of machines to agree on a single shared truth, even if some of those machines crash or disconnect. Consensus algorithms provide an important guarantee: machines never decide conflicting values. This ensures Meerkat replicasâ logs never diverge.

Meerkat uses its consensus-powered log to expose applicationsÂlike a key-value store, where each entry in the log is agetÂ or aput. Because the consensus algorithm guarantees replicasâ logs never diverge, they all construct the same key-value (KV) state. Comparable consensus-powered systems include Consul, etcd, and Apache ZooKeeper.

Unlike similar systems, however, Meerkat was designed forglobal scale. A Meerkat cluster may be distributed across continents and connected by links that often exhibit high and variable latency. This is an unusual setup for consensus systems, which are usually deployed in smaller, more local networks, and havestrict latency requirements.

## The challenges of consensus at a global scale

While all consensus algorithms ensure that replicas agree on the same value, many of them become disproportionately unavailable or slow when network conditions degrade (but machines do not crash). We have seen this happen firsthand:Â in 2020, thepartialfailureÂ of a core Cloudflare network switch caused a consensus-powered system to degrade and the dashboard to operate 80x slower than usual, for six hours. Critically, the system lost no data. But it became unavailable for writes until the issue was resolved, which is unacceptable.

Ideally, a consensus algorithm should be able to make progress despite latency spikes and broken connections, not just replica failures. This is particularly a problem at global scale, where faults are more likely to originate in the network, and not our own servers.

Letâs examine two common traits of consensus algorithms that can lead to degradation under hostile network conditions: destructive interference and fault detection. Later, weâll see how QuePaxa sidesteps both of these issues.

### Destructive interference and leaders

Consider Paxos, the veritable grandfather of most consensus algorithms. A lot of consensus algorithms inherit the structure of Paxos â both the good and thenot-so-goodÂ bits.

Leaving an egregious amountÂof detail out, hereâs how Paxos works. There are two kinds of processes: proposers and acceptors. Abstractly, the goal of the system is for a majority of acceptors to agree on a value proposed bysomeproposer. There are two phases: thePrepareÂ phase, and theAcceptÂ phase. In thePrepareÂ phase, any proposer can send a ballot number out to a majority of acceptors.Â This ballot number serves as a promise â acceptors will only accept proposals with that ballot number or higher. Then, in theAcceptÂ phase, the proposer sends its proposal along with the ballot number to a majority of acceptors again. If a majority of acceptors still hold the ballot number of the proposal, the majority accepts it, and the proposer can safely decide the proposal.

![In the Prepare phase, a proposer sends a ballot numbered â1â to three acceptors. The three acceptors reply. Then, in the Accept phase, the proposer broadcasts its proposal to the three acceptors. The acceptors have not received any other ballot, and so they accept the proposal. They reply to the proposer with this information, and the proposer decides.](/images/posts/42938a6a19dc.jpg)

Challenges arise when two or more proposers submit proposals at the same time. Specifically, another proposer can interleave its own higher ballot number in between the two phases, blocking any lower ballots. Two proposers can repeatedly block each other from progressing â effectively competing for acceptance.

![There are two proposers: one red, and one blue. In the Prepare phase, the blue proposer sends a ballot numbered â1â to three acceptors. The three acceptors reply. Then, the red proposer, in its own Prepare phase, sends a ballot numbered â2â to the three acceptors, before the blue proposer can send its proposal in the Accept phase. Because the red proposer reached the three acceptors with a higher ballot number, the blue proposerâs proposal was rejected. The blue proposer then sends a new ballot numbered â3â to all three acceptors. The blue ballots arrive before the red proposer can send its proposal to the acceptors, and so the acceptors reject the red proposerâs proposal. This then continues forever.](/images/posts/946ddca44838.jpg)

When proposers compete and block each other in this way, we say that they destructively interfere. Destructive interference gets worse as more proposers propose their own ballots. The more concurrent proposers there are, the more likely it is that the system gets stuck repeatedly proposing. Even if none of the replicas have crashed or are unavailable, multiple proposers and misbehaving networks can block Paxos. Formally, we say that Paxos does not guarantee livenessÂ (i.e., that proposals are eventually decided) without assuming that, at some point, all messages arrive within a bounded amount of time â an assumption known as partial synchrony.

To avoid multiple proposers constantly competing, most deployed consensus algorithms, like Raft, Multi-Paxos, and Viewstamped Replication, add a specialÂleaderÂproposer. The leader is the only replica that can make proposals. Centralizing the proposing power in one replica forces an order on concurrent requests, avoids competing proposals, and has the added benefit of getting decisions done in an optimal single network round-trip, instead of two. While the leader is healthy and the network is well-behaved, leader-based protocols are fast.

![There is a single leader replica, wearing a crown, that is the only one allowed to send proposals to other servers, called âreplicasâ. All they do is accept the leaderâs proposal.](/images/posts/6730864cf18a.jpg)

The trade-off is that the leader must remain operational and reachable. When it fails, becomes too slow, or is disconnected from the cluster, the system stalls. The only solution is for the remaining replicas to detect that the leader has failed, and elect a new one in its place.

### When leader recovery is unstable

When a leader fails, the system must recover by electing a new one. Interestingly,Â leader recovery is often how destructive interference sneaks right back into a leader-based system.

[翻译失败，原文如下]

Consider Raft. For safety reasons, Raft elects a new leader using a majority vote. A replica that suspects that the leader has failed announces itself as a candidate for leadership and requests a vote from other replicas. If more than half of the replicas agree to vote for the candidate, it becomes the new leader. If they donât, then a new election is called, and the candidates try again.

Multiple replicas can become candidates â all they need to do is detect that the leader is down. The candidates may then all try to acquire a majority vote simultaneously. The problem is that the candidates willcompeteÂ for the majority vote, which means Raftâs elections suffer from the destructive interference we just saw in Paxos: two replicas can mutually prevent each other from getting support from a majority and becoming the leader. The more elections fail, the more replicas will try to get themselves elected leader.

![There is a greyed out leader that has crashed, and four other replicas. Two replicas are candidates for leadership, and are trying to acquire a majority of votes to become leader. They both need three votes, but they each have only acquired two votes (their own and another replicaâs). No candidate is elected.](/images/posts/6b26ede2dab1.jpg)

Even if the leader stops being faulty, elections continueÂ to disrupt what could have been normal system functioning. This is known as ametastable failure: a failure pattern that perpetuates itself even when the initial cause of failure is removed. A two-second network outage â or a momentarily faulty network switch â can make the leaderappearÂ to be faulty and force a leader election, which can fail, and force further elections.Â The outage will be over in two seconds, but the election can continue for much longer as candidates continue to block each other.

Ideally, consensus algorithms wouldnât need any recovery process, as they are complicated, prone to interference, and introduce another source of downtime.

### When fault detection goes awry

The problem of destructive interference in leader elections is compounded by trigger-happy fault-detection, especially in wide-area networks. In order for leader-based consensus algorithms to choose a new leader, replicas must firstdetectÂ that the leader has failed. However, if replicas detect leader-failures inaccurately, the system may spend an inordinate amount of time in recovery, not handling requests.

In a distributed system, where machines are separated over a network, fault detection will ultimately depend on expectations. A process cannot directly observe that a remote process has failed; it can only observe that an expected message has or hasnât arrived. We need a predictable pattern of communication, such as heartbeats or acknowledgements, to tell us that a machine is healthy. If an expected message does not arrive within the expected time, we suspect a fault. The difficulty lies in managing those expectations.

In real networks, especially wide-area networks, messages donâtalwaysÂ arrive when predicted. There is no guaranteed upper bound on the time that it takes for messages to arrive. Thatâs not to say that the network is slow, or that it is unreliable âmostÂ messages arrive within the time we expect them to. Instead, sudden bursts of latency and losses in connectivity can, momentarily, and without warning, increase the time it takes for any message to traverse the network. We call such networks asynchronous.

The big issue with asynchronous networks is that if some server doesnât reply in a given amount of time, we donât really know if the server has failed or if the network is just slow â the two are indistinguishable over the network. Any practical fault detectorhasÂ to make a guess based on how long it has been waiting compared to its expectation, and sometimes that guess will be wrong.

![A user is waiting for a response from a server. The response is taking a while. The user questions whether the network is slow, or if the server crashed.](/images/posts/55443b94b4a6.jpg)

In leader-based algorithms, that guess is exactly what triggers leader elections. Sometimes the leader is down; sometimes its messages are late, or the connection is silently broken. The protocol cannot know which one happened before it reacts. If the guess is wrong, and a replica thinks the leader is faulty when it actually isnât, then an election begins and the entire system mustÂstop.Until the leader is replaced, no progress is made â and as we just saw, that can take a while.

Fault detection is fundamentally error-prone in asynchronous networks, and when the detector makes a mistake, we get downtime.

### When fault detection is slow

Even when a fault detector guesses correctly, there are issues. Fault detectors reactÂto failures by observing messages on the network, and so their response time has to scale with network latency â the detectorâs timeout canât be below the network latency. This is why Raft is commonly deployed with an election timeout offive to ten times the network round-trip time.Â It has to be high enough to give a chance for the leader to signal that it is alive, and avoid falsely triggering elections. The election timeoutcanbe much lower than that, but since leader elections completely stop the system, timeouts are usually set conservatively high.

Roughly speaking, a round trip halfway across the world is measured in hundreds of milliseconds. If an election timeout is several round trips, detecting a failed coordinator can take around a second. Even when fault detection is completely accurate, it is slow, and it is slowest in high-latency global networks. Until the detector reacts, the system is down.

## Why QuePaxa is the right fit

We realized that any algorithm relying on a strict leader or accurate timeouts was inevitably going to stall in a consensus system that runs over the Internet. We searched for consensus algorithms designed for asynchronous environments â protocols that didn't rely on a well-behaved network or precise timing to function. This led us toQuePaxa, published in 2023 by Tennage & BÄsescu et al.

The most notable thing about QuePaxa is how it can efficiently reach consensus in a single round trip under favorable network conditions, but also gracefully degrades performance during latency spikes, connectivity issues, and server failures. QuePaxa achieves this by solving the exact problems we just discussed through three key design choices: having anoptionalÂ leader, completely removing the reliance on fault detection, and designing forconstructive interferenceÂ between proposers.

In QuePaxa, much like in Paxos, there are two roles:proposersandrecorders. Proposers submit proposals to be decided on, and recorders serve as intermediaries between proposers, recording every proposal they see.

![Two proposers, one blue and the other red, are opposite each other, separated by three servers labeled âRecorderâ. Each proposer sends messages to each recorder.](/images/posts/3c2c7a37c96c.jpg)

Instead of having proposers compete to get their own proposals decided, in QuePaxa, proposers will cooperatively work towards a proposal that everyone supports. QuePaxa does this by assigning apriorityto proposals, in the form of a random number. The optional leader gets an exclusive maximum priority. During execution, proposers submit their proposals to the recorders, who propagate the proposal to other active proposers. When proposers receive a proposal from a recorder with a higher priority than theirs, they adopt the new proposal as their own, i.e., begin broadcasting the higher priority proposal instead. In general, proposers in QuePaxa work together to decide on the highest priority proposal that they collectively know. This means proposers canât lock each other out of deciding on a proposal, indefinitely.

[翻译失败，原文如下]

![Two proposers, one blue and the other red, are opposite each other, separated by a single recorder. The blue recorder proposes a proposal with priority â2â. The recorder records the blue proposal and replies to the blue recorder, with the same blue proposal. Then, the red proposer sends a proposal with priority â1â to the recorder. The recorder replies to the red proposer with the higher priority blue proposal. The red proposer, upon receiving the reply adopts the blue proposal with priority â2â as its new proposal.](/images/posts/8e8602711370.jpg)

The caveat is that it might not be possible to spread proposals around well enough to agree on a proposal, and so proposers have to try again, with each attempt constitutingÂ around. However, as more proposers submit proposals, the more likely they are to converge on the highest priority proposal. This is what makes QuePaxa a randomized algorithm: the randomly generated priorities of non-leader proposers are likely â but not guaranteed â to lead to consensus on thehighestÂknownpriority, in a round. Yet, given enough rounds, it is guaranteed that proposers agree on a proposal.

One proposer is designated the leader. The leader is the only proposer capable of deciding in a single round trip. The leader always proposes with the highest priority; if the leader knows it spreadÂ its proposal before any other proposer, then it can decide immediately. Clients arenât forced to make requests to the leader â any proposer can propose. If the leader goes down, then clients can keep making requests to other proposers. The leader iscompletely optional. The leader is simply more likely to decide, than any other proposer, and do so faster, in a single round trip.

However, because the leader is the only one that can decide in a single round trip, we want to use it whenever possible. To exploit thisfast pathÂ without creating a single point of failure, clients sending proposals to the systemhedgeÂ their bets: they send their requests for proposals toeveryÂ replica, and the non-leader replicas will wait for a small timeout, so the leader can propose and decide on its own. In our own implementation of QuePaxa, we actually deviate from the paper and have clients wait the hedge timeout instead of the replicas, to reduce the amount of messages we send over the network, but the overall result is the same.

Thishedging timeoutÂ is very different from the timeouts used in Raft or Multi-Paxos. It isnotÂ fault detection, and so isnât constrained by network latency; it is locally determined by replicas and can be as small as they want it to be.Â In Raft, having a five-millisecond timeout in a network with 100-millisecond latency would completely freeze the system. But in QuePaxa, a five-millisecond hedge timeout only increases the number of active proposers.

However, hedging isnât free: the more proposers there are, the more proposals get broadcast, and the more likely it is that replicas fail to decide in a round. Instead, hedging provides a tradeoff: we can react faster to leader changes by lowering the hedge timeout, but we incur extra bandwidth costs and may take more time to decide.Â Thatâs a tradeoff we're more than willing to make.

If the QuePaxa leader goes down, we can recoverÂ as fast as we want âÂ weâre not bound by network latency.Â This is how QuePaxa gets around fault detection: sinceanyonecan propose, not just the leader, QuePaxa can proactively deal with leader failures by hedging, rather than reacting to failures.

### How QuePaxa works under the hood

To understand how QuePaxa gives us all of these nice properties, letâs look at how QuePaxa actually works. Â

QuePaxa works in rounds made up of four phases. If a proposal hasnât been decided on in the last phase, a newroundÂ is started, and QuePaxa starts over. At the start of each phase, proposers broadcast their currently adopted proposal to all recorders. Once a proposer receives a reply from a majority of recorders, they advance to the next phase. Hereâs the general outline of the phases:

- Phase 0 (Propose and Adopt):Â Proposers randomly select a priority, send their proposals to recorders, and adopt the highest-priority proposal they receive from a majority of recorders. If itâs the first round and the leader knows its proposal reached a majority of recorders first, the leader decides immediately.
- Phase 1 (Spread):Â Proposers spread their adopted proposal to a majority of recorders.
- Phase 2 (Check and Decide):Â Proposers ask a majority of recorders for the highest-priority proposal seen in the previous phase. If it matches their own adopted proposal, they decide on it.
- Phase 3 (Carry Forward):Â Any proposer that failed to decide prepares for the next round by adopting the best proposal they see from a majority of recorders.

Letâs walk through a couple of example executions and unpack how each phase contributes to the overall behavior we want out of QuePaxa. Each execution will have two proposers (one of which is the leader) and three recorders.

The Leader Fast PathÂ(Phase 0):The first phase does three important things: it randomizes prioritiesÂ (which itmustÂ do to circumventthe FLP impossibility theorem), checks if the leader reached a majority of support first, and helps proposers converge if the leader didn't. The leaderâs proposal is not randomized, and will always have the highest possible priority.

![The image shows a message passing diagram, where time progresses from left to right. There are five lanes. At the leftmost side of the diagram, there are, ordered vertically: a blue server with a crown, labelled âLeaderâ, with a blue ribbon attached to it, and an infinity sign at the center of the ribbon; three violet servers with a pen and paper, each labelled âRecorderâ; a red server (with no crown), with a red ribbon attached to it, and a 1 at the center of the ribbon. The blue leader and the red proposer both broadcast their current proposal to every recorder. The recorders record and reply with the first proposal they receive. The leader reaches the first and second recorder first, while the red proposer reaches the third recorder first. The leader receives a majority (2) of replies each carrying the leaderâs proposal. The leader sees that all proposals in the majority are its own and decides. The red proposer receives a majority (2) of the recorderâs replies, from the second and third recorders, who replied with the leaderâs proposal and the red proposerâs proposal, respectively. The red proposer adopts the leaderâs proposal, since it is the one with maximum priority in the majority it received.](/images/posts/da148108b541.jpg)

In the example above, the leader's proposal reaches a majority of recorders before anyone else, and receives replies confirming it. The leader can safely decide right away. This might seem dangerous, but it is entirely safe thanks to a property calledmajority intersection: any two majorities of recorders always share at least one recorder. Because the leader reached a majority, any other proposer querying a majority will inevitably encounter the leader's proposal and adopt it. Since the leaderâs proposal has the highest priority, any other proposer will adopt the leaderâs proposal. It is impossible to decide on any other proposal.

Concurrent Slow Path (Phases 0-3): When there are concurrent proposers, however, it is not guaranteed that the leader will immediately decide. The leader might fail to reach a majority of recorders first, or it might receive a single reply supporting another proposer. Let's look at what happens when another proposer contests the leader.

[翻译失败，原文如下]

Phase 0:Â Pictured below, a second proposer(shown in red)Â reaches the second and third recorders first. The fast path is blocked. Instead of competing, proposers adopt the highest-priority proposal they receive from a majority and move to the second phase. The two proposerscouldÂ both converge to the leaderâs proposal in this phase. For illustrative purposes, our example will prevent convergence by delaying the leaderâs messages. Â

![The blue leader proposer and the red proposer both broadcast their current proposal to every recorder. The recorders record and reply with the first proposal they receive. The leader reaches the first recorder first, while the red proposer reaches the second and third recorders first. The leader receives a majority (2) of replies, containing its own maximum priority proposal and the red proposerâs proposal with priority 1. The leader adopts the proposal with the greatest priority which is its own. The red proposer receives a majority (2) of the recorderâs replies, from the second and third recorders, both containing the red proposerâs proposal. The red proposer adopts its own proposal, since it is the one with maximum priority in the majority it received. The reply from the third recorder arrives late, not in the majority, so it isnât considered for adoption.](/images/posts/0dd878a85436.jpg)

Phase 1:Â Proposers spread the proposalthey just adoptedÂ in Phase 0 to a majority of recorders. The recorders keep track of the highest-priority proposal they observe. It is a simple but critical step: it prevents the protocol from later deciding on a lower-priority proposal. This is once again thanks to majority intersection: any majority queried in the following phase must include at least one recorder that saw the adopted proposal, in this phase. For illustrative purposes, we prevent convergence in this phase by delaying the leaderâs message to the third recorder, so the recorder does not adopt the leaderâs proposal.

![The blue leader proposer and the red proposer both broadcast their current proposal to every recorder. The leaderâs message to the third recorder is lost and never reaches the recorder. The first and second recorder each receive the leaderâs proposal, with maximum priority, and the red proposerâs proposal, with priority 1. The third recorder only receives the red proposerâs proposal. Each recorder records the proposal with highest priority for the next phase. The first and second recorder record the leaderâs proposal, while the third recorder records the red proposerâs proposal.](/images/posts/d245f6e1c591.jpg)

Phase 2:Â Now, a decision can happen. Each proposer determines if a higher-priority proposal gained enough support to overtake its own by asking a majority of recorders for the highest-priority proposal observed duringÂ Phase 1. If the highest proposal returned is still their adopted proposal, they decide. In our diagram, the leader sees its own proposal returned by a majority and safely decides. The other proposer receives conflicting summaries, so it cannot decide yet.Â Like in Phase 1, recorders keep track of the highest priority proposal they received.

![The blue leader and the red proposer both broadcast their current proposal to every recorder. The first two recorders recorded the leaderâs proposal with maximum priority in the previous phase, while the third and final recorder recorded the red proposerâs proposal, with priority 1. Each recorder replies to the proposers with the proposal that the recorder has adopted. The leader receives a majority (2) of replies from the recorders, each carrying its proposal. Of that majority, the proposal with the maximum priority is its own, so it decides it. The red proposer receives a majority (2) of replies from the recorders, one carrying the red proposerâs proposal, and another carrying the leaderâs proposal. Of those two, the proposer's own proposal does not have the greater priority, so the red proposer cannot decide, and progresses to the next phase.](/images/posts/c37b8a0aea16.jpg)

Phase 3:Â If a proposer doesnât decide in Phase 2, it moves to the final cleanup phase to prepare for the next round. Proposers spread their proposals again and adopt the best they find among a majority of recorders. Here, the remaining proposer discovers the decided proposal and adopts it, heading into the next round.

![The red proposer fetches the recorded proposals at each recorder, all of which are the leader proposal with maximum priority. When the proposer receives a majority (2) of the replies, it adopts the proposal with the maximum value, which is the leaderâs proposal.](/images/posts/8bcdb8e9d448.jpg)

This is deliberate â if there was some decision in the previous phase, then a majority of the recorders will have that proposal, and any remaining proposersare guaranteedto adopt it. We see here another instance of cooperation between proposers â even when a round fails, proposers try to converge on the same proposal heading into the next round.

Moving to the next round:Â After the fourth phase, proposers move on to the next round. At this point, there is no more leader fast path, and the only way to decide is by converging in the third phase. Importantly, due to proposal adoption, it becomes exponentially easier to decide as rounds progress. The QuePaxa paper predicts that each round has a 50% chance of deciding, but in practice, that probability is much higher, thanks to convergence.

Putting all four phases together, we can see where QuePaxa gets its resilience. The first phase gives the leader its one-round-trip fast path. If that fast path fails, random priorities and proposal adoption help proposers converge instead of compete. The second and third phases make it safe to decide, thanks to majority intersection, while the fourth carries what proposers learned into the next round, in case proposers donât decide.

No proposer has to detect that the leader has failed before making progress, and a failed round doesnât throw away the work already done. When the network behaves, QuePaxa is fast. When it doesnât, QuePaxa keeps moving.

## How QuePaxa makes Meerkat possible

In our own evaluations of Meerkat, where we had servers spanning nearly all continents, weâve directly experienced the impact that QuePaxa has on the overall performance and availability of the system. Meerkat continuously processes requests, even when the leader crashes, disconnects, or just becomes slow. At no point have we ever seen it completely stall. This is exactly what we wanted.

The rate at which Meerkat handles requests has also been generally predictable. Most decisions â upwards of 95% â are made by the leader in the first phase, which keeps our throughput fairly stable. In the instances where a decision isn't reached in the first phase, the throughput drops momentarily, down to at most a third of the usual rate, signaling that three round trips â so three phases â were needed to decide instead of just one. The system slows down, but does not grind to a halt.

QuePaxa also allows us to confidently switch out which replica acts as leader while the cluster is running. Since the leader isnât the exclusive driver behind decisions and proposers are cooperative, a temporarily non-optimal leader isnât as limiting as in other algorithms, where a leader misconfigurationÂ could stall the system completely. We can dynamically tune which proposer is the leader without worrying too much about impacting the stability of a Meerkat cluster.

## What weâll be showing next

Designing Meerkat for a global network forced us to re-evaluate how we approach distributed consensus. Instead of sticking to familiar defaults that didn't quite fit our constraints, we looked to the decades of research produced by academia and industry. That search led us to QuePaxa.

[翻译失败，原文如下]

Choosing QuePaxa meant choosing a less-traveled path. It has not been battle-tested as extensively as Raft or Paxos, and weâre also extending the original crash-stop design to support crashrecovery. This demands careful engineering and stronger evidence of correctness than usual systems.

That is why we are formally verifying our QuePaxa implementation and Meerkat as a whole, alongside extensive simulation and fault-injection testing. Future posts in this series will explain how we verify Meerkat and QuePaxaâs Rust implementation, how we test failures that are difficult to reproduce in production, benchmarks, and what we have learned while turning an academic protocol into a production system.

Stay on the lookout for further Meerkat updates on the Cloudflare Blog, and if you want to learn more about research at Cloudflare, have a look at our work atCloudflare Research.

## Related tags

Follow on Social Media

- Cloudflare
- James Larisch

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Choosing QuePaxa, an unusualÂ consensus algorithm](https://blog.cloudflare.com/choosing-quepaxa/)
> 
> 翻译时间：2026-11-13 09:19
