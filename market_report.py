name: Run Market Report Script

on:
  schedule:
    - cron: '0 3,15 * * *'  # Runs at 5 AM & 5 PM SAST (UTC+2 converted to UTC)
  workflow_dispatch:  # Allows manual trigger

jobs:
  run_script:
    environment: Market  # ✅ Ensure secrets are pulled from the correct environment
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set Up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Run Market Report Script
        env:
          EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}  # ✅ Ensure the email password is retrieved
        run: python market_report.py

      - name: Upload Infographic as an Artifact
        uses: actions/upload-artifact@v4
        with:
          name: financial-infographic
          path: financial_infographic.png
