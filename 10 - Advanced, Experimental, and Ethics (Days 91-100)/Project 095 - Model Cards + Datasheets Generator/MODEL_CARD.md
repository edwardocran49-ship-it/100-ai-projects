# Model Card: Risk Triage Classifier

**Owner:** Edward Ocran  
**Version:** 1.0

## Intended use

Prioritize records for qualified human review; never make an adverse decision automatically.

## Performance

- Primary metric: held-out F1 = 0.842
- Evaluation population: stratified validation records

## Limitations and risk controls

Performance may shift across institutions and rare subgroups. Human review is mandatory.

## Monitoring

Track drift, subgroup recall, overrides, and complaints each month.
