---
title: Jev for Python engineers
title_original: Jev for Python engineers
date: '2026-10-02'
source: Vercel Blog
source_url: https://vercel.com/blog/jev-for-python-engineers
author: ''
summary: '[翻译失败，原文如下]


  It''s simply impossible to not hear about Jev. Seemingly everyone is tinkering with
  it in some way, from using it tomake trading decisions...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-04T07:59:41.537354'
---

[翻译失败，原文如下]

It's simply impossible to not hear about Jev. Seemingly everyone is tinkering with it in some way, from using it tomake trading decisions(what could possibly go wrong?)togenerating UIs with it(maybe we're onto something here!).

Jevis a new kind of AI model. You feed it data and ask it a set of multiple-choice questions, and it responds with its answers and how confident it is in each. Just like with any other model, Jev can and will make mistakes, but it will make them fast. ​

​The bottom line is: Jev is built for making narrow decisions. Whether it's accurateenoughfor your use cases is something you'll need to test.

The job of the Python team at Vercel is to make it easy for Python devs to tinker with Jev, among a few other things. So please welcome the latest release of theAI SDK for Python.

Install it withuv add aito use the new experimentalevaluate()API, which talks directly to Jev's nervous system.Then create anAI Gateway key, setAI_GATEWAY_API_KEY, and try this complete example:

```
1import asyncio2
3import ai4from ai.ops import experimental as jev5
6async def main():7    result = await jev.evaluate(8        ai.get_model("typesafe-ai/jev"),9        "You're Neil deGrasse Tyson",10        {"bigger": jev.ChoiceQuestion(11            instructions="Which is bigger, the Sun or the Earth?",12            criteria={"Sun": None, "Earth": None},13        )},14    )15    print(result.value["bigger"])16
17if __name__ == "__main__":18    asyncio.run(main())
```

Let's start with something Jev can't possibly get wrong.

Now, I'd like to explain what Jev is and how to make it work for you using a couple of examples. One is good and one is dumb. Ask Jev which is which. Let's have some fun!

## Copy link to headingJev ELI5

Jev is a universal classifier.

Classifiers are the classic primitive of good old machine learning. Say you want a spam filter. You train a classifier on lots of emails, each labeled as spam or not spam, and it learns to tell whether a freshly incoming email looks like spam.

Problem is, for every new classification task you'd have to collect and label new data, and then train a new classifier on it to tune its weights for that task. But you know what else has weights? Large language models! So the team behind Jev figured out how to turn an LLM into a classifier that you don't need to train for a specific domain, because it's already trained on a broad slice of human knowledge.

And while it started as an LLM, Jev still behaves like a classifier. It's cheap and fast, and it returns structured JSON instead of generating text. Its answers conform to the types and choices you define in your questions.

## Copy link to headingThe API

Jev'sofficial APIcouldn't be simpler, and to keep it that way, we implemented it in the Python AI SDK pretty much verbatim.

There's just one function,evaluate(), and a few supporting types. The function takes a model,state(can be a simple string or complex JSON), and a mapping of questions. A question is an instance of eitherChoiceQuestion(choose one answer),ScoreQuestion(rate the state on a scale you define), orNoulQuestion(estimate the probability that a statement is true).

For the complete API reference, refer your agent tothe docs. By now, we should have a good idea of what Jev is and how to use it. Time to see what we can build with it!

## Copy link to headingExample 1: Python or English?

This is a sensible example of using Jev: quite literally as a classifier.

About a year ago I had an idea to make the Python REPL agentic. I wanted it to have a great UX and thought it would be pretty cool if the REPL could tell whether I'm typing English or Python without me explicitly switching between chat and code.

I needed a classifier, so I spent two days training my own on a random selection of Python code and English text.

After a lot of sweat and dumb Opus 4.1 tokens, I concluded I'm not good enough to make a reliable classifier for Python vs. English. The UI felt jittery: typingif ihighlighted it as Python,if i iswitched it to English, andif i isflipped it back to Python. What seemed like a very simple problem turned out to be a really hard one.

