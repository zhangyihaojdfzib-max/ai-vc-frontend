---
title: 'PARDIG & SatWeave: Foundational Datasets for Earth Science'
title_original: 'PARDIG & SatWeave: Foundational Datasets for Earth Science'
date: '2026-11-10'
source: Google DeepMind
source_url: https://deepmind.google/blog/opening-the-datasets-behind-our-ai-weather-models/
author: ''
summary: '[翻译失败，原文如下]


  # Opening the datasets behind our AI weather models


  WeatherNext team


  ![Abstract 3D illustration of a globe segmented by layered transpa...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-14T08:49:18.413521'
---

[翻译失败，原文如下]

# Opening the datasets behind our AI weather models

WeatherNext team

![Abstract 3D illustration of a globe segmented by layered transparent panes showing different weather and climate datasets, including satellite imagery and precipitation grids.](/images/posts/27de6f32121c.jpg)

We are releasing PARDIG and SatWeave to help researchers and developers build new weather, hydrology, and climate applications.

Understanding and predicting the planetâs weather and water cycle starts with how well we can observe the Earth right now. Satellites and ground instruments monitor the planet continuously and in great detail. But converting these raw measurements into a coherent global picture and making it available quickly is a major scientific and engineering challenge.

Today, we are releasing two foundational datasets, SatWeave and PARDIG, to support the global community in building weather, hydrology, and climate applications. Both datasets are key to the advances in our recently releasedWeatherNext 3model. SatWeave is a global mosaic of geostationary satellite imagery that provides the model a live view of developing clouds and storms. PARDIG is an AI-based global precipitation dataset that was used to train the modelâs precipitation forecasts. We are making historical archives and live feeds of both datasets available, so researchers and developers can use them in their modeling and downstream applications.

## SatWeave: A unified view of Earth from space

SatWeave combines imagery from five satellites, which cover different parts of the globe: GOES-East and GOES-West, Meteosat 0 and Meteosat Indian Ocean, and Himawari. Because each uses different map projections, file formats, sensors, and scan schedules (ranging from 10 to 30 minutes), it is difficult to form a coherent global map. Most existing global composites drop incompatible aspects, offering only four or fewer channels, or updating every few hours.

![SatWeave blends observations from six geostationary satellites into a global mosaic across 17 visible, water vapor, and infrared channels.](/images/posts/f0186397c8b8.jpg)

![](/images/posts/4bf21547fada.jpg)

SatWeave blends observations from six geostationary satellites into a global mosaic across 17 visible, water vapor, and infrared channels.

SatWeave updates hourly and thus allows WeatherNext 3 to produce new global predictions, in contrast to models initialized on analysis data refreshed every six hours. We are releasing this hourly live feed, and a historical archive spanning over a decade.

While we have used SatWeave in WeatherNext 3âs medium-range weather forecasts, we're eager to explore forecasting applications such as solar power and wildfire monitoring with the broader research and developer communities.

## PARDIG: Accurate, high-resolution precipitation across the globe

Precipitation shapes everything from our food and water supplies to the risk of floods and droughts, yet tracking it accurately across the planet remains a major challenge. While ground radars and dense rain gauge networks provide high-quality data, they aren't always available or have good coverage in all regions.

To help bridge this gap, we developed PARDIG (Precipitation AI Reanalysis: Densely Inferred GPM). Built on an AI architecture similar to WeatherNext 3, PARDIG is trained directly on sparse spaceborne radar observations from the NASA Global Precipitation Measurement (GPM) Core Observatory, using SatWeave imagery and atmospheric fields from ECMWF as inputs. The result is a highly accurate global precipitation map at 15-minute temporal resolution and roughly 10-kilometer resolution, updated with an average latency of about five hours.

Hourly rainfall during the July 2025 Texas Hill Country flash floods, comparing ground-based NOAA MRMS radar (left, ~1 km) with near-real-time PARDIG (center, ~10 km) and IMERG-Final (right, ~10 km).

We have performed evaluations of PARDIG against three continental radar networks across the US, Europe, and Japan, as well as over 36,000 weather stations worldwide. PARDIG outperforms leading global baselines across all analyzed rain rates, including NASAâs IMERG-Final, a research-quality dataset of precipitation estimates that is incredibly important for countless applications. PARDIG improves hourly precipitation detection skill over IMERG-Final by more than 30% on light-to-moderate precipitation. It proved particularly effective at capturing extreme precipitation, which can be challenging for existing global products to detect.

![Hourly precipitation detection skill (Critical Success Index) evaluated from 2016 to 2023 against ground radar networks in the US, Europe, and Japan. Precipitation intensity thresholds are plotted on a logarithmic scale from 0.2 to 25 mm/h, with Light (0.3 mm/h), Moderate (2.5 mm/h), and Heavy (20 mm/h) marked on the axis.](/images/posts/f86c931ff7f3.jpg)

![Three graphs comparing the precipitation detection skill (CSI) of three modelsâPARDIG (near-real-time), IMERG-Final, and IMERG-Earlyâacross light, moderate, and heavy precipitation intensities in the United States, Europe, and Japan. In all regions, the PARDIG model consistently demonstrates the highest accuracy.](/images/posts/42b71ec9251c.jpg)

Hourly precipitation detection skill (Critical Success Index) evaluated from 2016 to 2023 against ground radar networks in the US, Europe, and Japan. Precipitation intensity thresholds are plotted on a logarithmic scale from 0.2 to 25 mm/h, with Light (0.3 mm/h), Moderate (2.5 mm/h), and Heavy (20 mm/h) marked on the axis.

Because PARDIG learns directly from satellites rather than relying solely on ground-based measurements, we expect it to have reliable accuracy everywhere on Earth, even in areas where these measurements are not available.

Along with the live data feed, we are releasing historical archives of PARDIG data from 1999 to 2026. While WeatherNext 3 used PARDIG for medium-range weather forecasting, we're excited to partner with, and enable, the community in exploring improved models for floods, landslides, and drought, especially in regions without dense ground radar networks.

## Empowering the weather and climate ecosystem

The SatWeave and PARDIG live and historical datasets are now openly available on Google Cloud Storage. PARDIGâs historical catalogs are also available in Google Earth Engine. As the latest addition to GoogleâsEarth AIportfolio, we hope these datasets empower researchers around the world to open new ways of connecting weather observations to crucial, real-world applications.

## Learn more

## Acknowledgements

This work was developed by teams across Google DeepMind and Google Research, in collaboration with Google Cloud and Google Geo. We thank the organizations whose open satellite programs and datasets make this work possible, including ECMWF, NASA, JAXA, NOAA, EUMETSAT, KMA, JMA, KNMI, and Synoptic Data.

### Introducing WeatherNext 3, our most advanced and accurate global weather AI model

![](/images/posts/d6b7590df19e.jpg)

---

> 本文由AI自动翻译，原文链接：[PARDIG & SatWeave: Foundational Datasets for Earth Science](https://deepmind.google/blog/opening-the-datasets-behind-our-ai-weather-models/)
> 
> 翻译时间：2026-11-14 08:49
