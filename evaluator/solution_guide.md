# Solution Guide: GCP Bucket and Pub/Sub Topic Creation

## Task
Create the following resources in your assigned GCP project:

1. **Cloud Storage Bucket**
   - Name: `eval-<student_id>` (replace `<student_id>` with your actual student ID)
   - Location: `asia-south1`
   - Enable **Uniform Bucket Level Access (UBLA)**
   - Enable **Object Versioning**

2. **Pub/Sub Topic**
   - Name: `eval-topic-<student_id>` (replace `<student_id>` with your actual student ID)

---


## Step-by-Step Solution (GCP Web Console Only)

### 1. Create the Storage Bucket
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. In the left menu, select **Storage > Buckets**.
3. Click **Create**.
4. Enter the bucket name as `eval-<student_id>` (replace `<student_id>` with your actual student ID).
5. Set the **Location type** to "Region" and choose `asia-south1`.
6. Click **Continue** through the options until you reach **Access control**.
7. Under **Access control**, select **Uniform** (Uniform bucket-level access).
8. Click **Create** to finish creating the bucket.

### 2. Enable Object Versioning
1. In the bucket list, click on your new bucket (`eval-<student_id>`).
2. Go to the **Configuration** tab.
3. Find **Object versioning** and click **Edit**.
4. Turn on **Object versioning** and save.

### 3. Create the Pub/Sub Topic
1. In the left menu, select **Pub/Sub > Topics**.
2. Click **Create Topic**.
3. Enter the topic ID as `eval-topic-<student_id>` (replace `<student_id>` with your actual student ID).
4. Click **Create**.

---

## Verification
- The evaluator will check for the existence and configuration of both resources.
- Make sure you use your assigned student ID in all resource names.
- You can run the evaluator workflow to verify your setup.

---

## Cleanup (Optional)
To delete the resources after evaluation:
1. Go to **Storage > Buckets**, select your bucket, and delete it.
2. Go to **Pub/Sub > Topics**, select your topic, and delete it.
