
# Solution Guide: GCP Storage Case Study 2 (GCP Console)

## Prerequisites
- You are logged into the Google Cloud Console (https://console.cloud.google.com/).
- You have the bucket name (`ds-collab-shared`), your student ID, the collaborator’s email, and the download student ID (provided by your instructor).
- You have a CSV dataset on your local computer.

---

### 1. Create Your Folder and Upload a CSV
1. Go to **Storage > Buckets** in the Cloud Console.
2. Click on the bucket: `ds-collab-shared`.
3. Click **Create folder**. Name it with your student ID (e.g., `12345`).
4. Open your folder. Click **Upload files** and select your CSV file.
5. Wait for the upload to finish. Confirm your file appears in your folder.

---

### 2. Set a Retention Policy of 7 Days
1. In the bucket, click the **Retention policy** tab (top menu).
2. Click **Edit** and set the retention period to **7 days** (604800 seconds).
3. Save changes. (Note: Retention is set at the bucket level. If not allowed, ask your instructor.)
4. Record the retention policy setting in your log.

---

### 3. Share Your File with a Collaborator
1. In your folder, select your uploaded CSV file.
2. Open the **info panel** (top right).
3. Under **Permissions**, click **Add principal**.
4. Enter your collaborator’s email.
5. Set the role to **Storage Object Viewer**.
6. Click **Save**. Record this action in your log.

---

### 4. Download a File from Another Student’s Folder
1. In the bucket, open the folder named after the download student ID (e.g., `67890`).
2. Find a CSV file. Click the **three dots** > **Download**.
3. Save the file to your computer. Note the file size (shown in the console or after download).
4. Record the file name and size in your log.

---

### 5. Delete a Test File and Verify
1. In your folder, upload a test file (e.g., `testfile.csv`) if not already present.
2. Select the test file. Click **Delete** (trash icon) and confirm.
3. Refresh your folder to verify the file is gone.
4. Record this action and result in your log.

---

**Tip:** Log every action and result in your `test_report.log` for submission or troubleshooting.

If you get stuck, use the Cloud Console help or ask your instructor for guidance.
