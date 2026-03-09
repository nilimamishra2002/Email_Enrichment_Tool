import pandas as pd

from parser import extract_domain, extract_name
from domain import detect_domain_type
from scraper import scrape_website
from search import search_company
from classifier import classify_sector
from confidence import calculate_confidence


emails = pd.read_csv("../data/input.csv")["email"].tolist()

domains = list(set([extract_domain(e) for e in emails]))

domain_results = {}


for domain in domains:

    domain_type = detect_domain_type(domain)

    if domain_type == "Corporate":

        compan, search_context = search_company(domain)

        website_text = scrape_website(domain)

        combined_text = website_text + " " + search_context

        sector, score = classify_sector(combined_text) 

    else:

        company = "Personal Email"
        sector = "N/A"
        score = 0

    confidence = calculate_confidence(domain_type, sector, score)

    domain_results[domain] = {
        "Company": company,
        "Sector": sector,
        "Confidence": confidence
    }


results = []

for email in emails:

    domain = extract_domain(email)

    name = extract_name(email)

    data = domain_results[domain]

    results.append({
        "Email": email,
        "Name": name,
        "Domain": domain,
        "Company": data["Company"],
        "Sector": data["Sector"],
        "Confidence": data["Confidence"]
    })


df = pd.DataFrame(results)

df.to_excel("../data/output.xlsx", index=False)

print("All emails processed successfully")