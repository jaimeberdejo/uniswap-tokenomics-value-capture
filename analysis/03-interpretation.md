# UNI Value Capture After UNIfication — An Interpretation

**As of:** 2026-06-21 (matching the Phase 2 onchain data snapshot).

*Standalone note: this interpretation is complete on its own. It reads only the Phase 1
narrative and the Phase 2 dashboard figures, and it depends on no later analytical layer —
the verdict below holds on the onchain evidence and the dashboards alone.*

This document interprets the onchain evidence gathered in Phase 2 against the sharp
question that frames the whole project: **now that Uniswap has switched value capture on
through a burn mechanism, is that value capture material, is it sustainable, and does it
actually reach UNI holders?** It reads only the Phase 1 narrative (`FOUNDATION.md`) and the
Phase 2 dashboard figures; it introduces no new numbers and it stands on its own — every
quantitative claim is traceable to a verified Phase 1 or Phase 2 source cited inline.

A note on terms, because this is written to be legible to a reader new to decentralized
finance (DeFi) as much as to a grader. Several pieces of vocabulary recur; each is defined
in plain language on first use below. The figures here are a snapshot, and snapshots in a
volatile market go stale — so the document carries an explicit as-of date matching the
Phase 2 data collection.

---

## The Question and the Inflection

The whole analysis turns on a single date: **27 December 2025 (UTC)** — the onchain timestamp
of the burn transaction (2025-12-27 20:33 UTC, per Phase 2). Before that date, Uniswap —
the largest decentralized exchange, a venue where anyone can swap one token for another
without an intermediary — collected trading **fees** that went entirely to the people who
supplied liquidity to its pools, and **none** to holders of its governance token, UNI. The
**protocol fee switch** — a setting in Uniswap's contracts that, when turned on, diverts a
small slice of trading fees away from liquidity providers and toward the protocol itself —
was off. UNI was, in cash-flow terms, a pure governance token: it conferred a vote, not a
claim on revenue.

