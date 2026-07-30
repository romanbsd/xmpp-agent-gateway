---
marp: true
theme: default
paginate: true
size: 16:9
title: Give Every Agent an Address
description: A human-centered introduction to the XMPP Agent Gateway ProtoXEP
author: Roman Shterenzon
style: |
  :root {
    --ink: #f5f8ff;
    --muted: #a9b8ce;
    --navy: #07111f;
    --navy-2: #0b1a2d;
    --cyan: #4ddcff;
    --cyan-2: #00a7d6;
    --amber: #ffb65a;
    --coral: #ff7a66;
    --paper: #f4f1ea;
    --paper-ink: #132033;
  }

  section {
    box-sizing: border-box;
    width: 100%;
    height: 100%;
    padding: 58px 72px 54px;
    background:
      radial-gradient(circle at 85% 15%, rgba(77, 220, 255, .11), transparent 28%),
      linear-gradient(145deg, var(--navy) 0%, #081728 56%, #0d2034 100%);
    color: var(--ink);
    font-family: "Avenir Next", Inter, Arial, sans-serif;
    font-size: 28px;
    line-height: 1.25;
    letter-spacing: -0.015em;
  }

  section::after {
    color: rgba(255,255,255,.38);
    font-size: 14px;
    right: 28px;
    bottom: 20px;
  }

  h1, h2, h3 {
    font-family: "Avenir Next", Inter, Arial, sans-serif;
    letter-spacing: -0.045em;
    margin: 0;
  }

  h1, h2 {
    color: var(--ink);
  }

  h1 {
    font-size: 72px;
    line-height: .98;
    max-width: 980px;
  }

  h2 {
    font-size: 47px;
    line-height: 1.04;
    max-width: 1120px;
    margin-bottom: 32px;
  }

  h3 {
    font-size: 28px;
    color: var(--cyan);
    margin-bottom: 10px;
  }

  p { margin: 0 0 18px; }

  strong { color: #fff; }

  code {
    font-family: "SFMono-Regular", Consolas, monospace;
    background: rgba(77, 220, 255, .10);
    color: var(--cyan);
    padding: .12em .34em;
    border-radius: 7px;
  }

  .eyebrow {
    color: var(--cyan);
    font-size: 17px;
    font-weight: 800;
    letter-spacing: .16em;
    text-transform: uppercase;
    margin-bottom: 22px;
  }

  .lead {
    color: var(--muted);
    font-size: 30px;
    line-height: 1.35;
    max-width: 850px;
  }

  .giant {
    font-family: "Avenir Next", Inter, Arial, sans-serif;
    font-size: 94px;
    font-weight: 700;
    line-height: .95;
    letter-spacing: -.06em;
  }

  .cyan { color: var(--cyan); }
  .amber { color: var(--amber); }
  .coral { color: var(--coral); }
  .muted { color: var(--muted); }

  .bottom {
    position: absolute;
    left: 72px;
    right: 72px;
    bottom: 64px;
  }

  .two {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 70px;
    align-items: start;
  }

  .three {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 34px;
    align-items: start;
  }

  .five {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 22px;
    align-items: start;
  }

  .line {
    height: 2px;
    background: linear-gradient(90deg, var(--cyan), rgba(77,220,255,.06));
    margin: 30px 0;
  }

  .statement {
    font-family: "Avenir Next", Inter, Arial, sans-serif;
    font-size: 58px;
    line-height: 1.08;
    letter-spacing: -.045em;
    max-width: 1060px;
  }

  .quote {
    font-family: "Avenir Next", Inter, Arial, sans-serif;
    font-size: 45px;
    line-height: 1.16;
    max-width: 1020px;
  }

  .number {
    color: var(--cyan);
    font-family: "Avenir Next", Inter, Arial, sans-serif;
    font-size: 54px;
    font-weight: 700;
    margin-bottom: 10px;
  }

  .step {
    border-top: 3px solid rgba(77,220,255,.42);
    padding-top: 18px;
  }

  .step p {
    color: var(--muted);
    font-size: 20px;
  }

  .tag {
    display: inline-block;
    border: 1px solid rgba(77,220,255,.28);
    border-radius: 999px;
    padding: 8px 15px;
    margin: 0 8px 10px 0;
    color: #d7f7ff;
    font-size: 17px;
    letter-spacing: .02em;
  }

  .scenario {
    border-left: 3px solid var(--cyan);
    padding-left: 20px;
  }

  .scenario p {
    color: var(--muted);
    font-size: 21px;
  }

  section.paper {
    background: var(--paper);
    color: var(--paper-ink);
  }

  section.paper h1, section.paper h2,
  section.paper h3, section.paper strong { color: var(--paper-ink); }
  section.paper .muted, section.paper .lead { color: #596477; }
  section.paper .step { border-color: #1a9ec2; }
  section.paper .step p { color: #596477; }
  section.paper .number, section.paper .cyan { color: #007f9f; }

  .cover {
    justify-content: flex-start;
  }

  .cover::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba(4,12,24,.96) 0%, rgba(4,12,24,.77) 38%, rgba(4,12,24,.14) 72%);
    z-index: 0;
  }

  .cover > * {
    position: relative;
    z-index: 1;
  }

  .cover h1 {
    margin-top: 130px;
    width: 600px;
  }

  .cover .lead {
    width: 560px;
    margin-top: 26px;
  }

  .image-left {
    background-position: center;
    background-size: cover;
  }

  .image-left::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba(4,12,24,.96) 0%, rgba(4,12,24,.86) 34%, rgba(4,12,24,.10) 70%);
    z-index: 0;
  }

  .image-left > * {
    position: relative;
    z-index: 1;
  }

  .image-left .lead,
  .image-bottom .lead {
    color: #ffffff;
    font-size: 32px;
    font-weight: 600;
    line-height: 1.32;
    text-shadow: 0 3px 18px rgba(0,0,0,.95);
  }

  .image-left .bottom,
  .image-bottom .lead {
    background: rgba(4,12,24,.60);
    border-radius: 14px;
    padding: 18px 22px;
    backdrop-filter: blur(4px);
  }

  .image-bottom {
    background-position: center;
    background-size: cover;
  }

  .image-bottom::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(4,12,24,.96) 0%, rgba(4,12,24,.64) 42%, rgba(4,12,24,.30) 75%, rgba(4,12,24,.16) 100%);
    z-index: 0;
  }

  .image-bottom > * {
    position: relative;
    z-index: 1;
  }

  .image-bottom h2,
  .image-bottom .lead {
    text-shadow: 0 2px 14px rgba(0,0,0,.72);
  }

  .address {
    margin-top: 120px;
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 66px;
    letter-spacing: -.05em;
    color: var(--cyan);
  }

  .arrow {
    color: rgba(77,220,255,.42);
    padding: 0 16px;
  }

  .flow {
    display: flex;
    align-items: center;
    margin-top: 105px;
    font-family: "Space Grotesk", Inter, sans-serif;
    font-size: 34px;
    font-weight: 600;
  }

  .flow span:not(.arrow) {
    border-top: 3px solid var(--cyan);
    padding-top: 18px;
  }

  .diagram {
    display: block;
    width: 100%;
    max-height: 470px;
    margin: 10px auto 0;
    object-fit: contain;
  }

  .pulse {
    display: inline-block;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--cyan);
    box-shadow: 0 0 0 9px rgba(77,220,255,.12), 0 0 28px var(--cyan);
    margin-right: 16px;
  }

  .closing {
    background:
      linear-gradient(90deg, rgba(4,12,24,.94), rgba(4,12,24,.38)),
      radial-gradient(circle at 75% 42%, rgba(77,220,255,.38), transparent 9%),
      radial-gradient(circle at 60% 30%, rgba(255,182,90,.22), transparent 8%),
      linear-gradient(145deg, #050c16, #0c2036);
  }

  .closing h1 {
    margin-top: 100px;
    max-width: 1000px;
  }

  .small {
    color: var(--muted);
    font-size: 18px;
  }
---

<!-- _class: cover -->
<!-- _paginate: false -->

![bg](./assets/agent-network-hero.png)

<div class="eyebrow">Proposed XMPP standard</div>

# Give every agent an address

<p class="lead">A practical way for people and AI agents to find each other, delegate real work, and stay in control across organizational boundaries.</p>

<!--
[Sources]
- Local source: protoxep-xmpp-agent-gateway.xml, Introduction and Requirements.
- Visual: OpenAI-generated original for this deck.
-->

---

<!-- _class: image-left -->
<!-- _backgroundImage: url("./assets/fragmented-agents.png") -->

<div class="eyebrow">The problem today</div>

## Powerful agents.<br>Stranded in silos.

<div class="bottom" style="width: 530px">
  <p class="lead">They have tools—but no shared way to find and trust one another, delegate work, ask follow-up questions, or track a long-running job.</p>
</div>

<!--
[Sources]
- Local source: protoxep-xmpp-agent-gateway.xml, Introduction.
- Visual: OpenAI-generated original for this deck.
-->

---

<div class="eyebrow">The hidden tax</div>

## Every handoff reinvents the same basics

<div class="three" style="margin-top: 58px">
  <div class="step"><div class="number">01</div><h3>Who are you?</h3><p>Identity and ownership are unclear.</p></div>
  <div class="step"><div class="number">02</div><h3>What can you do?</h3><p>Capabilities live in private catalogs.</p></div>
  <div class="step"><div class="number">03</div><h3>May I call you?</h3><p>Authentication is confused with permission.</p></div>
</div>

<div class="three" style="margin-top: 48px">
  <div class="step"><div class="number">04</div><h3>Did it start?</h3><p>A timeout may hide accepted work.</p></div>
  <div class="step"><div class="number">05</div><h3>Is it still running?</h3><p>Progress disappears between connections.</p></div>
  <div class="step"><div class="number">06</div><h3>Can I recover?</h3><p>Results are lost when sessions are lost.</p></div>
</div>

---

<!-- _class: image-left -->
<!-- _backgroundImage: url("./assets/travel-coordination.png") -->

<div class="eyebrow">Imagine this</div>

## One disrupted trip.<br>Five systems.<br>One calm traveler.

<div class="bottom" style="width: 600px;bottom:42px">
  <p class="lead" style="color:#fff;background-color:rgba(4,12,24,.82);padding:14px 20px;border-radius:14px;font-size:28px;font-weight:600">The travel agent asks policy what is allowed, delegates airline and rail rebooking, then confirms the calendar update.</p>
</div>

<!--
[Sources]
- Scenario is illustrative; capabilities are enabled by discovery, invocation, interactive input, cancellation, and federation profiles in the local ProtoXEP.
- Visual: OpenAI-generated original for this deck.
-->

---

<!-- _class: image-bottom -->
<!-- _backgroundImage: url("./assets/storm-response.png") -->

<div class="eyebrow">Or this</div>

## A storm crosses company boundaries.<br>The response should too.

<p class="lead" style="color:#fff;background-color:rgba(4,12,24,.82);padding:18px 22px;border-radius:14px;font-size:32px;font-weight:600;max-width:1040px">The forecast agent asks where outages are likely. Logistics delegates crew routing to field service; notification waits for human approval before alerting residents.</p>

<!--
[Sources]
- Scenario is illustrative; the local ProtoXEP defines addressable endpoints, federated policy, durable tasks, progress, and interactive input.
- Visual: OpenAI-generated original for this deck.
-->

---

<!-- _class: paper -->

<div class="eyebrow">The proposal</div>

<div class="statement">Use XMPP as the <span class="cyan">agent connection protocol</span> for addressable AI agents and their tools.</div>

<div class="line"></div>

<p class="lead">Not another agent runtime. Not a new model API. A shared network layer for identity, discovery, routing, permission, and durable work.</p>

---

<div class="eyebrow">Start with identity</div>

## An agent gets an address that already knows how to travel

<div class="address">weather@agents.example</div>

<div class="bottom">
  <span class="tag">stable identity</span>
  <span class="tag">routable</span>
  <span class="tag">federated</span>
  <span class="tag">policy-aware</span>
</div>

---

<div class="eyebrow">Then make it discoverable</div>

## Discovery flows naturally into delegation

<img class="diagram" src="./assets/discover-and-delegate.svg" alt="Sequence from service discovery to durable agent task acceptance and result">

<!--
[Sources]
- Local source: protoxep-xmpp-agent-gateway.xml, Finding a Gateway, Listing Agent Endpoints, Endpoint Information, and Invocation.
-->

---

<!-- _class: paper -->

<div class="eyebrow">Delegation, not messaging theater</div>

## “Please do this” becomes a durable task

<div class="five" style="margin-top: 88px">
  <div class="step"><div class="number">1</div><h3>Request</h3><p>Rebook the disrupted trip.</p></div>
  <div class="step"><div class="number">2</div><h3>Accept</h3><p>Return a durable task ID.</p></div>
  <div class="step"><div class="number">3</div><h3>Progress</h3><p>Rail option found.</p></div>
  <div class="step"><div class="number">4</div><h3>Interact</h3><p>Approve the €40 difference?</p></div>
  <div class="step"><div class="number">5</div><h3>Recover</h3><p>Fetch the confirmed itinerary.</p></div>
</div>

---

<!-- _class: image-bottom -->
<!-- _backgroundImage: url("./assets/durable-task.png") -->

<div class="eyebrow">Built for real life</div>

## The work outlives the connection

<p class="lead" style="color:#fff;background-color:rgba(4,12,24,.82);padding:18px 22px;border-radius:14px;font-size:32px;font-weight:600;max-width:1010px">The traveler crosses a tunnel mid-rebooking. On reconnect, the same task still has an identity, a state, and one authoritative itinerary.</p>

<!--
[Sources]
- Local source: protoxep-xmpp-agent-gateway.xml, Recovering After Notification Loss and Task Recovery.
- Visual: OpenAI-generated original for this deck.
-->

---

<!-- _class: paper -->

<div class="eyebrow">Recovery meets human judgment</div>

## A missed update does not break the task

<img class="diagram" src="./assets/recover-and-interact.svg" alt="Sequence showing a lost progress notification, authoritative recovery, interactive input, and retained result">

<!--
[Sources]
- Local source: protoxep-xmpp-agent-gateway.xml, Recovering After Notification Loss, Supplying Interactive Input, and Task Recovery.
-->

---

<div class="eyebrow">Plans change</div>

## Cancellation is a conversation with reality

<div class="two" style="margin-top: 74px">
  <div class="scenario">
    <h3>The meeting was cancelled</h3>
    <p>Ask the travel task to stop before it books the replacement.</p>
  </div>
  <div class="scenario">
    <h3>The booking already completed</h3>
    <p>The final result wins—and the system says so clearly.</p>
  </div>
</div>

<div class="bottom">
  <p class="lead">The standard models the race instead of pretending cancellation is instant.</p>
</div>

---

<!-- _class: paper -->

<div class="eyebrow">Failure without duplication</div>

## “I lost the reply” must not mean “do it again”

<div class="two" style="margin-top: 72px">
  <div>
    <div class="giant cyan">Retry the same request.</div>
  </div>
  <div>
    <p class="lead">A stable request identity lets the receiver return the original task instead of charging the card, sending the message, or placing the order twice.</p>
  </div>
</div>

---

<div class="eyebrow">Federation with boundaries</div>

## Reach across organizations.<br>Keep the boundaries.

<div class="two" style="margin-top: 66px">
  <div class="scenario">
    <h3>Local by default</h3>
    <p>Authenticated local agents can be visible according to tenant policy.</p>
  </div>
  <div class="scenario" style="border-color: var(--amber)">
    <h3 class="amber">Remote only by explicit trust</h3>
    <p>A federated connection proves who is speaking. It does not automatically grant discovery or invocation.</p>
  </div>
</div>

<div class="bottom">
  <span class="muted">Hidden, denied, and nonexistent resources receive privacy-safe treatment.</span>
</div>

---

<div class="eyebrow">An ecosystem bridge</div>

## MCP describes the tool.<br>XMPP gets the work there—and back.

<div class="two" style="margin-top: 65px">
  <div>
    <h3>MCP brings</h3>
    <p class="lead">Tool names, schemas, annotations, and result objects.</p>
  </div>
  <div>
    <h3>XMPP adds</h3>
    <p class="lead">Addressing, discovery, federation, authorization context, durable lifecycle, and recovery.</p>
  </div>
</div>

<div class="bottom">
  <p class="small">A bridge reports semantic loss rather than claiming every capability maps perfectly.</p>
</div>

---

<div class="eyebrow">What becomes possible</div>

## Agents can cooperate beyond a single app or vendor

<div class="three" style="margin-top: 58px">
  <div class="scenario"><h3>Operations</h3><p>Coordinate incidents across suppliers, utilities, and field teams.</p></div>
  <div class="scenario"><h3>Customer care</h3><p>Hand work to specialist agents while preserving one recoverable task.</p></div>
  <div class="scenario"><h3>Research</h3><p>Discover domain agents and run long analyses without keeping a session open.</p></div>
</div>

<div class="three" style="margin-top: 48px">
  <div class="scenario"><h3>Supply chain</h3><p>Ask inventory, transport, and customs agents to resolve one exception.</p></div>
  <div class="scenario"><h3>Personal assistants</h3><p>Coordinate travel, calendar, policy, and family preferences.</p></div>
  <div class="scenario"><h3>Agent marketplaces</h3><p>Build directories where visibility and access are policy-scoped.</p></div>
</div>

---

<!-- _class: paper -->

<div class="eyebrow">Why XMPP</div>

## The network primitives already exist

<div class="five" style="margin-top: 86px">
  <div class="step"><div class="number">＠</div><h3>Identity</h3><p>Stable addresses.</p></div>
  <div class="step"><div class="number">⌁</div><h3>Routing</h3><p>Across servers.</p></div>
  <div class="step"><div class="number">◎</div><h3>Discovery</h3><p>Find services.</p></div>
  <div class="step"><div class="number">⇄</div><h3>Federation</h3><p>Cross boundaries.</p></div>
  <div class="step"><div class="number">◉</div><h3>Presence</h3><p>Know what is reachable.</p></div>
</div>

---

<div class="eyebrow">Where the proposal stands</div>

## A ProtoXEP: concrete enough to build, open enough to improve

<div class="two" style="margin-top: 66px">
  <div>
    <h3>Already defined</h3>
    <p class="lead">Hosting, discovery, search, versioned capabilities, durable tasks, interactive input, cancellation, recovery, security, and MCP bridging.</p>
  </div>
  <div>
    <h3>What comes next</h3>
    <p class="lead">Implementations, interoperability testing, operational feedback, and standards review.</p>
  </div>
</div>

<div class="bottom"><p class="small">Current draft: XMPP Agent Gateway ProtoXEP 0.0.3. It has not yet been accepted or approved by the XMPP Standards Foundation.</p></div>

---

<!-- _class: closing -->
<!-- _paginate: false -->

<div class="eyebrow">The opportunity</div>

# A network of agents should behave like a network.

<div class="bottom">
  <p class="lead"><span class="cyan">Findable.</span> Addressable. Trusted. Recoverable.</p>
  <p class="small">XMPP Agent Gateway ProtoXEP · proposed standard</p>
</div>
