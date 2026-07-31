# Execution Surfaces

## 1. Same Architecture, Different Environments

The Agent Execution Model doesn't change based on what you're automating. The loop is identical whether your agent interacts with a browser, a desktop application, a command-line interface, a REST API, a mobile app, or industrial IoT hardware.

What changes is the **execution surface** — the medium through which perception acquires signals and execution produces mutations. Six surfaces exist today, each with different signal availability, different mutation capabilities, and different failure modes. But the underlying architecture remains constant.

This is the universality insight: agent systems engineering is not a browser technology or a desktop automation framework. It's the study of how autonomous systems perceive, decide, act, verify, and learn across any environment they can interact with.

## 2. Browser Surface

Browsers remain the dominant execution surface for agent systems. They offer the richest signal ecosystem: accessible DOM trees, screenshots, console logs, network traffic, cookies, storage APIs, and event streams. Agents perceive through AXTree (structured, low-cost), vision (unstructured, high-coverage), WebMCP (native tool exposure — the emerging ideal), or hybrid combinations.

Three perception architectures coexist in production:

**AXTree-primary** reads the accessibility tree — semantic UI metadata at 200-400 tokens per snapshot, 3-10 second latency. Works beautifully on well-built sites. Fails on custom widgets, canvas elements, and non-ARIA-compliant interfaces.

**Vision-first** captures screenshots and describes them — 1,600+ tokens per frame, 15-60 seconds latency. Universal coverage but expensive. Works when AXTree can't help: complex layouts, canvas-rendered content, dynamic updates without ARIA annotations.

**Hybrid** combines both — AXTree as primary, vision as fallback when AXTree confidence drops below threshold. Production default for serious systems. Achieves the best balance of cost (500-1,500 tokens average), reliability (~90%+), and speed (5-15 seconds).

Economics matter especially for browsers because token costs accumulate fast: each navigation step, each form interaction, each verification check generates new observations. At scale, browser agent economics separate viable products from experimental code. Caching provides 70%+ hit rates. Model routing saves 85%+ on budget tasks. Trimming reduces token counts by 57% while improving decision quality.

The browser surface is where agent systems engineering proves itself because browsers are simultaneously the most data-rich and the most hostile environment an agent can encounter. Malicious pages contain prompt injection attempts. Anti-bot systems detect automation. Dynamic content invalidates cached observations. Sites with poor accessibility block AXTree-based perception entirely. Building reliable browser agents requires the full architecture — perception, decision, planning, execution, verification, recovery, learning — working together under adversarial conditions.

## 3. Desktop/GUI Surface

Desktop environments offer a different signal landscape: screen pixels, OS accessibility APIs (Windows UI Automation, macOS Accessibility, Linux AT-SPI), window titles, clipboard, keyboard/mouse events. Perception here means either reading structured UI metadata through accessibility APIs or capturing screenshots and interpreting them visually.

Desktop agents face unique constraints browsers don't. No standardized web-like surface — each application has different UI paradigms. No universal DOM equivalent — some apps expose accessibility trees, others only render pixels. No built-in security model — desktop agents operate with whatever permissions the user grants, which may include file system access, registry modification, or system configuration changes.

Execution on desktop surfaces means simulating input (mouse clicks, keyboard strokes, touch events) or invoking OS-level APIs. Some applications provide automation frameworks; most don't. Verification requires comparing expected vs. actual desktop state, often through screenshot analysis when accessibility metadata isn't available.

## 4. Terminal/CLI Surface

Terminal environments offer the most structured signal format but the narrowest action space. Perception reads stdout/stderr streams, exit codes, and process state. Execution runs commands and parses output. No graphics to interpret, no forms to fill, no dynamic content to render.

But terminal agents face their own challenges: command output formats vary wildly between tools. Some outputs are machine-readable; most are human-oriented text that requires parsing. Error messages follow no standard format. Exit codes are informative but don't capture all failure modes. Network timeouts, permission errors, resource constraints — all produce different observable symptoms depending on the specific tool and environment.

Terminal agents excel at infrastructure operations: system administration, log analysis, deployment orchestration, configuration management. Their structured input/output model makes them more predictable than browser or desktop agents, which is why they're common in CI/CD automation and DevOps workflows.

## 5. API/Service Surface

API surfaces offer the purest form of agent interaction: structured request/response protocols with typed schemas. Perception reads JSON responses, WebSocket events, or GraphQL queries. Execution makes HTTP requests or invokes service methods. No UI interpretation needed, no accessibility concerns, no visual ambiguity.

API agents are the easiest to build correctly because the contract is explicit. Input types are defined in OpenAPI specs. Output schemas are versioned. Error responses follow documented formats. Monitoring is built into the API layer through status codes, response times, and throughput metrics.

But API agents are also the most constrained. They can only interact with systems that expose APIs. They cannot automate legacy applications without API wrappers. They cannot handle scenarios where the required action has no programmatic interface.

## 6. Mobile and IoT Surfaces

Mobile surfaces blend characteristics of browsers (WebView components), desktop (app UIs), and custom interfaces (native controls, gestures). Perception uses view hierarchies, screenshots, and touch events. Execution simulates taps, swipes, and typing. Each app presents a unique interaction model.

IoT surfaces represent the physical world interface: cameras, lidar, IMU sensors, actuators, telemetry streams. Perception reads sensor data in real-time. Execution controls motors, adjusts parameters, triggers alarms. Latency requirements are far stricter than digital surfaces — industrial robots cannot tolerate the 15-60 second perception cycles that browser agents accept.

## 7. The Surface Abstraction

Each surface offers different signal types and mutation capabilities. But the agent architecture treats them uniformly:

- **Perception** always converts surface signals → structured observations with confidence scores
- **Decision Engine** always transforms observations → intents with model routing
- **Planning** always decomposes intents → actionable steps with dependencies
- **Scheduling** always orders steps → temporally allocated resource assignments
- **Execution** always carries out steps → observable mutations on the surface
- **Verification** always compares outcomes → pass/fail with evidence
- **Recovery** always handles failures → classified diagnosis with retry strategies
- **Learning** always improves performance → cached patterns and updated heuristics

The abstraction doesn't flatten differences — it standardizes responses to them. A browser agent and an IoT robot use the same eight-node architecture; they differ only in what signals their surfaces provide and what mutations they can produce. This uniformity is what lets knowledge transfer across domains: a pattern discovered optimizing browser perception modality selection might inform how IoT systems choose between camera and lidar feeds.

Without this abstraction, every surface gets treated as a separate problem domain requiring separate architectural thinking. With it, the entire field benefits from insights discovered on any single surface.

---

*End of Chapter 4 — Execution Surfaces*
