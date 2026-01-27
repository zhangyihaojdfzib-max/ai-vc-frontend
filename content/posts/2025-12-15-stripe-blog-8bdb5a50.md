---
title: Stripe支持PayTo支付：澳大利亚实时支付解决方案
title_original: Accept PayTo Payments | Stripe
date: '2025-12-15'
source: Stripe Blog
source_url: https://stripe.com/payment-method/payto
author: Authorization Boost
summary: 本文介绍了Stripe集成的澳大利亚实时支付方式PayTo。PayTo支持单次和定期付款，能够帮助商家降低交易成本、提升转化率并拓展澳大利亚市场。文章详细说明了PayTo的功能特点、运作流程（客户通过银行信息授权支付），以及如何在Stripe平台上快速启用。此外，文章还提供了全球多个市场（如英国、澳大利亚、加拿大、法国、德国、意大利）的支付方式偏好数据，为商家提供市场洞察。
categories:
- AI产品
tags:
- 支付技术
- Stripe
- 实时支付
- 澳大利亚市场
- 金融科技
draft: false
translated_at: '2026-01-05T17:21:15.780Z'
---

PayTo是澳大利亚的一种实时支付方式，可用于接受单次和定期付款。

**提升销售额**
通过向本地买家提供他们偏好的实时支付方式，减少购物车放弃率并提高转化率。

**降低交易成本**
与卡支付相比，节省交易手续费成本。

**提供全球覆盖**
适应客户偏好并拓展新市场，支持全球买家使用的100多种支付方式。

**更快上线**
通过Payment Element或Checkout进行单一集成即可上线支付方式，无需额外的开发工作。

**功能**
*   客户所在地
    澳大利亚
*   呈现货币
    澳元
*   支付方式类别
    实时支付
*   结算时间
    适用标准结算时间
*   退款 / 部分退款
    支持 / 支持
*   支付确认
    由客户发起
*   定期付款
    支持
*   争议支持
    支持
*   Connect支持
    支持
*   可用地区
    澳大利亚

**运作方式**
**使用PayTo支付**
客户在结账时提供唯一的银行信息，以启动协议授权。随后，客户会收到其银行发来的授权PayTo协议的请求。
1.  选择PayTo
    客户从结账时显示的支付方式列表中选择PayTo。
2.  输入银行信息
    客户提供其PayID或银行账户信息以启动授权。
3.  授权交易
    客户收到其银行发来的授权PayTo交易的请求。
4.  支付完成
    客户收到支付完成的通知。

```
Select a payment method
Card
PayTo
Full name
First and last name
PayID
Email or phone number
Place order
```

**开始使用**
**在Stripe上轻松上线和管理支付方式**
只需在设置中点击即可添加和管理支付方式。
**访问统一报告**
在Stripe仪表板中查看使用各种支付方式完成的所有付款。

**资源**
**支付方式类型指南**
一份完整指南，列出了不同类型的可用支付方式，帮助您了解并为您的业务选择合适的支付选项。

**了解全球消费者支付方式偏好的差异。**
英国是欧洲最以卡为中心的市场，人均拥有超过两张卡。

**热门支付方式**
Visa
PayPal
Mastercard
Bacs Direct Debit
Klarna
UK bank transfers
Apple Pay
Google Pay
American Express
Revolut Pay

**支付方式份额**
*   卡支付：58%
*   电子钱包：20%
*   银行借记：7%
*   银行跳转：1%
*   银行转账：3%
*   先买后付：5%
*   现金代金券：2%
*   其他：4%

信用卡普及率：58%
银行账户人口比例：96%

2019年，澳大利亚83%的销售点支付为无接触支付，使其成为全球最大的无接触支付国家。此后，数字钱包日益普及，2022年约有25%的卡支付通过数字钱包完成。

**热门支付方式**
Visa
Australian BECS Direct Debit
Afterpay/Clearpay
American Express
Mastercard
eftpos Australia
Apple Pay
Google Pay
Click to Pay
Zip

加拿大消费者主要使用信用卡或借记卡，数字钱包也越来越受欢迎。

**热门支付方式**
Visa
Mastercard
Interac
American Express
Pre-authorised debits
Affirm

Cartes Bancaires是法国最大的国内卡网络，约占线下支付的80%和在线支付的60%。

**热门支付方式**
Cartes Bancaires
PayPal
SEPA bank transfers
SEPA Direct Debit
Visa
Mastercard
Apple Pay
Google Pay
Klarna
Alma

