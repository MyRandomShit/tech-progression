# Story Option 02 — *The Appointment*

> **Engine:** Every reform he ships is a **query he needed to run**. He rebuilds the data architecture of the Philippine state for six years for one reason: to find the eleven people who killed his wife. The country becomes ungovernable-by-thieves as a byproduct he never looks up from his desk to notice.
>
> **Register:** Institutional thriller. Le Carré in a government office with bad aircon. He never passes a law. He changes a dropdown, because he needed the dropdown to be searchable.

---

## Logline

A data-migration contractor loots the bank he was hired to modernize to buy his dying wife a trial slot she never lives to use — then buries himself under a dead man's name inside the agency that runs the country's transparency platform, where the only way to find the men who killed her is to make the entire Philippine government searchable. It takes six years. It works. Both things work.

---

## Cast

| | |
|---|---|
| **Protagonist** | **Rene Salcedo**, 38 → 44, operating as **"Ernesto 'Boy' Dimaano,"** contractor. Fourteen years of reading other people's undocumented databases. Ability: `Trace` (see `CHAR_PROTAGONIST.md`). He calls it *reading to the bottom*. |
| **X** | **Marisol Salcedo**, 36, his wife. Public-school music teacher. Diffuse midline glioma. The Singapore trial is self-pay, ₱6.2M, due in three weeks. |
| **The office** | **Bureau of Public Disclosure (BPD)** — the agency that operates the national open-data platform. 900 staff, four floors, a canteen, and total unglamorous authority over the schema every other agency must report in. |
| **The keepers** | **The Reconciliation Committee** — six chairs, no enabling law, a forty-year custody chain. No chair knows who filled the others before them. |
| **The state** | **The Cedula** — the Philippine Registry. Floors 9–11 of the same building. Officially: Office for Special Continuity Planning. |
| **The mirror** | **Dir. Paz Alonto-Rivera**, 50s, Cedula field director. Hunts an anomaly in her own building for four years. Holds the elevator for him twice. |
| **The replacement** | **Usec. Lina Buenafe**, 51 — competent, humorless, unbribable. Rene installs her in year three because a director who reads every memo is useless to him and a director who trusts her technical staff completely is a skeleton key. |

---

## Act I — The robbery, the Padron, the murder

Rene is legitimately contracted to migrate a mid-tier bank's forty-year record estate. He finds the **seam** in week two — a four-hour unreconciled float window between a legacy settlement ledger and its 2033 replacement, structurally invisible because each system considers it the other's problem. It is not a vulnerability. It is the honest kind of hole every system old enough to have history contains.

He takes ₱6.2M through it. He leaves the trail intact and timestamped, because he does not intend to get away with it; he intends to be in Singapore first.

The vault trip is one afternoon, for pre-2001 microfiche the migration scope required. Misfiled in a box bearing a dissolved department's acronym: **the Padron**.

Four hundred and ten pages. Not crimes — **accounts**. Which government depository accounts across four decades are not what their titles say. Which trust receipts, special education sub-accounts, calamity replenishment facilities, and confidential-fund clearing lines are pass-throughs, who signs each, what is retained at each hop.

Then the foundation calls: a medical-transport grant, an air ambulance, a nurse, a coordinator. Real. Beautiful paperwork. Rene, who has just committed a felony to afford exactly this, weeps at a stranger's kindness.

Marisol dies in transit. Oxygen delivery failure. The incident report is thorough, apologetic, and correct in every particular.

**The Padron gives him the plumbing. It does not give him the men.** The signatories are titles, not names — *Head, Special Disbursing Unit*; *Authorized Representative, Trust Receipts* — because that is how it survived four decades. To convert a title into a person, on a specific night, in a specific year, he would have to be able to search the Philippine government.

Nobody can search the Philippine government. Everything is public and nothing joins.

---

## Act II — Infiltration

He buys an identity — the hardest thing to forge in 2038, precisely because everything else is public — and becomes a mid-level contractor at the BPD.

He has chosen the one desk in the country from which the state is *queryable*, and he has chosen it for no civic reason whatsoever.

