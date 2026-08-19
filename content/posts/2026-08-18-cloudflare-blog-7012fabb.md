---
title: 'BGP Role model: tracking the adoption of RFC 9234'
title_original: 'BGP Role model: tracking the adoption of RFC 9234'
date: '2026-08-18'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/rfc9234-bgp-role-model/
author: ''
summary: '[翻译失败，原文如下]


  Route leakspush traffic down paths it was never meant to take. We havewrittenandspokenpublicly
  in thepastabout route leaks inBorder Gatew...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-19T03:07:52.087215'
---

[翻译失败，原文如下]

Route leakspush traffic down paths it was never meant to take. We havewrittenandspokenpublicly in thepastabout route leaks inBorder Gateway Protocol (BGP), depicting these events as impactful incidents that cause misdirection of traffic through unintended network paths. BGP routing is driven by therelationshipsbetween Autonomous Systems (ASes), i.e., customer-provider and peer-peer. Customers pay providers for access to the rest of the Internet, while peers exchange traffic with one another typically under a âsettlement-freeâ arrangement where no money changes hands. These relationships help define routing rules that form plausible paths. For example, the rules form a âvalley-freeâ hierarchy of how routes should propagate: a route learned from a provider or a peer should be announced only downward to customers, never back up to another provider or peer. Rules like this express an intent or expectation about Internet routes. A route leak is what happens when that intent is violated.

Historically, each network has had to implement this intent on its own, usingcomplex, error-prone routing policies. RFC 9234 (Route Leak Prevention and Detection Using Roles in UPDATE and OPEN Messages) simplifies this by expressing intent within the protocol itself. It introduces a new âBGP Roleâcapability, which requires that two BGP neighbors agree on their relationship when the session comes up, and an âOnly to Customerâ (OTC) path attribute, which marks routes that must not propagate beyond customers. A router that understands OTC can reject a leaked route on its own, without an operator-written policy.

We set out to evaluate how well RFC 9234 works on the Internet and how widely it has been adopted. Relying on our globalpeeringpresence, we developed a unique method for tracking the adoption of BGP Role configurations by monitoring which peer ASes send the OTC attribute to Cloudflare. Along the way we found something we did not expect: two largeTier-1 networksstripthe OTC attribute from routes they forward. We have been engaging with these Tier-1s to allow OTC attribute propagation through their networks, which aids in enabling route leak prevention capabilities for early adopters of RFC 9234. Below, we walk through our analysis, why the OTC stripping matters, and how to enable BGP Roles in your own network.

## Route leak prevention using BGP Roles and the OTC attribute

Before the measurements, letâs talk about how BGP Roles and the OTC attribute actually work.

### Route leaks

Route leaks are the âpropagation of routing announcements beyond their intended scope,â as defined inRFC 7908. The intended scope is determined by AS relationships: provider-to-customer or peer-to-peer.

Therulesare asymmetric, and it comes down to direction. Routes propagate freely downward: a provider may hand a customer anything in its table. Propagating routes upward or sideways is restricted to âlocalâ information. Specifically, an AS may send in the upwards or sideways directions only the routes it originates and that are learned from its own customers.

The figure below shows what B does with a route it learns from A, depending on Aâs relationship to B.

Putting it simply, a route leak happens when an AS takes a route learned from a provider or a peer and announces it to another provider or peer. The route travels down the hierarchy and then back up, creating a âvalleyâ in the hierarchy that the underlying relationships never authorized. Routing paths are required to bevalley-free.Â

Violations of the valley-free property come in many forms. A common shape is a customer announcing a route between two of its providers, also known as ahairpin turn.

This scenario is bad for everyone: the customer (AS64504) is not being paid to send traffic between its providers, and it also may nothave the capacity to absorb the trafficflowing between the two upstream networks, resulting in increased latency or drops.

Route leaks impact everyone, and they happenoften. Thatâs why we built theCloudflare Radar route leak detection systemto help track routing anomalies continuously. However, despite the frequency and the impact, existing defenses put the burden on network operators who must rely on prefix filters andIRR-derivedpolicies. Such mechanisms require every AS to express its own relationships correctly,by hand, on every session. RFC 9234 moves that burden into the BGP routing protocol.

