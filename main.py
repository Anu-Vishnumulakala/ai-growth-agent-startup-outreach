from src.utils import load_leads
from src.lead_analyzer import analyze_company
import pandas as pd

def parse_output(text): 
    result = {
        "summary": "",
        "score": "",
        "reason": "",
        "message": ""
    }

    lines = text.split("\n")

    for line in lines:
        if "Summary:" in line:
            result["summary"] = line.replace("Summary:", "").strip()

        elif "Relevance Score:" in line:
            result["score"] = line.replace("Relevance Score:", "").strip()

        elif "Reason:" in line:
            result["reason"] = line.replace("Reason:", "").strip()

        elif "Outreach Message:" in line:
            result["message"] = line.replace("Outreach Message:", "").strip()

    return result


def main():
    print("Loading leads...")
    df = load_leads("data/sample_leads.csv")

    results = []

    for _, row in df.iterrows():
        print(f"\nProcessing: {row['company_name']}")

        ai_result = analyze_company(
            company_name=row["company_name"],
            website=row["website"],
            industry=row["industry"]
        )

        parsed = parse_output(ai_result["analysis"])

        results.append({
            "Company": row["company_name"],
            "Website": row["website"],
            "Industry": row["industry"],
            "Score": parsed["score"],
            "Summary": parsed["summary"],
            "Reason": parsed["reason"],
            "Message": parsed["message"]
        })

    result_df = pd.DataFrame(results)

    print("\nFINAL TABLE:\n")
    print(result_df)

    # Save to CSV
    result_df.to_csv("output/results.csv", index=False)
    print("\nSaved to output/results.csv")


if __name__ == "__main__":
    main()