**How he finds them:** `Trace`, and he calls it competence. He opens a 2031 disbursement table and knows which eleven rows are fiction. He reads a scanned voucher and knows it was signed in a different room than the one it says. He sits in a coordination meeting and knows which of the four agency representatives has been in the Committee's presence, because the man is *downstream* of it, and Rene experiences that as a feeling about the man's shoes.

His colleagues think he is a savant. His performance reviews use the word "uncanny." He finds this mildly embarrassing.

---

## Act III — The queries, and what they accidentally did

| # | The query he needed | The "reform" he shipped to get it | What it accidentally fixed |
|---|---|---|---|
| 1 | *Find every disbursement mentioning a foundation, 1998–2038.* Impossible: the payee field is free text, forty years of it, no two spellings alike | **Data Quality Initiative**: eleven free-text fields converted to controlled vocabularies with mandatory counterparty identifiers. Sold as a cleanup ticket. Nobody objects | Four laundering routes become **unenterable**. Not illegal — impossible to type. Agencies stop using them the way you stop using a road that isn't there |
| 2 | *Read a record that stops changing.* Three times, a voucher he was reading was silently amended overnight | **Append-only revision history**, shipped as a platform reliability improvement | Every correction in the Philippine government becomes public and dated. Three governors are destroyed inside eighteen months — not by revelation, but because they can no longer *un-say* things |
| 3 | *Which other corporations share an incorporator with this foundation?* Requires joining the corporate registry to procurement to land titles to payroll. Five systems, five entity keys, none compatible | **Schema harmonization program.** Two years. Tedious beyond description. Everyone finds it boring; one man finds it holy | The citizen-auditor swarm — ten million people, four days off a week — can suddenly ask *which contractors share a director with a mayor's spouse's corporation?* Six seconds. The answer had been public for a decade in five pieces. **This is the single most consequential thing that happens in the book and Rene ships it to answer one question about one foundation** |
| 4 | *Place one man, in one city, on one night in 2033.* Confidential funds are exempt from itemization by law | **Standardized fleet, fuel, per-diem, facility-access and drone-flight logging**, mandated across all agencies, sold as a carbon-reporting and fleet-safety compliance package | Confidential funds stay confidential. Their **shadow** becomes public. Three agencies stop drawing them entirely because there is no longer any point. He got his man's hotel |
| 5 | *Stay in the building.* His director reads every memo and asks good questions | Engineered the promotion of **Usec. Lina Buenafe** — genuinely excellent, genuinely honest, and therefore genuinely willing to delegate technical authority to staff she has vetted once and trusted forever | Buenafe becomes the most effective agency head of her generation and is on the shortlist for a Cabinet post by year six. Rene installed her because he needed a boss who wouldn't read the release notes |

**Tonal rule:** each reform gets one short chapter from outside the building — a barangay treasurer who can finally refuse, a contractor who loses honestly, a journalist who runs one query and cries. Rene is in none of them. He is at his desk, at 11 PM, filtering for a surname.

---

## The dark ledger

| Who | What happened | Cost |
|---|---|---|
| **The coordinator**, 44 — signed the air ambulance manifest | Rene does not touch him. He *unmakes* him: eight months of true, sourced, devastating disclosures about unrelated things, until the man is unemployable, divorced, and living with his mother in Bulacan. Then Rene visits, once, and asks his question, and the man genuinely cannot remember the flight | Rene realizes he has spent eight months on a clerk. Tier 1 recedes another year |
| **Alma Cruzado**, 29, BPD data analyst | She notices someone is running unlogged joins at 2 AM and files a security concern. It is excellent work. Rene redirects the investigation onto a colleague, and Alma's finding is discredited and she is quietly moved to a regional office | She was the only other honest person on the floor. This is the book's first real crime and it costs him nothing, which is the point |
| **Atty. Dominador Rey**, 63, Committee counsel | Has to disappear. Knows Rene's face; has the resources to place it. Rene arranges it through the Committee's own protocol — feeds them evidence that Rey is negotiating with the Ombudsman, which is false, and which they believe | They handle it. Rene never sees a body and never asks. He sleeps fine, and notices that he sleeps fine, and files that observation the way he files everything |
| **The wrong one** | In year five he places a name at the center of the chain and moves against it — and is right about the provenance and wrong about the meaning. `Trace` reads what a person is downstream of, not what they chose. The man had been in the room. He had been in the room *objecting* | Rene finds the objection in a minute-book eleven months later. Four paragraphs. It is the worst chapter in the book |

