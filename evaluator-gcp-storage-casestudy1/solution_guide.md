
# Solution Guide: GCP Storage Case Study 1 (GCP Console)

## Prerequisites
- You are logged into the Google Cloud Console (https://console.cloud.google.com/).
- You have the bucket name (`media-assets-shared`), your student ID, and the team group email.
- You have at least 3 image files (JPG/PNG) on your local computer.

---

### 1. Upload 3 Images to Your Folder
1. In the Cloud Console, go to **Storage > Buckets**.
2. Click on the bucket name: `media-assets-shared`.
3. Click **Create folder**. Name it with your student ID (e.g., `12345`).
4. Open your new folder. Click **Upload files** and select at least 3 image files from your computer.
5. Wait for the upload to finish. You should see your files listed in your folder.

---

### 2. Set Object-Level Permissions for Your Team
1. In your student folder, select all your uploaded files (checkboxes).
2. Click **Show info panel** (top right) if not already open.
3. Under **Permissions**, click **Add principal**.
4. Enter the team group email (provided by your instructor).
5. Set the role to **Storage Object Viewer**.
6. Click **Save**. Your team now has access to your files.

---

### 3. List All Files and Log Names/Sizes
1. In your folder, review the list of files.
2. For each file, note the **Name** and **Size** columns.
3. Copy this information and paste it into a text file (for your log), or take a screenshot for your records.
4. You will later upload this log as `test_report.log` if required.

---

### 4. Move One File to the Archive Subfolder
1. In your student folder, click **Create folder** and name it `archive`.
2. Select one of your image files.
3. Click **Move** (top menu), choose the `archive` folder, and confirm.
4. The file should now appear in `12345/archive/`.

---

### 5. Generate and Test a Signed URL
1. In your folder, select one image file (not in `archive`).
2. Click the **three dots** (More actions) > **Create a signed URL**.
3. Set the expiration (e.g., 10 minutes) and click **Create**.
4. Copy the signed URL. Open it in a new browser tab or use `curl` to test.
5. If the image downloads or displays, the signed URL works. Record the result in your log.

---

**Tip:** Log every action and result in your `test_report.log` for submission or troubleshooting.

If you get stuck, use the Cloud Console help or ask your instructor for guidance.
