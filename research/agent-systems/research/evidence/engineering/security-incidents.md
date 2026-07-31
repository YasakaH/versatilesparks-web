# Production Browser Agent Security Incidents

> **Source:** Palo Alto Networks Unit 42, Obsidian Security, Anthropic Claude Opus 4.5 research  
> **Date:** 2026-07-23  
> **Category:** Engineering — security

---

## Real-World Prompt Injection in Browser Agents

### Palo Alto Networks Unit 42: Web-Based Indirect Prompt Injection (IDPI)

Palo Alto Networks documented **web-based indirect prompt injection attacks observed in the wild** targeting AI systems. These are deployed by malicious websites and exhibit previously undocumented attacker intents including:

- Data exfiltration from connected systems
- Unauthorized API calls  
- Malware distribution through compromised agents
- Persistent access through injected instructions

**Attack technique:** Runtime assembly via dynamic execution — JavaScript modifies HTML at runtime to create hidden elements with Base64-encoded instructions. The agent reads these at runtime because it parses DOM content as part of perception.

**Key finding:** A single example contained **24 attempts of prompt injection within one page**.

Source: [Web-Based Indirect Prompt Injection Observed in the Wild](https://unit42.paloaltonetworks.com/ai-agent-prompt-injection/)

### Anthropic: Claude Opus 4.5 Prompt Injection Rates

Anthropic quantified the threat directly:
- **17.8% success rate** for single prompt injection attempt against Claude Opus 4.5 browser agent without safeguards
- **~1% success rate** with proper defenses (reinforcement learning + classifier improvements)

This means roughly 1 in 5.6 interactions with a naive agent will be hijacked if it perceives a page containing injected content.

Source: [Prompt Injection Attacks: Examples, Techniques, and Defence (blog.cyberdesserts.com)](https://blog.cyberdesserts.com/prompt-injection-attacks/)

### OpenAI: Instruction Hierarchy and Automated Red Teaming

OpenAI demonstrated that automated red-teaming can uncover instruction hierarchy vulnerabilities in frontier models, showing that even the most capable models struggle to reliably separate trusted instructions from untrusted data when both arrive through the same perceptual channel.

### HiddenLayer: Policy Puppetry Universal Jailbreak

HiddenLayer discovered the "Policy Puppetry" attack in April 2025 — formatting prompts as policy files (XML, INI, JSON) could bypass safety alignment across all major LLMs. The attacker never interacts with the LLM directly; instead, the model encounters the injected content during routine retrieval or perception operations.

Source: [Vectra AI — Prompt Injection: Types, Real-World CVEs](https://www.vectra.ai/topics/prompt-injection)

### Security Implications for Agent Architectures

Agents move **16 times more data than human users** (Obsidian Security), making every compromised agent a high-magnitude data exposure event. The blast radius scales with agent access: an agent granted access to Salesforce, M365, and Workday simultaneously does not expose a single user's data — it exposes the effective authority of every permission the agent holds across all connected systems.

Source: [Obsidian Security — Prompt Injection Attacks](https://www.obsidiansecurity.com/blog/prompt-injection)

---

*End of Production Security Incident Data*