---

## Ending

He is caught by an ordinary HR audit of contractor credentials — the unglamorous kind of process he spent six years perfecting.

The Committee offers the deal: return the Padron, name no one, take the robbery charge, and Marisol's death stays an accident in the record.

The Cedula offers the better one: **come upstairs.** Full immunity, a new name, work that matters. Alonto-Rivera makes the offer herself and does not know she is talking to the anomaly she has hunted for four years.

He refuses both. He pleads to the robbery, the true crime, the one he did. The Padron is never recovered — because by year six it describes plumbing that no longer exists. He made his own evidence obsolete. That was never the plan; it was residue.

**The last chapter is a BPD release note. Version 12.4. Four bullet points.** Nobody reads it. It is the most consequential document published in the Philippines that decade and it is signed by a contractor ID that was deactivated last Tuesday.

---

## `Trace` in this option

**Seeded as:** the man who is never wrong about a record. In a world where forgery is free and provenance is the only currency, the BPD has accidentally hired the only verification engine on earth and files him under *Contractual, Tier 2*.

**The building irony:** three floors above him, the Cedula runs biannual sweeps and reads a null where he sits. Four years. Nine wrong suspects. Dir. Alonto-Rivera holds a door for the contractor carrying a monitor and says *thank you, sir.*

**The examination (Act III):** a corrupted Cedula Architect, brought in for the anomaly, sits across from Rene in an interview room, looks at him, and goes white. Her report reads: *Subject is a Natural. Recommend release.* She resigns eleven days later.

**The reveal (final chapters):** she comes to find him in custody, off the books, because she has not been able to stop thinking about it. She explains what he is: a passive layer-agnostic read that has been running since he was a child and has been overwriting him for thirty years. He does not believe her until she tells him what to check.

**The knife:** the thing he checks is Marisol. He has photographs. He has always thought the not-remembering was grief.

He asks her when it started. She says it started before he met his wife, which means he never had her, not the way other people have people — he had six years of a woman whose face was being deleted while she was still in the room.

---

## Grounding notes

- Government IT reality: contractors who outlast administrations, systems nobody owns, procurement that funds the wrong thing well.
- Contractual/job-order employment as the invisible tier of the bureaucracy — and the reason a stolen identity survives six years.
- The 2038 public health system is genuinely good. The gap that kills Marisol is narrow, specific, and real. The country is not a hellscape.
- Charitable foundations as the polite circulatory system of Philippine politics.
- Confidential and intelligence funds; calamity-declaration procurement exemptions; trust receipts; special education fund sub-accounts.
- Identity in a transparency state: you cannot fake a person, only inherit one.

## Ties to *The Architects*

- **The Cedula** — proposed canon for the Philippine Registry, slotting beside The Bureau, The Ledger, The Index, The Table (`WORLD_LORE.md` §VI.1).
- The Architect who examines him = the corrupted Architect flagged in `the-architects/CHAR_PROTAGONIST.md`. Rene is the first of the two she sees.
- The Padron's 1974–1981 section uses a reconciliation convention that appears in no accounting tradition on earth. The Committee inherited it and has never asked. It is an arc of the Epoch (`WORLD_LORE.md` §VI.6) — and **the ring lost this file in 1987 and has been looking for it ever since.**
- Timeline: Rene's six years end in 2038, the year Linus first `Decompile`s. Last chapter here and first chapter there can share a week.

## Risks / open questions

- Dropdowns are not cinematic. Every reform needs a face within a page — this is the whole craft problem of the option.
- Six years is long; run the hunt as present tense and let the reform accrete as background.
- Ration the Cedula subplot to four scenes.
- Does Alonto-Rivera ever learn? (Recommend: last page, reading release note 12.4, recognizing nothing.)
- Does Alma Cruzado come back? (Recommend: yes, year six, and she is the HR audit.)