Let's see how Jev does:

These are actual traces of Jev responses to "does this look like English or Python to you?" The code behind them isn't particularly interesting; it's basically the opening code snippet of this post with a different question.

What's more interesting is whether Jev could solve my REPL problem. And while it does seem to fare much better than my hand-rolled classifier did, it still has gaps. For example,"what's" + " uplooks like English to Jev, while it's quite obvious to me that it's a partially typed Python expression.

## Copy link to headingExample 2: Jev writes Python code

How about we regress and make Jev generate text like an LLM? Jev can't write, so one way to get it to type is to have it go letter by letter. At each step, it picks the next character from a set of letters, punctuation, and whitespace.Another waywould be to pick one word at a time from a vocabulary of someNEnglish words.

When I saw that, I immediately knew I had to test how good Jev is at writing Python code.

My first attempt used the "letters + Python keywords + whitespace" method, but I quickly realized Jev could barely type anifstatement that way. The only way to get anything sensible out of it was to make it generate an abstract syntax tree (AST) of the program instead.

The idea:

1. Take the user's prompt and use an LLM (GPT-5.6 in this case) to expand it into a concrete set of instructions for Jev. I found that without a detailed "plan", Jev struggles to implement even elementary tasks.
2. Make Jev build a Python AST through a series of choices. At each step, show it the current program, mark the field being filled, and offer the possible next nodes, like a function call, an arithmetic operation, or a variable.Each option comes with a preview of the code it would produce.
3. Apply each choice to the tree and render it back into Python. The host code handles punctuation and indentation; Jev decides the program's overall structure and contents. Repeat until Jev finishes the tree.

Take the user's prompt and use an LLM (GPT-5.6 in this case) to expand it into a concrete set of instructions for Jev. I found that without a detailed "plan", Jev struggles to implement even elementary tasks.

Make Jev build a Python AST through a series of choices. At each step, show it the current program, mark the field being filled, and offer the possible next nodes, like a function call, an arithmetic operation, or a variable.Each option comes with a preview of the code it would produce.

Apply each choice to the tree and render it back into Python. The host code handles punctuation and indentation; Jev decides the program's overall structure and contents. Repeat until Jev finishes the tree.

I did get Jev to generate syntactically valid (yet still mostly incorrect) Python code using this approach. But as you can see, making classifiers do the job of an LLM is quite challenging. The source code ison GitHubif you think you can do better.

## Copy link to headingTry Jev

Neither experiment worked quite as I'd hoped, but I'm still excited about Jev. We're only beginning to explore what this new class of models can do!

Try it today with theAI SDK for Pythonand let us know what you build. All you need isuv add aiand anAI Gateway key. Here's a ready to copy/paste prompt for your coding agent:

Create a minimal playground for Jev using Vercel's AI SDK for Python.

Initialize the project with `uv` (Python 3.12 or later) and install the SDK with `uv add ai`. Use `ai.get_model("typesafe-ai/jev")`. Write `main.py` that reads input line-by-line in a loop, calls `ai.ops.experimental.evaluate()` with a `ChoiceQuestion` to classify each line as Python or English, and prints the choice, probabilities, confidence, and latency. Exit cleanly on Ctrl+C.

[翻译失败，原文如下]

SDK docs: https://ai-python.dev/docs/reference/ops#experimentalevaluate

Prompt the user to create an AI Gateway key and explain how to set the `AI_GATEWAY_API_KEY` env variable. After that, the user can run `uv run python main.py`.

Gateway key setup docs: https://vercel.com/docs/ai-gateway/authentication-and-byok#quick-start

---

> 本文由AI自动翻译，原文链接：[Jev for Python engineers](https://vercel.com/blog/jev-for-python-engineers)
> 
> 翻译时间：2026-10-04 07:59
