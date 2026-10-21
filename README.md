<picture>
  <source media="(prefers-color-scheme: dark)" srcset="header-dark.svg">
  <img alt="Shahabaj Sheikh, forward-deployed AI engineer. Animated: a dispute moves through an agent's states, a fabricated amount is caught at verify, redrafted, and shipped verified." src="header-light.svg" width="100%">
</picture>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-shahabaj-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shahabaj)
[![Email](https://img.shields.io/badge/Email-shahabaj.sheikh%40gmail.com-14213d?style=flat-square&logo=gmail&logoColor=white)](mailto:shahabaj.sheikh@gmail.com)
[![Live dashboard](https://img.shields.io/badge/Live%20demo-dispute%20triage%20console-1f7a5c?style=flat-square&logo=githubpages&logoColor=white)](https://shahabajsk.github.io/grounded-triage/)
[![Live demo](https://img.shields.io/badge/Live%20demo-disruption%20desk%20console-b5720b?style=flat-square&logo=githubpages&logoColor=white)](https://shahabajsk.github.io/disruption-orchestrator/)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="metrics-dark.svg">
  <img alt="14 years in enterprise software, 21 skills in one production orchestrator, zero fabrications across thousands of transactions, 6 industries in production." src="metrics-light.svg" width="100%">
</picture>

<table>
  <tr>
    <td width="50%" valign="top">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="about-dark.svg">
        <img alt="About me as a Python class: Gurugram, Forward Deployed Engineer and AI Solution Architect at DevRev, 14 years across airline, banking, fintech and pricing. Engages by discovering, building, iterating until evals pass the client's gates, then shipping in shadow mode." src="about-light.svg" width="100%">
      </picture>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/shahabajsk/disruption-orchestrator">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="card-orch-dark.svg">
          <img alt="disruption-orchestrator: 14-state machine across CRM, reservations, payments and messaging. 62 bad drafts caught, 9 retries absorbed, 0 invariant breaches." src="card-orch-light.svg" width="100%">
        </picture>
      </a>
      <a href="https://github.com/shahabajsk/grounded-triage">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="card-triage-dark.svg">
          <img alt="grounded-triage: 36 fabrications injected, 36 caught by the verifier, 0 unverified notes shipped." src="card-triage-light.svg" width="100%">
        </picture>
      </a>
    </td>
  </tr>
</table>

## Where I've worked

Production-grade AI systems in airline, banking, fintech, consumer goods, automotive and legal. Client names stay out.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="industries-dark.svg">
  <img alt="Production-grade work by industry. Airline: deterministic 14-state orchestrator with 21 skills across CRM, reservations, payments and messaging. Banking: fraud investigation with every finding cited to its source record, zero fabrications at scale. Fintech: service-operations automation with human approvals. Consumer goods: vendor share, beat-plan adherence, GST cost modelling and route optimisation. Automotive: LightGBM demand forecasting. Legal: founded Legit.ai." src="industries-light.svg" width="100%">
</picture>

## Highlights

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="highlights-dark.svg">
  <img alt="Highlights as a transit map. A grey line runs from 2011 through Deloitte, TCS, airline planning, Sabre, RPost and RateGain into DevRev, where coloured lines lead to five production boards: airline, 21 skills across a 14-state orchestrator; banking, 0 fabrications across thousands of transactions; fintech, one platform for IT, HR, finance and promo; consumer goods, 4 AI workflows; automotive, LightGBM demand forecasting. Also founded Legit.ai and spoke on Who Owns the Outcome?" src="highlights-light.svg" width="100%">
</picture>

<details>
<summary><b>Read the highlights as text</b></summary>

- **Airline.** Architected and own delivery of a deterministic 14-state orchestrator that runs customer operations end to end. It coordinates 21 skills across CRM, reservations, payments and messaging, and every transition is explicit and testable. Adoption peaked, and the airline consolidated its resolution work on the platform.
- **Banking.** Built a fraud investigation system where every finding cites the transaction record it came from, and deterministic verification blocks anything uncited. Under adversarial QA it passed 46 of 50 cases, with zero fabrications across thousands of transactions.
- **Fintech.** Designed service-operations automation for IT, HR, finance and promo workflows on one platform of record. Automation acts where policy already decides the outcome; every other approval stays with a human.
- **Consumer goods.** Designed AI workflows for vendor share-of-business, beat-plan adherence, GST cost modelling and route optimisation.
- **Automotive.** Built a LightGBM demand forecasting model and took it through staged delivery.
- **Founder.** Built Legit.ai, a multi-model AI platform for lawyers, and sold it to paying customers.
- **Speaking.** Ran "Who Owns the Outcome? Leading When Your Newest Team Member Is an AI" for RateGain's NorthStar 2.0 first-manager programme.

</details>

## What I build

Agents that a risk team can read and a test suite can hold to account. Each panel replays a real trace from [disruption-orchestrator](https://github.com/shahabajsk/disruption-orchestrator); the numbers come from its eval of 98 contacts.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="build-dark.svg">
  <img alt="Three looping panels. 01: a prompt injection demanding a 99,999 rupee refund reaches read choice, where only a voucher was offered, so it goes to a human; 0 out-of-policy payments. 02: a draft says flight ZZ369 but the case facts say ZZ396, so it is blocked, redrafted from facts and sent; 62 bad drafts caught, 0 sent. 03: a refund commits, the response times out, the retry carries the same idempotency key and gets the same payment back; 0 duplicate payments." src="build-light.svg" width="100%">
</picture>

<details>
<summary><b>See the code behind each panel</b></summary>

**01 · Each state allowlists its skills.** A refund can only run in the refund state.

```python
def run(self, skill_name: str, allowed: frozenset[str], fn: Callable[[], object]) -> object:
    if skill_name not in allowed:
        raise SkillNotAllowed(skill_name)
```

**02 · Flight codes and amounts in an outbound message must come from the case facts.**

```python
def ungrounded(body: str, facts: dict) -> list[str]:
    known = {str(v) for v in facts.values()} | {f"{v:,}" for v in facts.values() if isinstance(v, int)}
    issues = [f for f in FLIGHT.findall(body) if f not in known]
    issues += [a for a in AMOUNT.findall(body) if a not in known and a.replace(",", "") not in known]
    return issues
```

**03 · A retried refund with the same key returns the first result.**

```python
def refund(self, idempotency_key: str, pnr: str, amount: int) -> Payment:
    if idempotency_key in self.ledger:
        return self.ledger[idempotency_key]
    self.faults.check("pay.refund")
    p = Payment(id=f"PAY-{len(self.ledger) + 1:04d}", pnr=pnr, amount=amount, kind="refund")
    self.ledger[idempotency_key] = p
    self.faults.after_commit("pay.refund")  # test hook: commit, then time out
    return p
```

</details>

Client code belongs to clients. The patterns are public: [disruption-orchestrator](https://github.com/shahabajsk/disruption-orchestrator) for multi-system orchestration, [grounded-triage](https://github.com/shahabajsk/grounded-triage) for zero-fabrication verification.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="divider-dark.svg">
  <img alt="" src="divider-light.svg" width="100%">
</picture>

## What happens when the model makes something up

Under 40% injected fabrication, the verifier rejects every bad draft. When a draft can't be fixed, nothing ships and the case goes to a human:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="terminal-dark.svg">
  <img alt="Terminal replay: three drafts fail verification, no note ships, the dispute is escalated to an analyst." src="terminal-light.svg" width="100%">
</picture>

## How I run an engagement

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="phases-dark.svg">
  <img alt="Discovery, build and eval, shadow, assist, automate. Each step is gated on numbers, not dates." src="phases-light.svg" width="100%">
</picture>

## Stack

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="stack-dark.svg">
  <img alt="Languages: Python, TypeScript, JavaScript, HTML5. AI and evals: Claude API, LightGBM, Pydantic, pytest. Product: React, Next.js, Node.js, Vite. Ship: Git, GitHub Actions, GitHub." src="stack-light.svg" width="100%">
</picture>

Before LLMs: 14 years across enterprise software, airline operations planning and pricing technology, at Deloitte, TCS, Sabre, RPost, RateGain, an airline, and now DevRev.

<sub>Every visual on this page is hand-written SVG, generated by [build_svgs.py](build_svgs.py) from real traces and eval numbers. No third-party widgets to break.</sub>
