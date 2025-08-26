# Dataflow Evaluator Pre-Setup (Instructor/Admin)

To ensure quota-friendly, reusable evaluation for all students, complete these steps before students begin:

## 1. Create a Shared Pub/Sub Topic
- Name: `dataflow-shared-topic`
- Location: Same region as student resources (e.g., `asia-south1`)
- Grant publish/subscribe permissions to all student accounts

## 2. Create a Shared BigQuery Dataset
- Name: `dataflow_shared`
- Location: Same region as Pub/Sub topic
- Grant BigQuery Data Editor permissions to all student accounts

## 3. Communicate Resource Names
- Document the shared Pub/Sub topic and BigQuery dataset names in the student `README.md` and `solution_guide.md`

## 4. Quota/Cost Management
- Students only create their own BigQuery tables (not datasets or topics)
- All Dataflow jobs read from the same topic and write to their own table
- Instructor can periodically clean up old tables if needed

---

**This setup allows multiple students to use the same infrastructure without hitting project quotas.**
