"""This script compares the licenses of the installed packages with the entries in the
whitelisted_licenses.txt file. If licenses are found, which have not been whitelisted, an
AssertionError will be thrown. The Error will contain information on which licenses to
check.

Raises:
      AssertionError: Thrown it non-whitelisted licenses have been found.
"""
import os
import piplicenses

# Initialize parser and args
parser = piplicenses.create_parser()
args = parser.parse_args()
packages = piplicenses.get_packages(args)

# Collect license information
licenses = {}
for p in packages:
    this_package_licenses = p.get("license_classifier", [])
    license_field = p.get("license", "")
    if license_field:
        this_package_licenses.append(license_field)
    licenses[p["name"]] = this_package_licenses

# Write to a text file
with open(r"codequality_reports\\package_licenses.txt", "w", encoding="utf8") as f:
    for package, license_list in licenses.items():
        license_str = ", ".join(license_list)
        f.write(f"{package}: {license_str}\n")

# Get whitelisted licenses from text file:
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
whitelisted_license_file = os.path.join(current_dir, "whitelisted_licenses.txt")
with open(whitelisted_license_file, encoding="utf8") as f:
    whitelisted_licenses = f.read().splitlines()

whitelisted_packages_file = os.path.join(current_dir, "whitelisted_packages.txt")
with open(whitelisted_packages_file, encoding="utf8") as f:
    whitelisted_packages = f.read().splitlines()

# Compare:
license_violations = []
for package, lics in licenses.items():
    if package in whitelisted_packages:
        continue
    if not any(lic for lic in lics if lic in whitelisted_licenses):
        license_violations.append(package)

# Raise error if non-whitelisted licenses have been found:
if len(license_violations) > 0:
    message = "\n".join([f"{p}: {str(licenses[p])}" for p in license_violations])
    raise AssertionError(
        "The program detected a license, which has not been whitelisted yet."
        + " Please check the license terms and add it to the whitelisted_licenses.txt file if ok."
        + " Packages and licenses to check are: "
        + message
    )
