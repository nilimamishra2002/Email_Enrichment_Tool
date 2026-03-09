from flask import Flask, render_template, request, send_file
import io
import pandas as pd
import sys

sys.path.append("src")

from parser import extract_domain, extract_name
from domain import detect_domain_type
from scraper import scrape_website
from search import search_company
from classifier import classify_sector
from confidence import calculate_confidence


app = Flask(__name__)

domain_cache = {}

last_results = []


def enrich_domain(domain):

    if domain in domain_cache:
        return domain_cache[domain]

    domain_type = detect_domain_type(domain)

    if domain_type == "Corporate":

        company, search_context = search_company(domain)

        website = scrape_website(domain)

        combined_text = website + " " + search_context

        sector, score = classify_sector(combined_text)

    else:

        company = "Personal Email"
        sector = "N/A"
        score = 0

    confidence = calculate_confidence(domain_type, sector, score)

    domain_cache[domain] = {
        "Company": company,
        "Sector": sector,
        "Confidence": confidence
    }

    return domain_cache[domain]


@app.route("/", methods=["GET", "POST"])
def index():

    results = []
    excel_file = None

    if request.method == "POST":

        email = request.form.get("email")
        file = request.files.get("file")

        if email:

            domain = extract_domain(email)

            if not domain:
                return render_template("index.html", results=[{
                    "Email": email,
                    "Name": "Unknown",
                    "Domain": "Invalid",
                    "Company": "Unknown",
                    "Sector": "Unknown",
                    "Confidence": "Very Low Confidence"
                }])

            name = extract_name(email)
            data = enrich_domain(domain)

            results.append({
                "Email": email,
                "Name": name,
                "Domain": domain,
                "Company": data["Company"],
                "Sector": data["Sector"],
                "Confidence": data["Confidence"]
            })

        elif file and file.filename.endswith(".csv"):

            df = pd.read_csv(file)
            emails = df["email"].tolist()

            for e in emails:

                domain = extract_domain(e)
                name = extract_name(e)
                data = enrich_domain(domain)

                results.append({
                    "Email": e,
                    "Name": name,
                    "Domain": domain,
                    "Company": data["Company"],
                    "Sector": data["Sector"],
                    "Confidence": data["Confidence"]
                })

        if results:

            df = pd.DataFrame(results)

            output = io.BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)

            excel_file = output

            global last_results
            last_results = results

    return render_template("index.html", results=results, excel_file=excel_file)


@app.route("/download", methods=["POST"])
def download():

    global last_results

    df = pd.DataFrame(last_results)

    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(
        output,
        download_name="email_enrichment_results.xlsx",
        as_attachment=True
    )
 


if __name__ == "__main__":
    app.run(debug=True)