---
title: BringingÂ post-quantum cryptography to geographically fenced key management
title_original: BringingÂ post-quantum cryptography to geographically fenced key management
date: '2026-10-23'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/post-quantum-geo-key-manager/
author: ''
summary: '[翻译失败，原文如下]


  Today, Cloudflare is launching a post-quantum geographically restricted key manager
  in support of our Data Localization Suite (DLS) in cl...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-24T07:04:49.673326'
---

[翻译失败，原文如下]

Today, Cloudflare is launching a post-quantum geographically restricted key manager in support of our Data Localization Suite (DLS) in closed beta. This new PQ GeoKey Manager is a cornerstone of Cloudflareâs data sovereignty solutions, making sure that a customer's decryption keys are only accessible in their chosen geography. GeoKey Manager implements this by wrapping each decryption key such that it can only be decrypted by Cloudflare servers that are located in the allowed geography.

While general availability (GA) is planned for Q1 2027, todayâs launch is an important milestone on our journey to support our customersâ data sovereignty goals while also migrating all Cloudflare products topost-quantum (PQ) cryptography.

Governments, financial institutions, healthcare providers, and defense organizations process highly sensitive data that can remain sensitive for years or decades after it is produced. Encryption is often required to protect this data. When classical, public-key encryption is used, adversaries do not immediately need a quantum computer today to put that data at risk: they can store the ciphertext and retain them until quantum computers can break the public key cryptography protecting it â an attack strategy known as harvest now, decrypt later.

For organizations with geographic requirements, resisting that threat is only half the challenge. At Cloudflare's scale, high availability requires replicating customer data across many servers across our global network. However, many data sovereignty regulations require that certain types of data be processed only within a given geographical region. We must therefore ensure the data is end-to-end encrypted such that only servers within the region have access to the plaintext. In this post, we describe the system that makes this work.

## The evolution of GeoKey Manager

Cloudflare pioneered the concept of geo-restricted transport layer security (TLS) keys back in 2017 withGeoKey Manager. This gave customers control over the locations where their private TLS keys could be unwrapped on Cloudflareâs anycast network to provide strongerÂ technical guaranteesÂ of which region their requests are decrypted into. For instance, a customer could choose to only unwrap their private keys in India. So instead of allowing decryption across Cloudflareâs entire global network, GeoKey Manager makes sure TLS signing for each customer request happens in our India network.

GeoKey Manager evolved again in 2022 withciphertext policy attribute based encryptionÂ (ABE). Instead of tying encrypted keys to a fixed set of data centers, ABE expressed geographic requirements using attributes such as country or region, like âregion = European Unionâ or âregion = Canada + United States + Mexicoâ.Â Newly authorized servers could receive matching decryption capabilities without rewrapping every customer key.

That flexibility created a challenge and opportunity for the post-quantum transition. No production-ready post-quantum ABE scheme is available today,Â and customers do not need a large number of regions. A simpler design meets the requirement and is easier to maintain and operate. Cloudflare therefore uses hybridML-KEM-768Â andX25519Â protection with two kinds of keys, out of which ML-KEM-768 is aNISTÂ standard that also opens doors to highly sensitive customers. A regional root key is a symmetric secret tied to one region, and an application-specific key pair is derived from it for a single service, such asGatewayÂ orTunnel.Â This protects private-key material against harvest now, decrypt later while preserving regional key-use boundaries.

## Global ciphertext, regional key unwrapping

In its new form, GeoKey Manager is the key foundationÂ for Cloudflareâs data sovereignty solutions. It controls which region protected decryption keys can be used from and when. Separate workstreams determine where tunnels terminate, where traffic is inspected, how it is routed, and where plaintext processing occurs. But all of them depend on the region where a customerâs private key can be unwrapped, because TLS traffic can only be decrypted where that key is available.

During initialization, the edge key service (the component on each Cloudflare edge server that unwraps customer private keys and uses them to serve requests) verifiesÂ that it has loaded every regional root key required by its configuration. If a configured key is missing or malformed, the service does not start. After initialization, an individual request also fails closed (Cloudflare rejects it rather than risk unwrapping a key out of region) if its metadata identifies a regional root key that is not locally available. If a request for Germany was somehow trying to decrypt in Spain or France it would fail, since neither Spain nor France have the regional root key for Germany. This guarantees that a regional root key never leaves its region, no matter what.

Cloudflare needs to maintain high performance while keeping our customersâ regionalized data secure at scale. This is where the next version of GeoKey Manager comes in. We are enabling fastÂ performance while logically separating our network by using post-quantum cryptography to restrict where customersâ private keys are unwrapped.Â Most of our regions will be available for customers to regionalize their workflow, and there may be product specific caveats. Customers select a region and Cloudflare manages everything else needed to unwrap their private keys within the regionâs boundary.

