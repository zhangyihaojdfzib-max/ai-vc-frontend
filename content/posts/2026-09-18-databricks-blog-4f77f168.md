---
title: Enabling secure, productive work on personal devices
title_original: Enabling secure, productive work on personal devices
date: '2026-09-18'
source: Databricks Blog
source_url: https://www.databricks.com/blog/enabling-secure-productive-work-personal-devices
author: ''
summary: '[翻译失败，原文如下]


  - How Databricks protects corporate data on personal devices while preserving employee
  privacy and building user trust.

  - A layered mobil...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-19T06:55:41.275072'
---

[翻译失败，原文如下]

- How Databricks protects corporate data on personal devices while preserving employee privacy and building user trust.
- A layered mobile security strategy covering device management, identity and access, zero trust, and application management.
- A practical example of applying the strategy to the Genie mobile app and partnering with Engineering as “customer zero.”

At Databricks IT, our vision is to empower people to work from anywhere without putting company data at risk. On mobile devices, the focus has shifted from merely checking email to getting real work done. People use Slack, approve requests, and access internal apps on their personal phones, and they expect it just to “work”. Additionally, the proliferation of AI Agents and tools like Genie, Omnigent, and Claude Code has shifted the way people work, with a growing desire to move desktop sessions to phones on the go to avoid losing deep work and context. Mobile BYOD makes that harder, because work and personal life share the same device. A personal phone is different from a company laptop. We, as in Databricks, do not own it, certain access cannot be restricted, and we have no right to view its contents. The challenge we set out to solve was simple to state and hard to do:protect corporate data on devices we don't own, without ever intruding on user privacy.

This post walks through how we approach mobile security internally. Instead of focusing on just one product, our approach consists of four layers, each serving a specific purpose: device management, authentication, zero trust, and application management.

## Device management

Before securing a phone, we must establish a trusted method for installing apps, configuration profiles, certificates, and security policies. This is achieved through Mobile Device Management (MDM), the foundational layer on which all other components rely.

The most important decision for personal devices is how to enroll them. We utilize Account-Driven User Enrollment (ADUE) on iOS, tailored for the "bring your own device" scenario. We avoid full device management on personal phones. User enrollment manages only the work-related components, never the device itself, which prevents us from taking control or imposing restrictions we have no business imposing on someone's personal phone. There have been notable security incidents in the wild where the absence of full wipe capabilities is a major benefit and helps build user trust in adopting Mobile Security controls.

During enrollment, the phone establishes a separate, encrypted workspace for work data linked to a managed corporate identity, while personal apps, photos, and messages remain fully private and inaccessible to us. On Android, the Work Profile offers a comparable clear separation.

MDM is often mistaken for the finish line. In reality, it's just the starting point. It allows us to establish a baseline, but it doesn't decide who gets access or check whether the device is trustworthy. Those capabilities lie in the subsequent layers.

## Identity and access

Once device management is established, the next step is determining access. Authentication (authN) and context-aware signals act as the gatekeeper for every company resource and are managed through our identity provider.

No request is granted on identity alone. Every request is weighed against a set of signals that together decide whether the gate opens. First is identity, confirming the user is who they claim to be, backed by strong, phishing-resistant, passwordless, multi-factor authentication. Next is the device, confirming the request comes from a known and managed phone rather than an unregistered or unknown one. Finally, the network path allows access only when the request arrives through our trusted tunnel. This is where authentication quietly leans on the next layer. The gate verifies that requests come from our secure network addresses, and those addresses are valid only while zero trust deems the device healthy. If any of these signals are weak or missing, the gate stays shut.

For most organizations, this is the highest-impact control you can turn on, and it's the right thing to enforce first. No trusted signals, no access.

## Zero trust

Authentication determines whether access should be granted, whereas implementing a Zero Trust Network Access (ZTNA) solution assesses the device's current health and provides real-time enforcement, not limited to login events. Work-related traffic is routed through a secure tunnel via a per-app VPN, ensuring personal traffic remains separate. Posture is evaluated continuously while the device is in use, not just once at the door. For example, our policy can automatically identify a vulnerable or compromised OS and block that device's traffic immediately, without manual intervention.

