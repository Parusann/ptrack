# ADR 0002: Direct carrier APIs first, aggregator as a fallback

- Status: Accepted
- Date: 2026-09-26

## Context

Tracking data is the core input. Access differs a lot by carrier:

| Carrier | Access |
|---|---|
| FedEx | Free Track API once a FedEx account is linked; 100K requests/day, 30 numbers per call |
| UPS | Free Tracking API tied to a UPS account; one number per call |
| DHL | Free Shipment Tracking - Unified key with no account; 250 calls/day; raw data must be deleted 30 days after delivery |
| Canada Post | Developer Portal Tracking API with a customer number |
| USPS, Purolator, Japan Post, others | No free direct access for a non-shipper |

The free aggregator tier (17TRACK) is a one-time allowance of 200 tracking numbers for new accounts, so it cannot be the main source.

## Decision

Route every tracking number through a router that:

1. Detects the carrier locally from the number's format and check digit.
2. Uses a direct carrier adapter when one exists.
3. Registers the number with the aggregator only when no direct adapter applies, always passing a confident carrier code.

All adapters implement one interface (`fetch`, `normalize`) and map carrier statuses onto one shared milestone model.

## Consequences

- Aggregator usage is metered and shown in the app.
- Adding a carrier means adding one adapter class and its tests.
- Updates come from scheduled polling, since none of the free direct APIs offer webhooks to non-account holders.