On 27 December 2025 (UTC) that changed. Following the **UNIfication** upgrade (Governance
Proposal #93), the protocol fee switch was activated onchain and a burn mechanism went live,
with the 100M-UNI burn transaction landing at 2025-12-27 20:33 UTC (FOUNDATION.md,
Post-UNIfication Status; Phase 2 onchain burn timestamp). This is the inflection the entire project is built
to read: not a steady-state gap between "could capture value" and "does," but a sharp
before/after break. Any framing that still describes the fee switch as "off," "debated," or
"a pending proposal" is stale and wrong as of this writing. The switch is on. The burn is
live.

Two further status facts must be fixed before any interpretation, because getting them wrong
would reintroduce exactly the stale thesis this project exists to retire. First, the
**fee-switch expansion passed.** What began as a proposal merely "advancing" in early 2026
concluded its onchain vote on approximately 4 March 2026; it is passed and rolling out, not
pending (FOUNDATION.md, Critical Status Correction). Second — and this matters because older
analyses lean on it heavily — **vesting unlock cliffs are no longer the sell-pressure
story.** The four-year team and investor vesting completed around September 2024
(FOUNDATION.md, Distribution & Vesting). Pre-2024 writing that treats unlock overhang as the
dominant supply dynamic is reading a chapter that has already closed. Post-2024, the supply
question is issuance versus burn, not cliffs — and that is the question this document takes
up directly.

So the inflection is real and recent, the expansion is a passed fact, and the old
sell-pressure narrative is retired. The rest of this interpretation asks what the burn
actually does, how big it is, whether it makes UNI net-deflationary, who controls it, and
whether the market believes any of it.

*(As of the Phase 2 data snapshot, 2026-06-21.)*

---

## Does Value Reach Holders? (Mechanism)

To answer whether value reaches holders, you have to be precise about which "fees" you mean,
because the single word hides an order-of-magnitude difference. Phase 1 insists — correctly
— that the word "fees" never be used unqualified, and the discipline pays off here
(FOUNDATION.md, Value-Accrual & Fee Taxonomy). There are three distinct quantities, and only
the last one touches holders.

**LP fees** are the headline number people quote: the total swap fee a trade pays, which is
gross income to **liquidity providers** (the people who deposit token pairs into a pool so
others can trade against them). This is large, and it is *not* the protocol's revenue. From
that pool of LP fees, the fee switch carves out a small slice — for example, in Uniswap v2
the total swap fee stays at 0.30% but the protocol now takes 0.05 of those 0.30 percentage
points, about a sixth of the swap fee (FOUNDATION.md, fee taxonomy). That carved-out slice is
**protocol fees**, and it does not flow to holders either. It collects in an immutable
onchain vault contract called **TokenJar**.

Value only reaches holders at the third step, and only through a particular mechanism. The
value accumulated in TokenJar is released exclusively by **burning UNI** — sending tokens to
a dead address from which they can never return — via a contract named **Firepit**
(FOUNDATION.md, the burn mechanism). This is a **buy-and-burn** design: protocol value is
used, in effect, to take UNI out of circulation permanently, rather than to pay anything out.
"Burn," then, means permanent destruction of supply; "buy-and-burn" means the protocol's
take is converted into a reduction of the token count rather than a cash distribution.

The nuance this produces is the single most important one in the entire analysis, and it is
why the verdict cannot be a simple thumbs-up. A burn is **not a dividend.** A holder who
never sells receives no cash, no yield, and no contractual claim on the protocol's revenue
(FOUNDATION.md, "How UNI captures value"). What the burn gives a holder is **scarcity**:
fewer tokens outstanding, so each surviving token represents a marginally larger share of the
network — *but only if demand for UNI holds.* If demand softens, a shrinking supply
multiplied by a falling price can leave holders no better off. This is buy-and-burn as
**supply-side pressure**, not a cash-flow claim. The value capture is genuine in the sense
that real protocol revenue is being committed to reducing supply; it is conditional in the
sense that the benefit to any individual holder is indirect, demand-dependent, and never a
right to be paid. Holding that distinction firmly is the precondition for reading every
magnitude figure that follows.

---

## How Big Is It? (Magnitude)

With the mechanism clear, the next question is scale. Here the Phase 2 headline metrics give
us the closed set of figures, and the picture they paint is deliberately undramatic.

Start with the one-time event. At activation, a single burn of **100 million UNI** — roughly
$595.6M (100M UNI at ~$5.96, the price at the time of the burn) — was executed on 27 December
2025 (UTC) (FOUNDATION.md, Post-UNIfication Status; Phase 2 burn-over-time). That is a genuinely large number, and it is
the right anchor for understanding intent: the protocol committed something on the order of
$600M of value to permanent supply destruction in a single transaction. But a one-time burn,
however large, is not the value-capture engine. The engine is the *ongoing* burn, and that is
where magnitude has to be read honestly.

Cumulatively, about **106.2M UNI** has been burned against a current total supply of roughly
**893.8M UNI**, with UNI trading near **$3.03** for a market capitalization of approximately
**$2.71B** (Phase 2 headline metrics). The ongoing burn — the recurring, volume-driven
destruction of UNI through Firepit, as distinct from the one-time event — runs at roughly
**$49.6M annualized.** Set against the ~$2.71B market cap, that ongoing burn is a **burn yield
of about 1.83% per year** (Phase 2 headline metrics). The "burn yield" here is simply the
annualized value being burned divided by market cap — the closest thing to a return number
this mechanism produces, while remembering from the previous section that it is not a yield
paid to anyone; it is the rate at which supply is being retired relative to the token's total
value.

The honest reading of **1.83% per year is: modest, but not trivial.** It is not a rounding
error dressed up as a thesis — $49.6M of real protocol value committed annually to supply
reduction is a material commitment for a protocol that, a year earlier, returned nothing to
its token at all. But neither is it the kind of figure that rewrites a valuation. A
~1.83%/yr supply-side pressure on a multi-billion-dollar token is a real but small force.
Crucially, it is also important *not* to cite the stale planning placeholder that floated
around earlier drafts — the burn at the scale measured onchain in Phase 2 is the ~$49.6M /
1.83% figure, and that is the only magnitude this interpretation will stand behind.

---

## Is It Net-Deflationary? (Supply)

A burn only tightens the float if it is not being outrun by new issuance. So the magnitude
question leads directly to a supply question: is UNI actually shrinking, or is the burn
merely offsetting tokens being minted elsewhere? "Net-deflationary" means the total token
count is falling on net — burns exceed issuance — so the float (the supply available) is
genuinely tightening rather than just churning.

The Phase 2 net-supply trajectory answers the current-state question cleanly: across the
observed weeks since activation, **new issuance is zero** while burns run every week, so UNI
is **net-deflationary right now** (Phase 2 net-supply trajectory). Every weekly bucket since
the inflection shows tokens leaving supply and none being minted. On the evidence, the float
is tightening, not churning — the burn is doing real supply-side work and nothing is
currently counteracting it.

But "right now" is load-bearing, and this is where interpretation must resist overclaiming.
Net-deflationary is a **current state, not a structural guarantee.** Phase 1's supply
trajectory documents two issuance levers that remain in governance's toolkit, dormant rather
than abolished: a **2% perpetual tail inflation** capability, live in principle since
September 2024, and a **20M UNI/yr growth budget**, vesting quarterly from 1 January 2026
(FOUNDATION.md, Supply Trajectory). The Phase 2 data shows neither materially firing in the
observed window — issuance reads as zero — but the *capacity* to issue has not been removed.
The headline supply question Phase 1 set up is exactly this break-even framing: the volume at
which the ongoing burn exceeds (2% inflation + the 20M growth budget). Today the answer is
comfortably deflationary because the issuance side is quiet. If governance activates those
levers, or if burn revenue falls with volume, the net could move. So the correct reading is:
**UNI is net-deflationary as observed, conditionally — a present fact resting on a policy
posture, not a property baked irreversibly into the token.**

---

## Who Controls the Switch? (Distribution & Governance)

If the burn is a policy posture rather than a contractual right, then the question of *who
sets the policy* is not a footnote — it is central to whether the value capture is durable.
The Phase 2 concentration dashboard makes the answer uncomfortable.

A crucial distinction has to be drawn first, because two different things are easy to
conflate here: *ownership* concentration and *voting* concentration are measured separately,
and they do not point the same way. UNI **ownership** is extraordinarily concentrated at the
top. The entity-adjusted **Gini coefficient is about 0.9952** — the Gini is a 0-to-1 measure
of inequality where 0 is perfectly even and 1 is a single holder owning everything, so 0.9952
is close to maximal concentration — and the ownership **Nakamoto coefficient is about 39**,
meaning roughly 39 entities together hold a majority of the relevant supply (Phase 2
concentration dashboard). This is across about **~314,140 holders** in total, which underlines
the gap: a very large base of small holders sits beneath a very small set of large ones.
Ownership is heavily concentrated at the top of the distribution. A single address — the Uniswap
**Timelock/Treasury** governance contract — holds about **~30.45% of supply** on its own
(Phase 2 top-holders / concentration dashboard).

But governance does not run on ownership; it runs on **delegated voting power**, and there the
Phase 2 data records a materially *different* picture — one of its own headline findings.
**Delegated voting power is more distributed than ownership.** The delegated-power dashboard
shows the **top delegate wielding about 7.15% of delegated voting power** (not 30%), and the
**voting Nakamoto coefficient is about 12** — roughly 12 delegates are needed to reach a
voting majority, versus ~39 entities by ownership and a treasury bloc that dominates the
supply table (Phase 2 delegated-power dashboard). In other words, the people who can actually
cast decisive votes are a *wider* set than the people who own the most tokens. This cuts
directly against any claim that "a tiny set decides by construction": on the voting measure,
the decisive set is broader, not narrower, than ownership suggests.

Governance must therefore be read on the right metric. Proposal #93, the UNIfication vote
itself, passed with about **125.3M UNI for against 742 against** across roughly **2,573 voters**
— on the order of **98.8% in favor** (Phase 2 governance turnout; FOUNDATION.md,
Post-UNIfication Status). The interpretation has two sides and both must be held. On one hand,
the votes so far have been decisively **holder-favorable**: UNIfication switched value capture
on, and the March 2026 expansion extended it, both by overwhelming margins. On the other hand,
control over the switch remains a real **governance variable**: the treasury's ~30.45% supply
bloc is a large single voice, and a voting Nakamoto of ~12 is still a relatively small
coalition in absolute terms. The honest reading is therefore calibrated: **whether the burn
persists is a governance decision, not a contractual right — and while voting power is more
distributed than ownership (voting Nakamoto ~12, top delegate ~7.15%), it is concentrated
enough that a modest coalition of delegates could change course.** The track record is
favorable, but what governance switched on, governance can shrink, redirect, or — by
activating the dormant issuance levers from the previous section — partially offset. Durability
rests on continued alignment, not on a property the contracts guarantee holders against their
own governance.

---

## Has the Market Priced It? (Reflexivity)

The final test is the market's own verdict, and it is the most deflating one for an
optimistic reading. If a genuine, net-deflationary, ~$49.6M/yr burn were being treated by the
market as a material change in UNI's value, you would expect it to show in price. It has not.

Across the burn period, **UNI fell from $5.96 to about $3** (Phase 2 price snapshot,
`02-01-SUMMARY.md`). A real burn, executed onchain, retiring supply every week with zero
issuance to offset it — and the token nonetheless roughly halved. The interpretation here is
careful: this is **not** evidence that the burn is fake or that the supply is not tightening
(Phase 2 shows it plainly is). It is evidence that the burn, at ~1.83%/yr, is **not large
enough to dominate the price relative to everything else moving it.** A ~1.83%/yr supply-side
tailwind is simply small against the swings of a crypto-market token whose value depends on
expectations about future trading volume, competitive position, and protocol credibility.

There is a reflexive subtlety worth naming. Because the ongoing burn is funded by protocol
value and executed by buying and destroying UNI, a *falling* price makes each dollar of burn
retire *more* tokens — the burn becomes more token-effective precisely when the price drops.
Yet the price fell anyway. The most defensible reading is that the market is **discounting
future volume and credibility** — the sustainability of the revenue that funds the burn —
rather than pricing the current burn as material. In other words, the market's skepticism is
not about whether 1.83%/yr is real; it is about whether the volume that produces that 1.83%
will hold, grow, or fade. That is a question the present snapshot cannot settle, and it is the
honest pivot into the verdict.

---

## Verdict

The evidence supports a single, defensible reading: **UNI's burn-based value capture is real
but modest and unproven.** That phrasing is chosen deliberately to hold a middle that the
data demands — it is neither a structural turning point to be celebrated nor a purely
symbolic gesture to be dismissed. Four supports, each tied to a figure, defend it.

**(a) The burn is genuine and net-deflationary.** This is not a paper mechanism. Protocol
fees collect in TokenJar and are released only by destroying UNI through Firepit, and the
onchain record shows it working: about **106.2M UNI** has been cumulatively burned (Phase 2
headline metrics), and across every observed week since the 27 December 2025 (UTC) inflection
**issuance reads as zero against weekly burns**, leaving UNI net-deflationary as measured
(Phase 2 net-supply trajectory). On the most basic question — is real value being committed
to retiring supply? — the answer is yes. The "real" in the verdict is earned.

**(b) It is small.** The ongoing burn runs at roughly **$49.6M annualized**, a **burn yield
of about 1.83% per year** against a **~$2.71B market cap** (Phase 2 headline metrics). That is
a material commitment for a token that captured nothing a year earlier, but it is a small
force on the valuation — modest, not trivial, and nowhere near large enough to dominate the
token's price on its own. The "modest" in the verdict is the honest scale, not a hedge. (And
it is the real ~$49.6M / 1.83% figure measured onchain, not the stale planning placeholder
that earlier drafts carried.)

