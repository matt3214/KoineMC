# KoineMC
This project contains an algorith which translates the English Minecraft lang file into one based on Koine-era Greek using OpenAI APIs.

# Purpose
As a Christian, I want to become more familiar with God through His Holy Word. The New Testament is written in Koine Greek. 

Along with spoken and grammar training, I want to grow in familiarity with this language by immersing myself in a world that has comprehensible input avaialble within every square/cube-meter. 

# The Specifics

## The Lang File:

The Minecraft lang file is used to translate __all__ text that appears ingame, including in-game items, user interfaces, and even subtitles.

### Challenges

#### File Size
The file (as of 9/25/2023) has 6217 entries. At an estimated 50 tokens per entry, that means at least 50 \* 6000 \* 2 tokens of input and output, not to mention all the context that must be added to each entry to ensure the model outputs what we want. (500-1000 tokens)

This works out to about .03$ per 1K token \* (50 tokens + ~750 tokens) * 6127 entries = 150$ roughly.

#### Contexts

There is a huge variation in context between different entries. It makes sense to a human reader, but it might be hard for the robot to understand and intelligently translate in the context.

A few selections from the file can illustrate how varied the contexts are.

>
```json
"block.minecraft.soul_wall_torch": "Soul Wall Torch", // not so bad, could be confusing
"block.minecraft.spawn.not_valid": "You have no home bed or charged respawn anchor, or it was obstructed", // pretty clear
"block.minecraft.spawner": "Monster Spawner", // also not so bad, although will it recognize this to be a block?
```
```json
"gui.abuseReport.reason.imminent_harm.description": "Someone is threatening to harm you or someone else in real life.", // what is the context here?
"gui.abuseReport.reason.narration": "%s: %s", // how will it attempt to translate this?
"gui.abuseReport.reason.non_consensual_intimate_imagery": "Non-consensual intimate imagery", // πορνεία;;;
```
```json
"effect.duration.infinite": "∞", // what will it come up with here?
"effect.minecraft.absorption": "Absorption",
"effect.minecraft.bad_omen": "Bad Omen",
```
```json
"parsing.long.invalid": "Invalid long '%s'", 
"parsing.quote.escape": "Invalid escape sequence '\\%s' in quoted string",
"parsing.quote.expected.end": "Unclosed quoted string",
```

These varied contexts and precise technical insertions (escape characters, printf references '%s') complicate the translation effort for our LLM model.

With this said, some sections of the file are much easier to translate. We may benefit from approaching different sections of the file with different prompts or strategies for generating prompts.

## The Translation Philosophy

The goal is to create a translation that meets the following criteria:

> Accuracy: How closely the translation captures the original meaning in the context of Minecraft.
>
> Clarity: How easily the translation can be understood by someone familiar with Koine Greek.
>
> Elegance: How aesthetically pleasing and "natural" the translation sounds in Koine Greek.
>
> Brevity: The conciseness of the translation.

## The Algorithm(s)


