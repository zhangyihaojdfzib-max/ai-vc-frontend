---
title: The GPU Revenue Ladder
title_original: The GPU Revenue Ladder
date: '2026-10-21'
source: Tomasz Tunguz
source_url: https://tomtunguz.com/the-gpu-revenue-ladder/
author: ''
summary: '[翻译失败，原文如下]


  In short :SpaceX''s third-quarter report & DeepSeek''s inference disclosure together
  price one GPU card-hour four ways, from DeepSeek''s the...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-22T06:55:02.291593'
---

[翻译失败，原文如下]

In short :SpaceX's third-quarter report & DeepSeek's inference disclosure together price one GPU card-hour four ways, from DeepSeek's theoretical $38 maximum to SpaceX's realized $2.44. Combined with a payback claim of under a year & a 2027 supply pipeline that is largely unbuilt, the data suggests large-scale inference is a healthy business with room for prices to climb.

Yesterday brought two data points about the health of inference businesses : SpaceX’s third-quarter report1& DeepSeek’s inference post.2

Overall, they demonstrate that inference businesses can be quite healthy even at current prices & efficiencies. Plus there is a tremendous amount of upside assuming demand persists at higher prices per card hour.

![Horizontal bar chart of revenue per GPU card-hour: DeepSeek maximum $38.00, B200 spot $8.77, SpaceX negotiated $5.27, SpaceX realized $2.44](https://res.cloudinary.com/dzawgnnlr/image/upload/w_2240,h_1264,c_fill,g_auto,q_auto,f_auto/https://res.cloudinary.com/dzawgnnlr/image/upload/v1792601256/analysis/spacex-q3-2026-ai-economics/chart-gpu-revenue-ladder-d788d9e638a9.png)

DeepSeek calculates a $38 maximum per GPU card-hour.3It describes a GPU running under optimal conditions : maximum utilization for external customers rather than internal work, & 100% of its output usable & billable, sold at full list price.

Revenue may be lower because V3 is priced below R1, & because prices vary between peak & off-peak hours.4

The spot price, what it costs to rent a card on the open market today, is $8.77.5SpaceX provides us with both the negotiated price from its contracts, at $5.27,6as well as the overall realized revenue, including operations costs, training, unusable & unbillable work.7

“At current pricing, new compute deployments are generating a payback of less than a year.”

— Bret Johnsen, CFO, SpaceX Q3 2026 earnings call

Assuming the quote measures payback after tax, on fully loaded costs, these economics suggest that the inference business can be a very good one.8

But the case rests on demand persisting, & on efficiency outrunning price cuts. The forces pushing the other way are considerable.

GPU rental prices doubled in six months, from $4.40 to $8.08 per card hour, while the price of intelligence fell much faster. OpenAI cut Luna 80% in July & another 50% in September. A benchmark threshold that cost $0.55 eighteen months ago now clears at $0.0015, a 377-fold reduction.9If tokens deflate that quickly while cards cost more, gross profit per card hour depends entirely on throughput gains keeping pace.

The second force moves inference off the datacenter altogether. AI companies are asking Qualcomm to run large models on the handset itself.

“Some of the companies at the forefront of AI are telling Qualcomm, by 2028, I need to make sure that I have the ability to run at least a hundred billion parameter model into a phone.”

— Cristiano Amon, CEO, Qualcomm, on the Sources podcast

Inference running on laptops & phones never sends tokens to the cloud.10

But the cloud is not big enough to support demand, & new data centres are behind schedule, with GPUs sitting idle on warehouse floors waiting for power.11JPMorgan finds that more than 60% of the data centre capacity planned for 2027 is not yet under construction, & a further 7% is delayed.12With demand continuing to drive record revenue growth for AI, the deflationary forces may succumb to too much demand.

The economics of large scale inference suggest the business model is healthy at scale, & token factories benefit from more rungs to climb on the pricing ladder.

1. Space Exploration Technologies Corp., Form 8-K for the quarter ended September 30, 2026, filed October 20, 2026, Exhibit 99.1.https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/0001628280-26-066482-index.htm↩︎
2. DeepSeek’s V4.1-Flash disclosure, which reports revenue of about $38 per card-hour at off-peak prices & roughly $0.60 per million tokens. The figure describes a single best cluster running its cheapest model, not a fleet average. DeepSeek’s earlier V3/R1 overview, from open-source week in February 2025, implied about $12.90 per card-hour: $562,027 of notional daily revenue against $87,072 of daily cost on 1,814 GPUs.https://github.com/deepseek-ai/open-infra-index/blob/main/202502OpenSourceWeek/day_6_one_more_thing_deepseekV3R1_inference_system_overview.md↩︎
3. Every figure here is an estimate. No company in this table publishes a per-card-hour revenue figure as such. SpaceX’s are derivations from filings & DeepSeek’s is explicitly theoretical.↩︎
4. Revenue may be lower than the maximum because V3 is priced below R1, & because prices vary between peak & off-peak hours. See note 3.↩︎
5. ORNN Compute Price Index, settled 2026-10-20. A volume-weighted winsorized mean of executed neocloud transactions, excluding reserved & forward contracts.↩︎
6. S-1 & S-1/A, 2026 : $1.25b divided by 325,000 GPUs times 730.5 hours equals $5.27. The GPU count & whether the contract bundles power or shells make this an upper bound on pure compute.↩︎
7. Q3 2026 8-K : AI segment revenue of $7,560m annualized & divided by 1.7 GW. The figure uses installed rather than utilized capacity. The Q2 10-Q defines nameplate as not representing actual utilization.↩︎
8. Payback is capex divided by annual cash flow, where cash flow is revenue less cash operating costs. Depreciation is excluded from the denominator because the capex is already the numerator. Per card, a $46 per watt build costs $55,200, while the $5.27 contract rate yields $46,165 of annual revenue against roughly $570 of cash operating cost, giving a payback of 1.21 years. At B200 spot the payback is 0.72 years. To reconcile the quote with a $46 per watt build, we assume Johnsen is measuring after tax. At a 21% federal rate, 100% bonus depreciation shields $11,592 in year one, lifting first-year cash flow to $57,187 & shortening payback to 0.97 years. That is a timing benefit rather than a cost reduction : total deductions over the asset’s life are unchanged, so it flatters a payback metric far more than it improves net present value. SpaceX has not disclosed whether the figure is pre- or after-tax, state taxes would raise the shield, & the availability of full bonus depreciation for datacenter property placed in service in 2026 should be verified rather than assumed.↩︎
9. How GPU Prices Can Double While AI Gets Cheaper. The 377x figure comes from Epoch AI,The Plunging Price of Thought. Luna pricing fromGPT-5.6. Microsoft’s 90% tokens-per-GPU-year from$555B of Cloud Spend.↩︎
10. Cristiano Amon, Qualcomm, interviewed by Alex Heath on the Sources podcast, published October 8, 2026. He did not name the companies. Qualcomm’s current flagship can run a 30-billion-parameter mixture-of-experts model locally, so a hundred billion parameters is roughly a three-fold jump within about two years.↩︎
11. Business Insider, October 20, 2026 : Amazon is taking ownership of Nvidia GB300 racks under a program AWS calls “Early Rack Receipt,” before the sites to run them are ready. An internal email projected roughly $5 billion of GB300 deliveries in August alone, & about $3 billion a month thereafter, with some facilities holding space for more racks but lacking the power to activate them. Amazon described staging hardware near deployment sites as standard practice.https://www.businessinsider.com/amazon-nvidia-ai-gpu-data-centers-power-shortages-2026-10↩︎
12. JPMorgan, cited by the Wall Street Journal in June 2026 : more than 60% of data centre capacity planned for completion in 2027 is not yet under construction, & a further 7% is delayed. Goldman Sachs Commodities Research put on-time delivery for the next one to two years at only 50% to 60%, against a historical base rate of roughly 72% for capacity scheduled within four quarters.↩︎

[翻译失败，原文如下]

Space Exploration Technologies Corp., Form 8-K for the quarter ended September 30, 2026, filed October 20, 2026, Exhibit 99.1.https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/0001628280-26-066482-index.htm↩︎

DeepSeek’s V4.1-Flash disclosure, which reports revenue of about $38 per card-hour at off-peak prices & roughly $0.60 per million tokens. The figure describes a single best cluster running its cheapest model, not a fleet average. DeepSeek’s earlier V3/R1 overview, from open-source week in February 2025, implied about $12.90 per card-hour: $562,027 of notional daily revenue against $87,072 of daily cost on 1,814 GPUs.https://github.com/deepseek-ai/open-infra-index/blob/main/202502OpenSourceWeek/day_6_one_more_thing_deepseekV3R1_inference_system_overview.md↩︎

Every figure here is an estimate. No company in this table publishes a per-card-hour revenue figure as such. SpaceX’s are derivations from filings & DeepSeek’s is explicitly theoretical.↩︎

Revenue may be lower than the maximum because V3 is priced below R1, & because prices vary between peak & off-peak hours. See note 3.↩︎

ORNN Compute Price Index, settled 2026-10-20. A volume-weighted winsorized mean of executed neocloud transactions, excluding reserved & forward contracts.↩︎

S-1 & S-1/A, 2026 : $1.25b divided by 325,000 GPUs times 730.5 hours equals $5.27. The GPU count & whether the contract bundles power or shells make this an upper bound on pure compute.↩︎

Q3 2026 8-K : AI segment revenue of $7,560m annualized & divided by 1.7 GW. The figure uses installed rather than utilized capacity. The Q2 10-Q defines nameplate as not representing actual utilization.↩︎

Payback is capex divided by annual cash flow, where cash flow is revenue less cash operating costs. Depreciation is excluded from the denominator because the capex is already the numerator. Per card, a $46 per watt build costs $55,200, while the $5.27 contract rate yields $46,165 of annual revenue against roughly $570 of cash operating cost, giving a payback of 1.21 years. At B200 spot the payback is 0.72 years. To reconcile the quote with a $46 per watt build, we assume Johnsen is measuring after tax. At a 21% federal rate, 100% bonus depreciation shields $11,592 in year one, lifting first-year cash flow to $57,187 & shortening payback to 0.97 years. That is a timing benefit rather than a cost reduction : total deductions over the asset’s life are unchanged, so it flatters a payback metric far more than it improves net present value. SpaceX has not disclosed whether the figure is pre- or after-tax, state taxes would raise the shield, & the availability of full bonus depreciation for datacenter property placed in service in 2026 should be verified rather than assumed.↩︎

How GPU Prices Can Double While AI Gets Cheaper. The 377x figure comes from Epoch AI,The Plunging Price of Thought. Luna pricing fromGPT-5.6. Microsoft’s 90% tokens-per-GPU-year from$555B of Cloud Spend.↩︎

Cristiano Amon, Qualcomm, interviewed by Alex Heath on the Sources podcast, published October 8, 2026. He did not name the companies. Qualcomm’s current flagship can run a 30-billion-parameter mixture-of-experts model locally, so a hundred billion parameters is roughly a three-fold jump within about two years.↩︎

Business Insider, October 20, 2026 : Amazon is taking ownership of Nvidia GB300 racks under a program AWS calls “Early Rack Receipt,” before the sites to run them are ready. An internal email projected roughly $5 billion of GB300 deliveries in August alone, & about $3 billion a month thereafter, with some facilities holding space for more racks but lacking the power to activate them. Amazon described staging hardware near deployment sites as standard practice.https://www.businessinsider.com/amazon-nvidia-ai-gpu-data-centers-power-shortages-2026-10↩︎

JPMorgan, cited by the Wall Street Journal in June 2026 : more than 60% of data centre capacity planned for completion in 2027 is not yet under construction, & a further 7% is delayed. Goldman Sachs Commodities Research put on-time delivery for the next one to two years at only 50% to 60%, against a historical base rate of roughly 72% for capacity scheduled within four quarters.↩︎

---

> 本文由AI自动翻译，原文链接：[The GPU Revenue Ladder](https://tomtunguz.com/the-gpu-revenue-ladder/)
> 
> 翻译时间：2026-10-22 06:55