### BGP Roles

ABGP Roledeclares where you sit relative to a neighbor on the given eBGP (External BGP) session. The Role describes each side of the neighbor relationship: on a session with your transit provider, you configure the Rolecustomer, and they configure the Roleprovider.

There are five options: Provider, Customer, Peer, RS, and RS-Client. The first three are the transit and lateral-peering relationships described above. RS and RS-Client involveInternet Exchange(IX)route servers, where a route server acts like a provider to all of its clients, re-announcing prefixes between IX members transparently.

Only five pairings of the five roles are valid:

Local AS Role

Remote AS Role

Provider

Customer

RS-Client

RFC 9234 states a Role should be configured at the local AS on every eBGP session. During partial deployment, most sessions will have a Role on one side only. RFC 9234 handles that by default: if you send the Role capability and your neighbor does not, the session still comes up, and your locally configured Role still drives partial route leak prevention. An operator who wants a stronger guarantee can enable "strict mode," which rejects any session where the neighbor sends no Role capability. Strict mode is opt-in, and as the adoption numbers later in this post show, it is not yet realistic for most networks.

When both sides send a Role and the pair is not one of the five above (e.g., one end says customer and the other says peer), the session is rejected with a Role Mismatch notification (code 2, subcode 11).

The rejection is one reason Roles are so useful: a Role mismatch means the two networks disagree about what their relationship actually is, which is precisely the kind of latent misunderstanding that surfaces later as a route leak. A Role mismatch fails the handshake instead of failing later as an incident.

No single Role is able to describe multiple roles, for example, if you hold more than one relationship with the same neighbor over a single session (e.g., provider-to-customer for some prefixes, peer-to-peer for others). RFC 9234 says Roles must not be configured on such a session at all. Instead, networks need to split theComplex relationshipinto separate eBGP sessions with normal relationships, and configure the relevant Role on each. Without individual sessions that are assigned Roles, a network operator must implement a more complicated per-prefix policy with no in-band way to check that the policy is correct â which falls back to the failure-prone âby-handâ mechanisms that motivate Roles in the first place.

Roles have a second use beyond session negotiation. In our earlier post onASPA validation, we described how a different algorithm applies to paths received from a provider than to paths received from a peer, customer, route server, or route server client. Routes from a provider may contain a full upward, sideways, and downward motion in the path. However, routes from a non-provider must only contain a downward-facing ramp to customer ASes.Â

The BGP Role is what tells the router which of the two to run, so BGP Roles and ASPA should be configuredtogetheron routers that support both.

### The Only to Customer (OTC) attributeÂ

[翻译失败，原文如下]

OTCis an optional transitivepath attribute(type code 35) carrying one value, an AS number. That value records the AS that first sent the route sideways or downward. It marks the peak of the path, after which the route may only continue down. Once OTC has been set, RFC 9234 requires it to be preserved unchanged. And because the attribute isoptional transitive, even a router with no RFC 9234 support is expected to pass it along rather than discard it. Both of those facts matter later.

Your Role on each session decideswhich rules apply.

Setting OTC. A route is stamped the first time it stops travelling strictly upward:

- If announcing to a customer, a peer, or an RS-client with no OTC present, then attach OTC carryingyour ownASN;
- If receiving from a provider, a peer, or an RS with no OTC present, then attach OTC yourself, carryingtheirASN.

Checking OTC. Once a route carries OTC, it may only travel downward:

- Never announce an OTC-carrying route to a provider, a peer, or an RS;
- An OTC-carrying route arriving from a customer or an RS-client is a leak, so reject it;
- An OTC-carrying route arriving from a peer with any value other than that peer's own ASN is a leak, so reject it.

As a concrete example, letâs return to the hairpin leak, but add Roles and OTC. AS64502 announces the route to its peer AS64503, attaching OTC=64502 on the way out. AS64503 passes it further down to its own customer AS64504, while leaving OTC untouched because it is already present. AS64504 then unintentionally violates the intended BGP relationships, by announcing the route to its other provider.