## How GeoKey Manager ensures that keys are only available in a region

GeoKey Manager controls where wrapped private keys can be unwrapped and used on the data plane. It does not control where requests are forwarded or routed (thatâsÂRegional Services), where tunnels terminate, or where traffic inspection happens (also Regional Services).

GeoKey Manager separates globally distributed wrapped private keys from the regional root key required to unwrap it.Quicksilver, our global configuration distribution system, distributes wrapped private keys and its metadataÂ across our network. It does not distribute regional root keys; that happens through a separate provisioningÂ serviceÂ thatÂ stores regional root keys and delivers them only to edge servers authorized for each region. Regional root keys follow a separate, controlled path.Â On the data plane, a nodeâs regional configuration, which region a node belongs to, determines which nodes can receive which regional root keys.

### Defining key hierarchy and application-specific keys

Every wrapped customer private key carries metadata identifying its service context, regional boundary, and epoch.

The service context is the Cloudflare service that uses the key, such as Tunnel or Gateway. The regional boundary is the approved set of Cloudflare data centers where the key may be unwrapped and used, such as data centers in Germany or the European Union. The epoch identifies which generation of the regional root key the key belongs to; each rotation creates a new epoch.Â

For example, Acme Co. might have one key for TunnelÂ in Germany (acme0001) and another for GatewayÂ in Germany (acme0002). Road Runner Inc. might have one key for Tunnel in Germany (runner0001) and another for Gateway in the European Union (runner0002).

![](/images/posts/1ec2e24dd2b0.jpg)

Keys with the same service context, regional boundary, and epoch use the same application-specific key pair. Therefore, compromising the Tunnel-Germany application-specific private key could expose both acme0001 and runner0001, but not the Gateway keys. Compromising the Germany regional root key could affect every application-specific key derived from that root for the same epoch, including acme0001, acme0002, and runner0001.

[翻译失败，原文如下]

In the current architecture, the application-specific key pair is asymmetric. The public component wraps the customer's private key material, while the private component is required to unwrap it. The resulting wrapped private key is distributed with its service context (Access, Gateway, Tunnel,Cloudflare One client), region, and epoch.

### Provisioning regional root keys

![](/images/posts/bb2411e9dc66.jpg)

When Cloudflare/Admin configures a region for a CF1 use case, key management serviceÂ (which also derives application-specific key pairs and wraps customer private keys)Â creates a regional root key and associates it with a regional boundary and epoch and sends it to provisioning service for storage and distribution which under the hood uses Vault, which is managed by us on-premises.

### Authorizing edge servers for a region

![](/images/posts/440e45b367cc.jpg)

Before an edge server can receive a regional root key, provisioning service evaluates three inputs:

1. Trusted Platform ModuleÂ (TPM) proves that the server possesses a registered hardware identity
2. Zinc, Cloudflare's server inventory system, maps that identity to a data center and locationÂ
3. Provisioning service determines which regional root keys the server may access

Zinc updates its membership records for each edge server. This asynchronous process adds new servers as the network grows and removes servers when they are decommissioned. As Cloudflare performs maintenance on data centers in Germany, the definition of which data centers belong in Germany changes in Zinc. That definition is swiftly propagated through our network with QuicksilverÂ so that our edge is up to date. The reverse also works. As we add capacity to our network, the definition of Germany, or any other region, is updated in Zinc and that is also swiftly propagated through our network with Quicksilver.

Zinc also associates a registered hardware identityÂ with a server and physical location, which supportsFIPS 140-3Â compliance. TPM-backed identity, server inventory data, and regional configurations determine which region an edge server belongs to and what regional root keys it can access.

Each edge server calls the control planeâsÂ provisioning service, and provides its registered hardware identity. After verifying the serverâs hardware identity and regional membership, the provisioning service issues a token that permits the server to retrieve only the regional root keys authorized for its location. Each edge server receives its token and uses it to fetch the regional root keys.

Authorized edge servers load regional root keys into thekernel keyringÂ rather than persisting them on disk. Process level access controls limit which services can use them. Because this memory is volatile, a machine restart removes the keys and the server must authenticate and provision them again. This adds operational complexity in exchange for reducing persistent key material which could be an attack vector for adversaries.

### Wrapping private keys for global distribution

