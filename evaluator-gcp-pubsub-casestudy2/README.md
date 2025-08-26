# GCP Pub/Sub Case Study 2: Financial Transaction Processing

## Scenario
You are working for a fintech startup. Your team must process real-time financial transactions using Pub/Sub, ensuring that all published messages conform to a strict schema for compliance.

## Tasks
1. **Define a Pub/Sub schema** (AVRO or Protocol Buffer) for transaction data (fields: transaction_id, user_id, amount, currency, timestamp).
2. **Create a Pub/Sub topic** and enforce the schema on published messages.
3. **Publish 5 valid transaction messages** to the topic.
4. **Publish a message with an invalid data type** (e.g., amount as a string) and verify it is rejected.
5. **Create a subscription** and pull all valid messages, logging their content.

## Verification
- The evaluator will check for schema enforcement, topic setup, valid/invalid message handling, and subscription delivery.

## Notes
- Use OIDC authentication (no static keys).
- All actions and results must be logged to `test_report.log`.
- Do not delete or overwrite resources from other students.

---
See `solution_guide.md` for step-by-step instructions and `pre_setup.md` for instructor setup.