OTC has two opportunities to stop the leak. If AS64504 is compliant, it must not announce an OTC-carrying route to a provider at all, and the leak never leaves. If AS64504 is not compliant, as shown in the above example, the receiving provider sees a route arriving from a customer with OTC attached, which RFC 9234 defines as a leak, and marks it ineligible. Either alone is enough.

In summary, configure a Role on eBGP sessions, and you automatically get route leak protection in BGP.Â

## Tracking adoption of RFC 9234 is challengingÂ

### Who is setting OTC?

As mentioned above, RFC 9234 outlines the rules for setting OTC both on egress and ingress routes. In an ideal world with complete (and correct) deployment, egress OTC attachment is enough. However, in the case of partial deployment or misconfigurations, ingress stamping by the receiving RS-Client, Customer or Peer fills in the missing OTC value. Quoting the relevant rule ofRFC 9234 section 5directly:

While this double-sided OTC attachment serves to tag as many routes as possible, it also obfuscateswhohas set the OTC value. For example, by observing the path64506 64507with OTC=64507, we cannot infer whether AS64507 set the OTC on egress or AS64506 set its missing value on ingress.

This makes identifying adopters of RFC 9234 by tracking OTC difficult, but is important enough for us to try.

### Using public BGP data

With this limitation in mind, we first attempted to detect which ASes are setting the OTC value by analyzing the Routing Information Base (RIB) dumps of all public BGP collectors fromRouteViewsandRIPE RIS. While naively counting the distinct OTC values gives us 361 potential setter ASes, this number is inflated by ASesfilling in missing valuesfrom their peers, providers, and, less frequently, RSes. To account for this, our first step was to count the number of OTC values that were equal to the first AS of the AS_PATH. Those ASes set the OTC attribute towards the route collectors which capture theraw receivedBGP messages. This step gives us an initial number of nine setter ASes.Â

Extending this analysis to detect if OTC was set on egress or on ingress in the AS_PATH requires using multiple guards to differentiate. We started with a simple and relaxed method to estimate the ASes potentially setting the OTC. We looked at all the AS_PATHs with an OTC value, and collected all the edges(ASX ASZ)where OTC = ASZ. Then, based on these edges we created two mappings,downstream: ASNânext_hops andupstream: ASNâprevious_hops. For example, in the case of(ASX ASZ), we would addASXtodownstream(ASZ)andASZtoupstream(ASX). As a next step, we want to remove from both sides the ASes that with higher confidence are setting OTC on the other side. For that, we collect all the ASesYthat have |downstream(Y)| â¥ 10 or |upstream(Y)| â¥ 10, and then remove them from the previous_hops or next_hops respectively.

As a final step, out of those two mappings we kept the ASes with at least three next or previous hops, and found 18 ASes potentially setting OTC and 20 ASes potentially filling in missing OTC values in the ingress. Combining these results with the ones from direct peer ASes, we find only 36 ASes that arepotentiallyRFC 9234-compliant, although the true number needs further investigation.

We understand that for the sake of certainty this method may miss ASes that have very few downstreams or upstreams. We are already looking at improvements. For example, AS_PATHs missing the OTC value may be negative evidence for an ASnotsetting OTC. In this approach, knowledge of the relationships between the ASes is necessary to focus only on instances where OTC should be set, i.e., not in upstream direction. However, getting accurate AS relationships has been a hard problem for over two decades, but multiple efforts exist that may be helpful such asCAIDAâsandBGPKITâsAS Relationships datasets. Public data is invaluable, even with inherent shortcomings.

We decided to supplement the view of RFC 9234 compliance by devising experiments conducted using Cloudflareâs network, in service of and spirit of an open and public Internet.Â

### Using Cloudflareâs global peering

Cloudflare, withthousands of peersand anopen peering policy, can help track who has implemented RFC 9234. As we described before, the core challenge is how to confidently differentiate whether OTC was set on egress or on ingress. Since Cloudflare peers directly with many ASes, we can assess their RFC 9234 compliance directly, without the ambiguity introduced by intermediate ASes.

