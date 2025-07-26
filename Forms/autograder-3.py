import json, os
from bs4 import BeautifulSoup

marks = {}
feedback = {}

with open("/home/labDirectory/forms3/forms-3.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

def check(condition, key, message_if_true, message_if_false):
    marks[key] = 1 if condition else 0
    feedback[key] = message_if_true if condition else message_if_false

# Personal Info Fieldset
fieldset1 = soup.find_all("fieldset")
pi_fieldset = fieldset1[0] if len(fieldset1) > 0 else None
check(
    pi_fieldset and pi_fieldset.find("legend") and pi_fieldset.find("legend").text == "Personal Information",
    "Personal Information Fieldset",
    "Personal Information fieldset is present with legend.",
    "Personal Information fieldset is missing."
)

fn_input = soup.find("input", {"name": "full_name"})
check(
    fn_input and fn_input.get("type") == "text" and fn_input.has_attr("required"),
    "Full Name Input",
    "Full Name input is present and correctly configured.",
    "Full Name input is missing or incorrectly configured."
)

email_input = soup.find("input", {"name": "email"})
check(
    email_input and email_input.get("type") == "email" and email_input.has_attr("required"),
    "Email Input",
    "Email input is present and correctly configured.",
    "Email input is missing or incorrectly configured."
)

dob_input = soup.find("input", {"name": "dob"})
check(
    dob_input and dob_input.get("type") == "date" and dob_input.has_attr("required"),
    "Date of Birth Input",
    "Date of Birth input is present and correctly configured.",
    "Date of Birth input is missing or incorrectly configured."
)

# Car Preferences Fieldset
car_fieldset = fieldset1[1] if len(fieldset1) > 1 else None
check(
    car_fieldset and car_fieldset.find("legend") and car_fieldset.find("legend").text == "Car Preferences",
    "Car Preferences Fieldset",
    "Car Preferences fieldset is present with legend.",
    "Car Preferences fieldset is missing."
)

car_color = car_fieldset.find("input", {"name": "car_color"}) if car_fieldset else None
check(
    car_color and car_color.get("type") == "color" and car_color.has_attr("required"),
    "Car Color Input",
    "Car Color input is present and correctly configured.",
    "Car Color input is missing or incorrectly configured."
)

car_model = car_fieldset.find("select", {"name": "car_model"}) if car_fieldset else None
valid_options = {"sedan", "suv", "hatchback", "convertible"}
options = {o.get("value") for o in car_model.find_all("option")} if car_model else set()
check(
    valid_options.issubset(options),
    "Car Model Select",
    "Car Model select is present with correct options.",
    "Car Model select is missing or incorrect."
)

car_age = car_fieldset.find("input", {"name": "car_age"}) if car_fieldset else None
check(
    car_age and car_age.get("type") == "range",
    "Car Age Range",
    "Car Age range input is present.",
    "Car Age range input is missing or incorrectly configured."
)

electric = car_fieldset.find("input", {"name": "electric"}) if car_fieldset else None
radios = car_fieldset.find_all("input", {"type": "radio"}) if car_fieldset else []
check(
    electric and len(radios) == 2,
    "Electric Car Preference",
    "Electric car preference radio buttons are present.",
    "Electric car preference is missing or incorrect."
)

# Phone Preferences Fieldset
phone_fieldset = fieldset1[2] if len(fieldset1) > 2 else None
check(
    phone_fieldset and phone_fieldset.find("legend") and phone_fieldset.find("legend").text == "Phone Preferences",
    "Phone Preferences Fieldset",
    "Phone Preferences fieldset is present with legend.",
    "Phone Preferences fieldset is missing."
)

phone_color = phone_fieldset.find("input", {"name": "phone_color"}) if phone_fieldset else None
check(
    phone_color and phone_color.get("type") == "color" and phone_color.has_attr("required"),
    "Phone Color Input",
    "Phone Color input is present and correctly configured.",
    "Phone Color input is missing or incorrectly configured."
)

phone_brand = phone_fieldset.find("select", {"name": "phone_brand"}) if phone_fieldset else None
brand_options = {"apple", "samsung", "google", "oneplus"}
selected = {o.get("value") for o in phone_brand.find_all("option")} if phone_brand else set()
check(
    brand_options.issubset(selected),
    "Phone Brand Select",
    "Phone Brand select is present with correct options.",
    "Phone Brand select is missing or incorrect."
)

release_date = phone_fieldset.find("input", {"name": "release_date"}) if phone_fieldset else None
check(
    release_date and release_date.get("type") == "date" and release_date.has_attr("min"),
    "Phone Release Date Input",
    "Phone Release Date input is present and correctly configured.",
    "Phone Release Date input is missing or incorrectly configured."
)

submit = soup.find("button", {"type": "submit"})
check(
    submit,
    "Submit Button",
    "Submit button is present.",
    "Submit button is missing."
)

result = {
    "data": [
        {
            "testid": f"Form/{key}",
            "score": marks[key],
            "maximum marks": 1,
            "message": feedback[key],
        }
        for key in marks
    ]
}

# Print results
eval_path = os.path.join(os.path.dirname(__file__), "../.evaluationScripts/evaluate.json")
with open(eval_path, "w") as f:
    json.dump(result, f, indent=4)
