# Security & Red-teaming

Adversarial robustness, jailbreaks, weight security, supply chain, prompt injection.

**4 live/paywalled entries** · catalog domain id: `security-redteam`

> Generated from `data/entries.json` — do not edit by hand. Run `python scripts/generate_domains.py`.

## Entry tier

No prerequisites beyond the domain's stated baseline.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Explaining and Harnessing Adversarial Examples](https://arxiv.org/abs/1412.6572) (Ian J. Goodfellow, Jonathon Shlens, Christian Szegedy, 2015) | paper | entry | — | The founding insight of adversarial ML — it reframed adversarial examples from a curiosity into a predictable failure mode of linearity that any high-dimensional model shares, which is why frontier LLMs inherit the same class of vulnerabilities. |

## Core

The load-bearing literature of the subfield.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Towards Deep Learning Models Resistant to Adversarial Attacks](https://arxiv.org/abs/1706.06083) (Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt et al., 2018) | paper | core | Explaining and Harnessing Adversarial Examples | Set the standard threat-model formalism and defense baseline for all subsequent robustness work; its PGD adversary is the tool of choice for measuring whether a defense is real or illusory. |
| [Robustness May Be at Odds with Accuracy](https://arxiv.org/abs/1805.12152) (Dimitris Tsipras, Shibani Santurkar, Logan Engstrom et al., 2019) | paper | core | Explaining and Harnessing Adversarial Examples | Formalizes the uncomfortable trade-off that robustness is not free — a finding with direct implications for how far safety-via-adversarial-training can take frontier models. |

## Deep

Formal treatments, frontier research, and specialized material.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Adversarial Examples Are Not Bugs, They Are Features](https://arxiv.org/abs/1905.02175) (Andrew Ilyas, Shibani Santurkar, Dimitris Tsipras et al., 2019) | paper | deep | Explaining and Harnessing Adversarial Examples | Deeply unsettling for alignment: it suggests robust and standard accuracy can genuinely conflict, and that models may latch onto features humans cannot even see — a caution for any safety claim resting on what a model 'actually learned'. |
