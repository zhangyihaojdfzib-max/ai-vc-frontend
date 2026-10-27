---
title: 'Lessons from Pixar: Why Software Developers Should Be Storytellers'
title_original: 'Lessons from Pixar: Why Software Developers Should Be Storytellers'
date: '2024-01-11'
source: First Round Review
source_url: https://review.firstround.com/lessons-from-pixar-why-software-developers-should-be-story-tellers/
author: ''
summary: '[翻译失败，原文如下]


  When most people think ofPixarthey think of movies likeFindingNemoandToy Story.
  But the studio has also been producing world-class film-m...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-27T07:31:55.847577'
---

[翻译失败，原文如下]

When most people think ofPixarthey think of movies likeFindingNemoandToy Story. But the studio has also been producing world-class film-making software for almost three decades to help bring those stories to life on the big screen. I was fortunate to work as an engineering lead on the software team at Pixar. During my time there, we utilized techniques that are commonly used in film-making to help build the studio's new software pipeline, now called Presto. This is what I learned.

Talk to users in their own language. Use concepts and processes that your users are familiar with in order to communicate software designs as naturally as possible.

## Film Concepts in Software

It's often said at Pixar that “story is king” and that this is the primary reason for the company's success. Appropriately then, all films at Pixar begin with the Story Department, where the initial script is developed and expressed on storyboards to refine the look and feel of the film. (Storyboards are physical boards of wood with a grid of 4" x 6" hand-drawn index cards pinned to them.) This story is pitched to the executive team before being green lit and entering production.

In many ways, designing a great software product is like creating a great story. It’s not surprising that modern agile processes refer to “user stories” as a way to capture requirements from the perspective of the user. So very early on we took this concept to the next level and created a story department in our software group. This department was responsible for designing the user workflows of our new software and communicating these to our production users on standard storyboards. These boards were presented to artists (our customers) in the format of a story pitch, allowing them to interact with us in a familiar style and meeting structure. We also had a “story room” that contained all of these storyboards up on the walls, encompassing the design for the entire system in one space.

Of course, this approach will not be appropriate for all other software projects, but the key lesson is to talk to your users, and use the techniques and language they understand best. Similarly, while it's obvious that you must listen to your users when writing software for them, we took this one step further by actually embedding some of our users in our software group.

Artists rotate off and on films at different times, so we would try to find ones who were between films and who were interested in affecting the direction of the studio's software. These artists would help us refine the workflows and user interfaces for the new software based upon their experiences with the existing software. For example, our initial focus was to support the articulation pipeline, so we had a senior articulator join our group early on. He would use our software on a daily basis to try and articulate models of Buzz and Woody, he would be in design meetings to provide input on features and point out things we were missing. He would also help us brainstorm new ways for articulators to work more efficiently.

Having this level of input from an expert user gave us the confidence that we were building something that would solve the problems that our customers were actually having on a daily basis. The other benefit is that these embedded artists could then become evangelists for the product amongst their peers.

## Communicating Progress

Demonstrate your software internally. Some of the best notes can come from people you least expect.

Once a film is in production, individual departments assemble the digital assets of the film, including modeling, articulation, layout, set dressing, animation, simulation, lighting, shading, special effects and final rendering. A system of daily and weekly reviews (known as “dailies” and “weeklies”) is used to refine all production work. These reviews take place in a screening room with your peers, often with the director present. Throughout this process, the story is continually refined and the latest film “reels” are presented to the entire company one or two times a year, at which point all employees are encouraged to submit notes for improvement. That is one of the amazing things about Pixar: Even the cafeteria staff or janitors can offer feedback on the story and characters of a film.

We therefore decided to create reels for our software designs. These were digital movies composed of simple hand-drawn imagery that were narrated and animated to show how users would interact with the new system. Each workflow would star a specific artist in the studio and show how his or her daily routine would be changed by the new way of working. These reels were refined and presented every six months to the entire studio in our main theater. This was a way to increase exposure for our plans and also to solicit feedback from anyone who might not otherwise be tracking what we were doing.

Internally, we also adopted the concept of engineering weeklies. This was a meeting where the entire software group gathered in a screen room once a week and individuals could present their latest work in progress. The demos could be rough and informal because they were for the rest of the software team, not our users. This meeting let everyone on the team show off what they were working on and helped to raise a greater sense of involvement. It also provided a fun way to keep everyone up to date on the latest state of the project.

## Director/Producer Model

Balance technical and creative visions. The best products come from listening to both sides of your brain. Find a good balance between technical complexity and artful design.

Developing a film-based software process illuminated a fundamental difference in the way films are made and the way software is developed. In the film business, you have a director who is concerned with the creative direction of the movie and a producer who is concerned with budget, schedules, and staffing. These two people are peers with a natural tension between their roles.

This classic tension played out when I was working onThe Incredibleswhere, during a discussion about spending more resources to achieve a better visual effect, the producer, John Walker, told the director, Brad Bird, that he was just trying to make sure they could cross the finish line. To which Brad Bird responded that he was trying to make sure they crossed the line in first place.

By contrast, in the world of software there is normally a single person who is responsible for assembling the final product, often called the product manager or product owner. There are also engineers and designers who are responsible for the art and interaction design for the product, but they very seldom have an equally powerful voice to the product manager.

While I was at Pixar, we experimented with a director/producer model to manage our new software effort. We did this in an attempt to better balance the conflicting constraints of building something great and building something functional and on time. Our producer came from the world of software and was responsible for things like defining the deployment platform, programming language, development processes and project schedules. Whereas our director came from the world of film-making and was concerned with things like specific animation features, user workflows, the look and feel of the product, etc.

Both perspectives are important and often overlap. For example, we had a lot of discussion early on about deploying on Macs versus Linux. This decision affected technical aspects like the programming language and UI toolkit we could use, but it also affected creative aspects like the user interface and interaction design that we could present to our customers.

[翻译失败，原文如下]

Having two equally-weighted voices controlling the direction of a product can certainly make for a difficult process at times, but finding the right balance between art and technology is critical to building amazing products. This of course was also Steve Jobs' philosophy at Apple, that the best ideas are formed at the intersection of computer science and art/design. The importance of this natural tension between art and technology is also what John Lasseter was referring to when he famously stated that art challenges technology, and technology inspires art.

---

> 本文由AI自动翻译，原文链接：[Lessons from Pixar: Why Software Developers Should Be Storytellers](https://review.firstround.com/lessons-from-pixar-why-software-developers-should-be-story-tellers/)
> 
> 翻译时间：2026-10-27 07:31