Our methodology issimpleandconcrete: we use ourBMP(BGP Monitoring Protocol) feeds from our routers at Cloudflare to monitor OTC that we receive from our peers. We check if the OTC value is equal to the peer ASN. We processed our BMP data over the past three months and found 67 ASes that set the OTC attribute. In the figure below, we show a distribution of the network types of those ASes according toPeeringDBwith some manual corrections.

Two features of the pie chart stand out. First, we observe how Route Servers are more likely to quickly adopt new solutions such as RFC 9234 withYYCIX being the first to deploy it, partially due to the use of open-source BGP implementations that introduce new features much faster. This is very important as Route Servers play a critical role in the public Internet; they sit in the path of propagation of numerous routes and, by adding the appropriate OTC value, help protect a significant part of the Internet. We hope to see more and more RSes following this example. Second, the proportion of compliant ASes owned by individuals features highly. One explanation may be personal inclinations to use open-source BGP implementations.

Shown below is our current view of RFC 9234 adoption by observing OTC from peers over the past three months.

Looking ahead, we will keep a close eye on the adoption of RFC 9234 by tracking OTC, and plan to release this data publicly in Cloudflare RadarâsRouting sectionin the near future. In the meantime, we wondered which networks may unexpectedlystripthe OTC attribute.

## Experiment to find ASes stripping OTC

According to RFC 9234, OTC is an optional transitive attribute.Section 5 of RFC 4271states the following about handling optional transitive attributes:

[翻译失败，原文如下]

BeforeRFC 7606, the propagation of a malformed transitive attribute would remotely trigger multiple session resets, and cause outages far away from the AS that originated the announcement. This makes sense since, if a BGP speaker received a BGP UPDATE with a malformed attribute, it would reset its session with the neighbor that sent the message. Thisvulnerabilitymotivated some operators to start dropping unrecognized attributes, even if transitive, in order to minimize the impact of such a misconfiguration or an attack. There was even arecent issuewhere a malformed OTC attribute caused session resets in some BGP implementations. RFC 7606 addressed this risk by defining finer-grained error-handling where an announcement with a malformed optional attribute would cause to "treat-as-withdraw" the prefixes in it, while the session is preserved.

Propagating OTC even if unrecognized is vital for RFC 9234-compliant ASes that are multiple hops away to detect and prevent route-leaks. In early partial deployment stages, central or top-tier ASes bear the responsibility of adopting such routing security solutions, or at least not compromising their effectiveness by stripping essential attributes.Â

We wanted to study who is stripping the OTC attribute on the Internet. In our experiment, we announced one IPv4 and one IPv6 prefix, with attachedOTC = 13335, from all of our peering locations using BGPAnycast. After confirming global propagation, we later withdrew the prefixes to trigger thepath huntingprocess, revealing more paths to the test prefixes, giving us more opportunities to spot OTC-absent paths. As shown in the figure below, we used theBGPKITtoolkit to parse the Update messages from the Multi-threaded Routing Toolkit (MRT) dumps of all the public BGP collectors fromRIPE RISandRouteViews, and the local BMP data that we collect from our routers. Note that we opted to analyze the Updates instead of the Routing Information Base (RIB) dumps, which are snapshots of the routing tables of the peer ASes, to retrieve as many routes as possible both during the announcement and the withdrawal phase.

First, we focused on the AS_PATHs in the formatASX AS13335. If that path does not carry an OTC value,ASXmust have stripped the attribute. With this first step, we found six ASes dropping OTC, out of which two were Tier-1 ASes,AS3257(GTT) andAS1299(Arelion). Moving forward, we iteratively looked at longer paths to build two distinct sets of ASes preserving the OTC value and ASes dropping it:

1. We seed ourtrustedset(T)with AS13335.Tholds all the ASes that propagate the OTC.
2. For each AS_PATH:Filter out all ASes inT.If only one AS remains, we can attribute the presence or absence of the OTC to that AS. We record the mappingAS â OTC(s).
3. For each pairAS â OTC(s):IfOTC(s) == 13335, we add AS toT.Else if OTC is absent, we add AS toD(roppers).
4. IfTwas updated in 3, repeat the procedure from 2.

1. Filter out all ASes inT.
2. If only one AS remains, we can attribute the presence or absence of the OTC to that AS. We record the mappingAS â OTC(s).