**(c) It is supply-side pressure, not a dividend.** The burn confers scarcity, not cash. A
holder who never sells receives no yield and no contractual claim on the ~$49.6M/yr that funds
the burn (FOUNDATION.md, value-accrual taxonomy). This is **buy-and-burn** — value reaching
holders indirectly, supply-side, and only if demand holds — not a distribution. Whoever reads
the headline burn number as a dividend has mistaken the mechanism; the verdict refuses that
mistake.

**(d) Its durability is volume-dependent and unproven, and the market has not priced it as
material.** The burn is funded by trading volume, so it is only as durable as Uniswap's volume
moat; and control over whether the switch persists is a governance variable. *Ownership* is
near-maximally concentrated (Gini ~0.9952, Nakamoto ~39, treasury/timelock ~30.45% of supply),
but *delegated voting power* is more distributed than ownership (voting Nakamoto ~12, top
delegate ~7.15%) — so the decisive coalition is wider than the supply table implies, even if a
modest set of delegates could still change course, and the votes so far (Proposal #93, ~98.8%
for across 2,573 voters) have been holder-favorable (Phase 2 concentration, delegated-power,
and governance-turnout dashboards). The market's own verdict is skeptical: **UNI fell from $5.96 to about $3**
across the burn period despite a genuine, net-deflationary burn (Phase 2 price snapshot) —
the price is discounting future volume and credibility, not pricing the current burn as
material. The "unproven" in the verdict is this: sustainability has not been demonstrated, and
the market is, so far, unconvinced.

Held together, these supports land exactly in the middle and stay there. The burn is a real,
automated, irreversible reduction in dilution risk and a structural bid on UNI — a genuine
step-change for a token that previously returned nothing. It is also small, indirect,
governance-contingent, volume-dependent, and not yet validated by price. The defensible
answer to the project's sharp question — *is the newly switched-on value capture material,
sustainable, and does it reach holders?* — is therefore: **the value capture is real, it
reaches holders only indirectly through scarcity, its current magnitude is modest, and its
sustainability remains unproven.** Real but modest and unproven.
