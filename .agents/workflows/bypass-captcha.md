---
description: How to bypass CAPTCHAs for Facebook and Instagram on Railway
---

Since Railway runs in a headless environment without a user interface, it cannot solve CAPTCHAs or handle complex login challenges manually. 

Follow these steps to generate login cookies locally and upload them to Railway:

1. **Install Dependencies Locally**
   Ensure you have the required packages installed on your local machine:
   ```bash
   pip install selenium selenium-stealth python-dotenv
   ```

2. **Run the Cookie Setup Script**
   Run the following command in your local terminal:
   ```bash
   python Mall_Ai_Dashboard/setup_cookies.py
   ```

3. **Log In Manually**
   - A visible browser window will open.
   - Enter your credentials for Facebook and/or Instagram.
   - Solve any CAPTCHAs or 2FA prompts that appear.
   - Once the script detects you are logged in, it will save `fb_cookies.pkl` and/or `ig_cookies.pkl` in the `Mall_Ai_Dashboard` directory.

4. **Upload Cookies to Railway**
   - Add the newly created `.pkl` files to your git repository:
     ```bash
     git add Mall_Ai_Dashboard/fb_cookies.pkl Mall_Ai_Dashboard/ig_cookies.pkl
     git commit -m "Add login cookies for Railway"
     git push
     ```
   - Alternatively, if you are using a Persistent Volume on Railway, upload the files directly to the `Mall_Ai_Dashboard` directory.

5. **Redeploy**
   Once the cookies are present on Railway, the scrapers will automatically use them to bypass the login screen entirely.
