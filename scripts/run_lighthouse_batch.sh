#!/usr/bin/env bash
set -euo pipefail

ORIGIN="${1:?Usage: run_lighthouse_batch.sh ORIGIN MANIFEST OUTPUT_DIR}"
MANIFEST="${2:-dist/manus-routes.json}"
OUTPUT_DIR="${3:-lighthouse-mobile}"
WIDTH="${4:-390}"
HEIGHT="${5:-844}"
mkdir -p "$OUTPUT_DIR"

mapfile -t ROUTES < <(python3 - "$MANIFEST" <<'PY'
import json, sys
for route in json.load(open(sys.argv[1]))["routes"]:
    print(route["path"])
PY
)

for route in "${ROUTES[@]}"; do
  slug="${route#/}"; slug="${slug%/}"; slug="${slug//\//-}"; [ -n "$slug" ] || slug=home
  echo "Lighthouse mobile: $route"
  npx --yes lighthouse@12.8.2 "${ORIGIN%/}${route}" \
    --output=json --output-path="$OUTPUT_DIR/$slug.json" \
    --only-categories=performance,accessibility,best-practices,seo \
    --form-factor=mobile \
    --screenEmulation.mobile=true \
    --screenEmulation.width="$WIDTH" \
    --screenEmulation.height="$HEIGHT" \
    --screenEmulation.deviceScaleFactor=2 \
    --chrome-flags="--headless --no-sandbox --disable-dev-shm-usage" \
    --no-enable-error-reporting --quiet >/dev/null
done

python3 - "$OUTPUT_DIR" <<'PY'
import glob, json, os, statistics, sys
rows=[]
for path in sorted(glob.glob(os.path.join(sys.argv[1], "*.json"))):
    data=json.load(open(path)); cats=data["categories"]; name=os.path.basename(path)[:-5]
    rows.append({"route":"/" if name == "home" else "/"+name+"/", **{k:round(cats[k]["score"]*100) for k in ("performance","accessibility","best-practices","seo")}, "fcp":data["audits"]["first-contentful-paint"]["displayValue"], "lcp":data["audits"]["largest-contentful-paint"]["displayValue"], "cls":data["audits"]["cumulative-layout-shift"]["displayValue"], "tbt":data["audits"]["total-blocking-time"]["displayValue"]})
print(json.dumps(rows, indent=2))
for key in ("performance","accessibility","best-practices","seo"):
    values=[r[key] for r in rows]; print(f"{key}: min={min(values)} max={max(values)} avg={statistics.mean(values):.1f}")
PY