When the key-management service receives a customer's private key material with a service context and regional boundary, it will use the requestâs regional boundary to get the regional root key and its latest configured epoch. It will then derive the corresponding asymmetric application key pair and use its public component to wrap the private key. The result is a wrapped private key and its metadata.

Quicksilver will then distribute the wrapped private key and metadata across our network.Â Since the wrapped key requires the specified region to decrypt, global wrapped key distribution does not grant edge servers global access to the private key because unwrapping still requires the corresponding regional root key and service context.

![](/images/posts/6ffbb7c8abfd.jpg)

### Unwrapping using application-specific keys on the data plane

![](/images/posts/12786d3754d4.jpg)

## Why we chose this cryptographic design

### Symmetric roots with asymmetric key wrapping

Regional root keys are 256-bit symmetric secrets. GeoKey Manager derives application-specific keys from each regional root key. For the current Cloudflare One path, the control planeâs key management service derives an application-specificHybrid Public Key EncryptionÂ (HPKE) key pair.

### HPKE with hybrid post-quantum KEM

The Cloudflare One path uses HPKE, as defined inRFC 9180. Its key-encapsulation mechanism (KEM) combinesML-KEM-768Â withX25519, whileHKDF-SHA-256 provides key derivation and AES-256-GCM provides authenticated encryption. Combining post-quantum and classical components preserves confidentiality as long as at least one component remains secure.

### Designing for rotationÂ

The validated design supports two types of key rotation: soft rotation and hard rotation.

A soft rotation creates a new epoch for the regional root key while retaining controlled access to a limited number of previous regional root-key epochs â letâs say one previous generation, as an example. The customerâs new private-key material is wrapped using the latest epoch, while older wrapped private keys are still usable during the transition. This is a similar concept to when a credit card company allows you to use a previous version of your credit card for recurring payments from an authorized retailer. In this case, the number of epochs we support determine how many generations of previously wrapped private keys â credit cards â are usable. This allows customers to preserve their service uptime while they transition.

A hard rotation instead rewraps affected customersâ wrapped private keys under a replacement epoch so access to the previous epoch can be removed. In this case, it would be like the credit card company not allowing you to use the previous credit card for a transaction under any circumstances.

### Security and availability tradeoffs

Failing closed is a very intentional design choice.Â Failing open would mean unwrapping a customerâs private key outside its allowed region rather than rejecting the request. We never do that: if any required check fails (service context, region, epoch, etc.), the request is rejected. At startup, each edgeâs key service loads every configured regional root key from its Linux kernel keyring. Missing or malformed root keys prevent the edge key service from initializing. Once running, the edge key service uses in-memory copies so that it canât be tampered with, preventing out of region or cross-region unwrapping. In practice, an edge server serves requests for a region only once its configuration and key provisioning are complete.

The trust boundary (all services that can access the regional root key) includes the key-management service, the provisioning service, and authorized edge key services because each can access regional root keys. The key-management service uses them to derive application-specific keys, the provisioning service stores and distributes them, and edge key services use locally authorized copies of them. Quicksilver remains outside this boundary because it receives only wrapped private keys and associated metadata.

## Operating GeoKey Manager

Cloudflareâs network is constantly changing. As servers enter or leave service, Cloudflareâs fleet inventory updates regional membership. This means the list of data centers that make up a region like Spain is not static. GeoKey Managerâs provisioning layer refreshes that membership several times each day, granting or removing access to regional root keys as the network changes. This process is separate from key rotation and requires no customer action.

[翻译失败，原文如下]

When regional membership changes, the provisioning service immediately synchronizes the serverâs Linux kernel keyring with the latest authorized regional root keys. The edge key service caches these keys in process memory until it restarts or the cache expires. It then reloads the current authorized set from the kernel keyring.

## Whatâs next: Cloudflare One integration and CDN

GeoKey Manager is the basis for an improved Regional Services offering for Cloudflare One; these new capabilities will be announced in a few months.

Older versions of GeoKey Manager already provide geographic controls for private keys associated with CDN certificates. We are developing a separate integration that will bring this new post-quantum GeoKey Manager described here to that existing CDN capability. We will share testing and transition details when that work is ready.

If you are a current DLS customer who is regionalizing CDN traffic, you can register intent to test this feature before itâs generally available for CDN traffichere.

Thank you to everyone who made this product a reality. It was a huge effort across the Data Localization Suite, Cloudflare One, and Cloudflare Research teams.

- Cloudflare

---

> 本文由AI自动翻译，原文链接：[BringingÂ post-quantum cryptography to geographically fenced key management](https://blog.cloudflare.com/post-quantum-geo-key-manager/)
> 
> 翻译时间：2026-10-24 07:04
