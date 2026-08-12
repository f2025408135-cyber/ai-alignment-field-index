# Security & Red-teaming

Adversarial robustness, jailbreaks, weight security, supply chain, prompt injection.

**13 live/paywalled entries** · catalog domain id: `security-redteam`

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
| [Catastrophic Jailbreak of Open-source LLMs via Exploiting Generation](https://arxiv.org/abs/2310.06987) (Yangsibo Huang, Samyak Gupta, Mengzhou Xia et al., 2023) | paper | core | Jailbroken: How Does LLM Safety Training Fail? | Reveals that refusal behavior is an artifact of decoding configuration, not of the model's learned values — a reminder that safety alignment can be switched off by the deployment stack, not only by adversarial inputs. |
| [Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models](https://arxiv.org/abs/2308.03825) (Xinyue Shen, Zeyuan Chen, Michael Backes et al., 2023) | paper | core | Jailbroken: How Does LLM Safety Training Fail? | The ground-truth picture of jailbreaking in the wild — evidence that safety alignment, as deployed in 2023, failed against community-sourced attacks at an alarming rate. |
| [Open-Sourcing Highly Capable Foundation Models: An Evaluation of Risks, Benefits, and Alternative Methods for Pursuing Open-Source Objectives](https://arxiv.org/abs/2311.09227) (Elizabeth Seger, Noemi Dreksler, Richard Moulange et al., 2023) | paper | core | — | The key governance analysis of the open-weights question: whether to release frontier weights is the single highest-stakes distribution decision a lab makes, and this is the reference framework for weighing it. |
| [Jailbreaking Black Box Large Language Models in Twenty Queries](https://arxiv.org/abs/2310.08419) (Patrick Chao, Alexander Robey, Edgar Dobriban et al., 2023) | paper | core | Jailbroken: How Does LLM Safety Training Fail? | Demonstrates that black-box models can be jailbroken cheaply and without gradient access — meaning API-deployed frontier models are not protected by hiding their weights. |
| [Securing AI Model Weights: Preventing Theft and Misuse of Frontier Models](https://www.rand.org/pubs/research_reports/RRA2849-1.html) (Sella Nevo, Dan Lahav, Ajay Karpur et al., 2024) | paper | core | — | Weights are the crown jewels of AI: if stolen, they enable unrestricted misuse without lab oversight. This is the authoritative mapping of how they could be lost and how to protect them. |

## Deep

Formal treatments, frontier research, and specialized material.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Adversarial Examples Are Not Bugs, They Are Features](https://arxiv.org/abs/1905.02175) (Andrew Ilyas, Shibani Santurkar, Dimitris Tsipras et al., 2019) | paper | deep | Explaining and Harnessing Adversarial Examples | Deeply unsettling for alignment: it suggests robust and standard accuracy can genuinely conflict, and that models may latch onto features humans cannot even see — a caution for any safety claim resting on what a model 'actually learned'. |
| [DeepInception: Hypnotize Large Language Model to Be Jailbreaker](https://arxiv.org/abs/2311.03191) (Xuan Li, Zhanke Zhou, Jianing Zhu et al., 2023) | paper | deep | Jailbroken: How Does LLM Safety Training Fail? | Exemplifies the semantic, role-play class of jailbreaks that survive most input-filtering defenses — evidence that refusal policies can be circumvented by imaginative context construction. |
| [SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks](https://arxiv.org/abs/2310.03684) (Alexander Robey, Eric Wong, Hamed Hassani et al., 2023) | paper | deep | Jailbroken: How Does LLM Safety Training Fail? | A concrete proof that jailbreak defenses are possible, but also that they are heuristic — the brittleness insight behind the defense is itself a statement about how unnatural successful attacks are. |
| [Preventing Model Exfiltration with Upload Limits](https://www.lesswrong.com/posts/rf66R4YsrCHgWx9RG/preventing-model-exfiltration-with-upload-limits) (Ryan Greenblatt, 2024) | community | deep | Securing AI Model Weights: Preventing Theft and Misuse of Frontier Models | A concrete, engineering-level mitigation proposal from a leading AI-safety researcher — the kind of operational detail RAND-style threat assessments point to but don't specify. |
| [Aggressive Compression Enables LLM Weight Theft](https://arxiv.org/abs/2601.01296) (Davis Brown, Juan-Pablo Rivera, Dan Hendrycks et al., 2026) | paper | deep | Securing AI Model Weights: Preventing Theft and Misuse of Frontier Models | Undermines the common assumption that weight size makes theft impractical — a concrete technical result that raises the urgency of weight security controls. |
