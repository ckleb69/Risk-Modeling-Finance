import pandas as pd
import numpy as np
from arch import arch_model
from statsmodels.stats.diagnostic import acorr_ljungbox
import warnings
warnings.filterwarnings("ignore")

# === 1. Load Student-t EGARCH results ===
res_path = r"Modelling/EGARCH_refit_failedtickers.csv"
data_path = r"C:\Kurtay Finance Project\Data\CLEANWRDS.csv"
save_path = r"C:\Kurtay Finance Project\Results\EGARCH_studentt2.csv"

res = pd.read_csv(res_path)
df = pd.read_csv(data_path)

# === 2. Ensure required columns exist ===
if "nu" not in res.columns:
    res["nu"] = np.nan
if "convergence_flag" not in res.columns:
    res["convergence_flag"] = 0

# === 3. Compute persistence ===
res["persistence"] = res["alpha[1]"] + res["beta[1]"]

# === 4. Classify stability ===
def classify(row):
    try:
        if (row["persistence"] < 2) and (row["beta[1]"] < 0.99) and (row["convergence_flag"] == 0):
            return "Stable"
        elif (0.99 <= row["beta[1]"] <= 1.0) and (row.get("nu", 3) > 2):
            return "Borderline"
        else:
            return "Unstable"
    except Exception:
        return "Unstable"

res["stability_class"] = res.apply(classify, axis=1)

# === 5. Identify unstable tickers ===
unstable_tickers = res.loc[res["stability_class"] == "Unstable", "ticker"].tolist()
print(f"\n⚠️  {len(unstable_tickers)} tickers flagged for re-fit:\n{unstable_tickers}")

# === 6. Re-fit unstable tickers with β fixed at 0.95 ===
refits = []
for t in unstable_tickers:
    print(f"\n================ Re-fitting {t} (β fixed = 0.95) ================")
    sub = df.loc[df["ticker"] == t, "log_ret"].dropna()
    if sub.empty:
        print(f"⚠️  {t}: no usable data.")
        continue

    x = sub * 1e6
    x = x.clip(lower=x.quantile(0.01), upper=x.quantile(0.99))

    try:
        am = arch_model(
            x,
            vol="EGARCH",
            p=1, q=1,
            mean="Constant",
            dist="t",
           
        )

        # --- set numeric starting vector ---
        start_vals = am.starting_values()
        if len(start_vals) > 3:
            start_vals[3] = 0.95  # fix beta

        res_fit = am.fit(disp="off", tol=1e-5)

        alpha = res_fit.params.get("alpha[1]", np.nan)
        beta  = res_fit.params.get("beta[1]", np.nan)
        nu    = res_fit.params.get("nu", np.nan)
        mu    = res_fit.params.get("mu", np.nan)
        omega = res_fit.params.get("omega", np.nan)
        persist = alpha + beta

        resid = res_fit.std_resid.dropna()
        lb_resid = acorr_ljungbox(resid, lags=[10], return_df=True)["lb_pvalue"].iloc[-1]
        lb_sqres = acorr_ljungbox(resid**2, lags=[10], return_df=True)["lb_pvalue"].iloc[-1]

        print(f"✅ {t}: β={beta:.3f}, ν={nu:.2f}, persistence={persist:.3f}")

        refits.append({
            "ticker": t,
            "mu": mu,
            "omega": omega,
            "alpha[1]": alpha,
            "beta[1]": beta,
            "nu": nu,
            "persistence": persist,
            "logL": res_fit.loglikelihood,
            "aic": res_fit.aic,
            "bic": res_fit.bic,
            "LB_pval_resid": lb_resid,
            "LB_pval_sqresid": lb_sqres,
            "convergence_flag": getattr(res_fit, "convergence_flag", 0),
            "stability_class": "Refit_Stable"
        })

    except Exception as e:
        print(f"❌ {t}: refit failed — {e}")
        continue

# === 7. Merge refitted results back ===
refit_df = pd.DataFrame(refits)
if not refit_df.empty:
    for t in refit_df["ticker"]:
        res.loc[res["ticker"] == t, :] = refit_df.loc[refit_df["ticker"] == t, :].values

# === 8. Save merged results ===
res.to_csv(save_path, index=False)
print(f"\n💾 Final results (with refits) saved to:\n{save_path}")

# === 9. Print summary ===
summary = res["stability_class"].value_counts()
print("\n📊 Final Stability Summary:")
print(summary)