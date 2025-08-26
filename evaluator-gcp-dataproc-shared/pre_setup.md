# Dataproc Shared Cluster Evaluator Pre-Setup (Instructor/Admin)

To ensure quota-friendly, reusable evaluation for all students, complete these steps before students begin:

## 1. Create a Shared Dataproc Cluster
- Name: `dataproc-shared-cluster`
- Region: e.g., `asia-south1`
- Single node (1 master, 0 workers) is sufficient
- Grant job submission permissions to all student accounts

## 2. Create a Shared Cloud Storage Bucket
- Name: `dataproc-shared-bucket`
- Location: Same region as the cluster
- Grant read/write permissions to all student accounts

## 3. Communicate Resource Names
- Document the shared cluster and bucket names in the student `README.md` and `solution_guide.md`

## 4. Quota/Cost Management
- Students only upload their own input/output files
- All jobs run on the same cluster and use the same bucket
- Instructor can periodically clean up old files if needed

---

**This setup allows multiple students to use the same infrastructure without hitting project quotas.**
