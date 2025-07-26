import json, os
from bs4 import BeautifulSoup

marks = {
    "Form": {
        "Textarea for Comments": 0,
        "Dropdown Select for Feedback Type": 0,
        "Multiple Select for Product Type": 0,
        "Button to Reset the Form": 0,
        "Button to Submit the Form": 0,
    }
}

feedback = {
    "Form": {
        "Textarea for Comments": "",
        "Dropdown Select for Feedback Type": "",
        "Multiple Select for Product Type": "",
        "Button to Reset the Form": "",
        "Button to Submit the Form": "",
    }
}

with open("/home/labDirectory/forms2/forms-2.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

textarea = soup.find("textarea", {"name": "comments"})
if textarea and textarea.get("id") == "comments":
    marks["Form"]["Textarea for Comments"] = 1
    feedback["Form"]["Textarea for Comments"] = "Textarea for comments is present and correctly named."
else:
    feedback["Form"]["Textarea for Comments"] = "Textarea for comments is missing or incorrectly named."

feedback_type_select = soup.find("select", {"name": "feedback_type"})
if feedback_type_select:
    options = [opt.get("value") for opt in feedback_type_select.find_all("option")]
    required_options = {"general", "product", "service", "other"}
    if required_options.issubset(options):
        marks["Form"]["Dropdown Select for Feedback Type"] = 1
        feedback["Form"]["Dropdown Select for Feedback Type"] = "Dropdown select for feedback type is present with correct options."
    else:
        feedback["Form"]["Dropdown Select for Feedback Type"] = "Dropdown select for feedback type is missing required options."
else:
    feedback["Form"]["Dropdown Select for Feedback Type"] = "Dropdown select for feedback type is missing."

product_type_select = soup.find("select", {"name": "product_type", "multiple": True})
if product_type_select:
    options = [opt.get("value") for opt in product_type_select.find_all("option")]
    required_options = {"laptop", "desktop", "tablet", "smartphone", "other"}
    if required_options.issubset(options):
        marks["Form"]["Multiple Select for Product Type"] = 1
        feedback["Form"]["Multiple Select for Product Type"] = "Multiple select for product type is present with correct options."
    else:
        feedback["Form"]["Multiple Select for Product Type"] = "Multiple select for product type is missing required options."
else:
    feedback["Form"]["Multiple Select for Product Type"] = "Multiple select for product type is missing."

reset_button = soup.find("button", {"type": "reset"})
if reset_button:
    marks["Form"]["Button to Reset the Form"] = 1
    feedback["Form"]["Button to Reset the Form"] = "Reset button is present."
else:
    feedback["Form"]["Button to Reset the Form"] = "Reset button is missing."

submit_button = soup.find("button", {"type": "submit"})
if submit_button:
    marks["Form"]["Button to Submit the Form"] = 1
    feedback["Form"]["Button to Submit the Form"] = "Submit button is present."
else:
    feedback["Form"]["Button to Submit the Form"] = "Submit button is missing."

overall = {"data": []}
for category, val in marks["Form"].items():
    overall["data"].append({
        "testid": "Form/" + category,
        "score": val,
        "maximum marks": 1,
        "message": feedback["Form"][category],
    })

eval_path = os.path.join(os.path.dirname(__file__), "../.evaluationScripts/evaluate.json")
with open(eval_path, "w") as f:
    json.dump(overall, f, indent=4)

