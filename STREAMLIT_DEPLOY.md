# Streamlit Cloud — one-click deploy of the interactive explorer

The `steam-threshold-app/` directory is a Streamlit app that lets you re-run filters, explore distributions, and drill into individual developers and titles.

## Prerequisites

- A free [Streamlit Community Cloud](https://streamlit.io/cloud) account
- This repo connected to your GitHub (already done if you're reading this)
- Optionally: the private roster repo connected too, if you want the candidate drill-down

## Deploy steps

1. Go to <https://share.streamlit.io/> and click **"New app"**
2. Select repository: `mlpage910/indie-investor-pci-pipeline`
3. Branch: `main`
4. Main file path: `steam-threshold-app/app.py`
5. Click **"Advanced settings"**
   - **Python version:** 3.11
   - **Secrets** (paste this in, edit values):
     ```toml
     APP_PASSWORD = "pick-a-strong-password"
     ROSTER_REPO_TOKEN = "ghp_xxx"   # personal access token with read:repo scope on the private roster repo
     ```
6. Click **"Deploy"**

The app will be live at `https://<your-app-name>.streamlit.app/` within a couple of minutes.

## Password gating

The candidate-roster tab is gated by `APP_PASSWORD`. The public methodology tabs (filter sweeps, distribution explorer, threshold calibration) remain open.

To change the password later: edit the secret in the Streamlit Cloud dashboard — no redeploy needed.

## Pulling roster data at runtime

The app reads candidate CSVs from the private companion repo `mlpage910/indie-investor-pci-pipeline-roster` using `ROSTER_REPO_TOKEN`. To rotate the token:

1. Generate a new fine-grained PAT on GitHub with **Read** access to that one repo only
2. Update `ROSTER_REPO_TOKEN` in Streamlit Cloud secrets
3. Revoke the old token

## Data refresh

The deployed app uses whatever CSVs are pulled by `data_fetch/fetch_upstream.sh` at build time. To refresh:

1. Re-run the pipeline locally on a fresh scrape
2. Push the new roster to the private repo
3. Streamlit Cloud will redeploy on the next push to either repo
