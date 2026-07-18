# Production Story Specification

## Purpose

A production story makes a failure mode memorable. Readers forget statistics. They remember the time a scraper silently stored `₹0` for six days.

## Requirements

- Based on a believable incident
- One specific failure, one specific lesson
- Never sensationalized or exaggerated
- Maximum 400 words (V1: 200 words)
- Must include a concrete symptom a reader could recognize

## Structure

### Paragraph 1 — The Setup (2-3 sentences)

What was the automation supposed to do? Make it sound reasonable. The reader should think "I would have built that too."

### Paragraph 2 — The Failure (2-3 sentences)

What broke? Include a concrete symptom: what the developer saw, what the logs showed, what the business noticed.

### Paragraph 3 — The Root Cause (1-2 sentences)

Why did it break? This must be a specific technical failure, not a vague "something went wrong."

### Paragraph 4 — The Lesson (1-2 sentences)

What should the reader learn? Frame as an engineering principle.

## Example

```
[Setup] A retailer built a daily price monitoring system. The scraper ran every morning, extracted prices, and stored them in a database. It worked perfectly for six months.

[Failure] One morning, every price was ₹0. Marketing had launched a "Beat Any Competitor Price" campaign based on the previous day's data. They lost thousands of dollars before anyone noticed. The automation had crashed — it exited with code 0. Every monitoring system showed SUCCESS.

[Root Cause] A website selector had changed. Instead of extracting the price, the scraper extracted "Price unavailable" text. The parser converted it to 0. No exception. No timeout. No alert.

[Lesson] A successful exit code does not guarantee a successful business outcome. Validate your data, not just your process.
```

## Rules

- Never name real companies or products (use "a retailer," "a logistics company")
- Never exaggerate numbers (losing "thousands" is believable; "millions" is not without evidence)
- The failure must be realistic for the recipe's context
- Place the story after the Mental Model, before Learning Objectives