The fundamental principle is to deny access by default and permit only when acceptable conditions are met. Rather than granting broad network access, ZTNA grants access only to specific applications, while both the user's identity and the device's health remain valid. If either slips, access drops. We focus on our most critical applications, where continuous verification matters most.

## Application management

When deploying an app to a mobile device, the first step is installing it as a managed app. This ensures the copy of the app on the phone is controlled by us, not a self-downloaded version. How we then secure company data depends on the app. Sometimes, we push a managed configuration via the MDM, such as settings that restrict data to within the app or pre-configure secure sign-in. Certain apps include their own enterprise management features, while others offer tenant-level controls, such as blocking copy and paste outside the app, managed through the service rather than the device. When effective, corporate data remains within a secure boundary, even on personal devices.

Mobile device management provides the app, while application management determines its functionalities.

We can only reliably enforce the managed version of an app when the app or the service itself is compatible, either by refusing to run without our managed configuration or by accepting traffic only from our secure tunnel. When an app supports neither, our identity policy can confirm the device is managed, but it cannot tell whether the specific copy in use is ours or one downloaded straight from the app store. We solve this by tiering apps by sensitivity, strictly favoring apps that support enterprise mobility controls, steering web apps through an enterprise-managed browser so a single controlled channel covers many services at once, and requiring support for managed configuration or network restrictions when evaluating new mobile applications.

## Privacy and transparency

A mobile security program's success depends on employee enrollment. Even the most sophisticated controls are useless if staff perceive the company is secretly monitoring their personal devices, leading to low participation. Therefore, we prioritize employee experience and transparency as crucial components.

Our foundation is complete transparency regarding privacy. We clearly communicate, in plain language, what company staff can and cannot access and what actions they can take on personal devices. We documented this policy, reviewed it with Legal and Privacy teams, and made it easily accessible before enrollment. Trust is built through this high level of transparency.

## All this in practice

We use this model to build and secure our own mobile apps - including theGeniemobile app – in which Databricks IT was customer zero.

[翻译失败，原文如下]

Databricks IT collaborates closely with Engineering rather than acting as a stakeholder. We work alongside them, recommending additional controls that Genie continues to use to this day. Genie is deployed to our mobile fleet as a managed app, with access limited through identity controls to ensure only authorized users on managed devices can use it. Traffic is sent through our secure tunnel for security and regular posture checks. Since the foundational security layers were already in place, Genie did not need a separate mobile security solution and instead used our existing infrastructure.

As customer zero, Databricks IT had the opportunity to guide product development and produce documentation that helps our customers deploy the app. We provided feedback to Engineering on enrollment, mobile access processes, and the security model needed for mobile. This ongoing input helps shape Databricks offerings like Genie and Omnigent. This partnership enables many future internal and customer-facing applications that deliver a secure, mobile-first experience.

## Key takeaways

- Layering your Mobile StrategyNo single control can fully secure mobile devices. Instead, security relies on combining device management, identity, zero trust, and app management, so each layer adds compensating controls that culminate in a holistic solution.
- Privacy and User TrustThe controls that visibly protect personal data are the ones people are willing to accept, and that acceptance is what makes the strategy work.
- Know the capabilitiesNot every app can be fully locked down on a personal device. Build your strategy around that reality rather than assuming a policy reaches further than it does.

- No single control can fully secure mobile devices. Instead, security relies on combining device management, identity, zero trust, and app management, so each layer adds compensating controls that culminate in a holistic solution.

- The controls that visibly protect personal data are the ones people are willing to accept, and that acceptance is what makes the strategy work.

- Not every app can be fully locked down on a personal device. Build your strategy around that reality rather than assuming a policy reaches further than it does.

## Conclusion

No single control can secure a personal device. Instead, security depends on multiple layers working together. Start with mobile device management, gate access through identity and device status, run continuous health checks on vital signals, and contain data at the app level wherever feasible. Roll these layers out gradually and always respect user privacy, so security feels inherent rather than imposed. On devices the company doesn't own, willing participation is what makes security effective.

Please visithttps://www.databricks.com/trustto learn more about our platform security and compliance capabilities

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Enabling secure, productive work on personal devices](https://www.databricks.com/blog/enabling-secure-productive-work-personal-devices)
> 
> 翻译时间：2026-09-19 06:55
