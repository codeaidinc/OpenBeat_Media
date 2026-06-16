> 本書はリーガルチェック前のドラフト（標準構成）です。弁護士確認のうえ確定してください。
>
> *(This document is a pre-legal-review draft (standard configuration). Confirm with counsel before finalizing.)*

# Operator as Data Controller (Self-Hosting) — OpenBeat Media (Free OSS edition)

## 1. Product premise
OpenBeat Media (Free OSS edition, Apache-2.0) is a local static-site generator.

- A local "Studio" (Python/Flask) is used to edit articles and write static HTML to `output/`.
- **The default generated site collects NO personal data, sets NO cookies, and contains NO trackers, analytics, or outbound calls.**
- There are no AI features, no external API calls, and no telemetry.

## 2. Division of responsibility
| Role | Party | Scope |
|---|---|---|
| Platform provider (processor) | 合同会社CODEAID (CODEAID LLC) | Tool safety, explainability, logs, incident response, security, QA |
| Brand / controller (OEM) | Association (JASTJ / WFSJ) 【if applicable】 | Brand policy |
| Content responsibility | Journalists / editors | Accuracy and sourcing of articles |
| **Data controller of the published site** | **The self-hosting operator** | Published content, outbound links, any added third-party services |

## 3. Why the self-hosting operator is the data controller
The party that **publishes the generated static site on their own domain / hosting** (e.g. Cloudflare Pages) is the operator. Therefore the operator is the **data controller** for:

- **Published content**: article bodies, images, headlines, metadata.
- **Outbound links**: the appropriateness of external links in body text and sources.
- **Added third-party services**: any analytics (e.g. Google Analytics), externally hosted fonts, embeds (YouTube/X, etc.), or contact/newsletter forms the operator adds later. These may set cookies or process personal data.
- **Access logs**: handling of access logs / IP addresses collected by the hosting provider (e.g. Cloudflare).

CODEAID is not the data controller for elements the operator adds or publishes. CODEAID's responsibility is limited to the safety, quality, and security of the tool itself.

## 4. Personal data in the default configuration
- **Personal data collection: none** (no forms, login, or comments)
- **Cookies: none**
- **Analytics / trackers: none**
- **External resource loading: none** (the default theme uses inline CSS; no external fonts or CDNs)

In this default state, the operator generally has no additional GDPR / UK GDPR / Japan APPI obligations (privacy policy, consent, etc.). However, **the hosting provider's access logs** should be reviewed separately.

## 5. Obligations when the operator adds third-party services
As soon as analytics, external fonts, embeds, or forms are added, the operator must, **on their own**:

1. Publish a privacy policy (see `compliance/PRIVACY_TEMPLATE_en.md`).
2. Obtain consent for cookies / tracking (opt-in by default in the EU and UK).
3. Identify a lawful basis for processing (GDPR Art. 6, etc.).
4. Enable the optional privacy notice partial (`themes/default/_privacy_notice.html`).

## 6. Contact and scope
- Questions about the tool: 合同会社CODEAID (CODEAID LLC) 【contact email / channel】
- Applicable markets: EU, UK, Japan
- Related documents: `PRIVACY_TEMPLATE_en.md` / `SECURITY_NOTES.md` / `PLD_FOSS_NOTE.md` / `SBOM.md`

## Gaps (to complete)
- 【Official name / applicability of the Association (OEM controller)】
- 【CODEAID contact channel】
- 【Hosting provider name and whether a data processing agreement (DPA) for its access logs exists】