PayPal等电子钱包是在线支付的首选方式，先买后付也越来越受欢迎。

**热门支付方式**
PayPal
Visa
Mastercard
SEPA Direct Debit
SEPA bank transfers
Klarna
Apple Pay
Google Pay

偏爱店内现金支付的较成熟人口结构导致其电子商务市场增长慢于其他欧洲国家。然而，37%的人口因疫情进行了首次在线购物。

**热门支付方式**
PayPal
Visa
Mastercard
Apple Pay
SEPA Direct Debit
SEPA bank transfers
Google Pay
American Express
Klarna
Satispay

大约70%的电子商务支付使用信用卡。日本拥有独特的本地支付方式组合，如便利店支付和银行转账，这些方式仍然很受欢迎。

**热门支付方式**
Visa
Mastercard
JCB
American Express
Konbini
Bank Transfers (Furikomi)
PayPay

在马来西亚，大约50%的在线消费支付通过FPX和数字钱包完成。货到付款仍然是一种流行的支付方式，约占在线购物的11%。

**热门支付方式**
FPX
Visa
Mastercard
GrabPay
Google Pay
American Express
Alipay
WeChat Pay
Touch'n Go

由于银行账户人口比例较低，大多数人更喜欢在墨西哥的便利店使用现金支付。此外，30-40%的电子商务消费使用分期付款计划。

**热门支付方式**
Visa
Mastercard
Mexico bank transfers (SPEI)
OXXO
American Express
Meses Sin Intereses

iDEAL是一种为在线支付提供银行转账的本地支付方式，服务于所有荷兰消费者银行。它主导了在线支付领域，占数字购物的69%。超过90%的本地卖家现在接受iDEAL。

**热门支付方式**
iDEAL
Mastercard
SEPA Direct Debit
Klarna
PayPal
SEPA bank transfers
Visa
Apple Pay

先买后付作为一种支付方式在新西兰快速增长，预计到2025年将占所有电子商务交易的17%。

**热门支付方式**
Visa
Mastercard
Afterpay/Clearpay
American Express
Apple Pay
Google Pay
New Zealand BECS Direct Debit

BLIK是一种银行跳转支付方式，是最受欢迎的移动支付方式，在2021年占电子商务支付组合的54%。

**热门支付方式**
BLIK
Przelewy24
Visa
Mastercard
Apple Pay
Google Pay
PayPal

虽然新加坡的信用卡普及率是该地区最高的，但包括数字钱包和实时支付在内的本地支付方式也很受欢迎。PayNow是增长最快的支付方式。

**热门支付方式**
Visa
Mastercard
PayNow
Apple Pay
GrabPay
American Express
China UnionPay
Google Pay
Alipay
WeChat Pay

西班牙传统上是一个以现金为中心的市场，尽管这种情况正在改变。数字钱包越来越受欢迎，占在线购物的很大一部分。

**热门支付方式**
Visa
PayPal
Mastercard
SEPA Direct Debit
SEPA bank transfers
Klarna
Apple Pay
Google Pay

瑞典是全球现金使用率下降最快的国家。先买后付和移动钱包等数字支付方式是标准支付方式。

**热门支付方式**
Klarna
Swish
Mastercard
Visa
Apple Pay
Click to Pay
Google Pay
PayPal

**热门支付方式**
Visa
PayPal
Mastercard
Bacs Direct Debit
Klarna
UK bank transfers
Apple Pay
Google Pay
American Express
Revolut Pay

信用卡仍然是主要的支付方式，数字钱包也越来越受欢迎。

**热门支付方式**
Visa
Mastercard
American Express
Apple Pay
USD bank transfers
Klarna
Google Pay
Discover
Affirm
Amazon Pay

**准备开始了吗？联系我们或创建账户。**
使用简单、按量付费的定价访问完整的支付平台，或联系我们为您的业务专门设计定制套餐。

**设计您的支付页面**
使用Stripe Elements（我们的一套预构建可嵌入UI组件）创建您自己的支付页面。

**托管支付页面**
通过集成Stripe Checkout（我们为转化优化的预构建支付页面）在您的网站上接受付款。

> 本文由AI自动翻译，原文链接：[Accept PayTo Payments | Stripe](https://stripe.com/payment-method/payto)
> 
> 翻译时间：2026-01-05 17:21