1. IfOTC(s) == 13335, we add AS toT.
2. Else if OTC is absent, we add AS toD(roppers).

### Where was OTC being stripped?

Our methodology yielded nine more ASes that are dropping the OTC value. Additionally, we counted the number of distinct AS_PATHs that carried no OTC and found that33.1%of routes for IPv4 and17%for IPv6 had their OTC attribute dropped. This means that despite the possibly small number of ASes scrubbing OTC, almost one out of three AS_PATHs in IPv4 had its OTC stripped.

We first focused on the impact of two Tier-1 ASes, AS1299 and AS3257, due to their prominent position on the Internet. In the figure below, we show the proportion of OTC-absent AS_PATHs that included either or both of the two Tier-1s. Together, they appear in 96.6% of IPv4 and 92.9% of IPv6 OTC-absent paths, though Arelion accounts for thevastmajority of these instances.

Additionally, when we concentrated on the AS_PATHs where the next hop of AS13335 is either of those two Tier-1s, we observed that while GTT was consistently dropping the OTC attribute, Arelion had 71.4% in IPv4 and 40.7% in IPv6 of those AS_PATHs without an OTC. This meant that Arelion inconsistently dropped the OTC across their network. These findings highlight the critical role high-tier ASes play in the deployment of RFC 9234.Â

We contacted both GTT (AS3257) and Arelion (AS1299) with our research findings, and they confirmed they were indeed stripping the OTC attribute as a part of defensive practices followingBGP error-handling incidentsof the past.

Current configurations at GTT (AS3257) still result in the OTC attribute being removed. This will continue to hinder the effectiveness of RFC 9234 against route leaks propagating through AS3257 until they preserve the OTC attribute and/or configure BGP Roles on their routers.

In the case of Arelion, it appears they rolled out configurations to begin preserving the OTC attribute soon after our conversation. We can verify that OTC is no longer missing from paths through AS1299 with our experiment prefixes usingmonocle. Here is an example query:

```
â  ~ monocle search -D rib \
  --start-ts "2026-08-18T00:44:00Z" \
  --end-ts "2026-08-18T03:44:00Z" \
  -p 8.44.61.0/24 \
  -a '^1299 13335$' \
  --collector route-views4 \
  -f type,timestamp,peer_asn,prefix,as_path,only-to-customer \
  --json
{
  "as_path": "1299 13335",
  "only_to_customer": 13335,
  "peer_asn": 1299,
  "prefix": "8.44.61.0/24",
  "timestamp": 1787017771.0,
  "type": "ANNOUNCE"
}
```

We are very excited that our research hasalreadyresulted in better effectiveness for route leak prevention using the OTC attribute.

## Configure BGP Roles in your network

The BGP Role configuration and OTC attribute are critical building blocks for preventing route leaks from propagating and causing major incidents. The table below lists the BGP implementations that already support these configurations or have planned to support RFC 9234 soon as of August 2026:

BGP Implementation

RFC 9234 support

Cisco IOS XR

Coming in 26.4.1 release

Junos OS / Junos OS Evolved

Arista EOS

Nokia SR OS

Huawei

Extreme SLX-OS

RouterOS

OpenBGPD

ArcOS

GoBGP

ExaBGP

If your routing vendor already supports RFC 9234, we recommend that you configure Roles now to start preventing route leaks. Keep in mind the rollout will need to be completed during maintenance windows, as BGP sessions will need to be reset upon applying Roles. At Cloudflare, we have already started our gradual deployment of RFC 9234 configurations across our global fleet of routers.

Compared to complex routing policy configurations, route leak prevention provided by the Only to Customer attribute isautomaticonce the Roles are applied.Â

If your vendor does not yet support RFC 9234, we encourage you to reach out to them and ask for support, so you can prevent your network from spreading or initiating leaks as soon as possible.

## Related tags

Follow on Social Media

- Cloudflare
- Bryton Herdes
- Iliana Xygkou
- Mingwei Zhang

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[BGP Role model: tracking the adoption of RFC 9234](https://blog.cloudflare.com/rfc9234-bgp-role-model/)
> 
> 翻译时间：2026-08-19 03:07
