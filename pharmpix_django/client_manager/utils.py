# client_manager/utils.py
# gpi, pack_size, quantity_dispensed these column we have changed for type from N to A/N so need to change and do it in the code
FILE_LAYOUT = [
    {"field_name": "claim_number", "type": "N", "length": 20, "from": 1, "to": 20, "comments": "TRx Claim Number"},
    {"field_name": "claim_status", "type": "A/N", "length": 1, "from": 21, "to": 21, "comments": "Claims Status Values: P=paid X=reversal R=reject"},
    {"field_name": "int_claim_number", "type": "A/N", "length": 30, "from": 22, "to": 51, "comments": "Internal TRx Claim Number used to tie out reversals"},
    {"field_name": "carrier", "type": "A/N", "length": 30, "from": 52, "to": 81, "comments": "Client Carrier"},
    {"field_name": "account", "type": "A/N", "length": 30, "from": 82, "to": 111, "comments": "Client Account Code"},
    {"field_name": "group", "type": "A/N", "length": 30, "from": 112, "to": 141, "comments": "Client Group Code"},
    {"field_name": "plan_code", "type": "A/N", "length": 15, "from": 142, "to": 156, "comments": "Benefit/Plan code used to adjudicate the prescription"},
    {"field_name": "rx_number", "type": "N", "length": 20, "from": 157, "to": 176, "comments": "Prescription Number"},
    {"field_name": "fill_date", "type": "N", "length": 8, "from": 177, "to": 184, "comments": "Date Prescription was dispensed: YYYYMMDD"},
    {"field_name": "written_date", "type": "N", "length": 8, "from": 185, "to": 192, "comments": "Date Rx Written: YYYYMMDD"},
    {"field_name": "submitted_date", "type": "N", "length": 8, "from": 193, "to": 200, "comments": "Date Submitted: YYYYMMDD"},
    {"field_name": "submitted_time", "type": "N", "length": 6, "from": 201, "to": 206, "comments": "Time Submitted: HHMMSS"},
    {"field_name": "generic_brand_ind", "type": "A/N", "length": 1, "from": 207, "to": 207, "comments": "M, N, O, Y as defined by Medispan"},
    {"field_name": "compound_ind", "type": "A/N", "length": 1, "from": 208, "to": 208, "comments": "Compound Code Indicator as submitted by pharmacy; NCPDP standard"},
    {"field_name": "cob_ind", "type": "A/N", "length": 1, "from": 209, "to": 209, "comments": "Coordination of Benefits ind: Y/N"},
    {"field_name": "refill_ind", "type": "N", "length": 4, "from": 210, "to": 213, "comments": "New/Refill Indicator: value >1 indicates refill"},
    {"field_name": "formulary_ind", "type": "A/N", "length": 1, "from": 214, "to": 214, "comments": "Formulary Indicator: Y/N"},
    {"field_name": "tier", "type": "A/N", "length": 2, "from": 215, "to": 216, "comments": "Tier level 1,2,3..."},
    {"field_name": "price_source", "type": "A/N", "length": 2, "from": 217, "to": 218, "comments": "Price Source: Item Submitted Basis of Cost"},
    {"field_name": "authorization_code", "type": "N", "length": 11, "from": 219, "to": 229, "comments": "Prior Auth Code when claim has an override"},
    {"field_name": "member_reimbursement", "type": "A/N", "length": 1, "from": 230, "to": 230, "comments": "Y or N; Y= Member submitted claim or N= submitted by pharmacy"},
    {"field_name": "ndc", "type": "N", "length": 11, "from": 231, "to": 241, "comments": "Drug Identifier"},
    {"field_name": "gpi", "type": "A/N", "length": 14, "from": 242, "to": 255, "comments": "Drug GPI Number"},
    {"field_name": "drug_name", "type": "A/N", "length": 30, "from": 256, "to": 285, "comments": "Full Drug Label Name"},
    {"field_name": "manufacturer", "type": "A/N", "length": 10, "from": 286, "to": 295, "comments": "Drug manufacturer"},
    {"field_name": "pack_size", "type": "A/N", "length": 11, "from": 296, "to": 306, "comments": "Drug package"},
    {"field_name": "drug_strength", "type": "A/N", "length": 10, "from": 307, "to": 316, "comments": "Drug strength"},
    {"field_name": "quantity_dispensed", "type": "A/N", "length": 12, "from": 317, "to": 328, "comments": "Drug Quantity Dispensed"},
    {"field_name": "days_supply", "type": "N", "length": 4, "from": 329, "to": 332, "comments": "Days of Supply for Rx"},
    {"field_name": "daw", "type": "N", "length": 1, "from": 333, "to": 333, "comments": "Dispense as Written"},
    {"field_name": "pharmacy_nabp", "type": "A/N", "length": 12, "from": 334, "to": 345, "comments": "Pharmacy NABP Number"},
    {"field_name": "pharmacy_npi", "type": "N", "length": 10, "from": 346, "to": 355, "comments": "Pharmacy NPI Number"},
    {"field_name": "pharmacy_name", "type": "A/N", "length": 50, "from": 356, "to": 405, "comments": "Pharmacy Name"},
    {"field_name": "pharmacy_chain", "type": "A/N", "length": 50, "from": 406, "to": 455, "comments": "Pharmacy Chain"},
    {"field_name": "pharmacy_network", "type": "A/N", "length": 50, "from": 456, "to": 505, "comments": "Pharmacy Network"},
    {"field_name": "member_id", "type": "A/N", "length": 16, "from": 506, "to": 521, "comments": "Member Id"},
    {"field_name": "person_code", "type": "N", "length": 3, "from": 522, "to": 524, "comments": "Member Person Code"},
    {"field_name": "member_first_name", "type": "A/N", "length": 35, "from": 525, "to": 559, "comments": "Member First Name"},
    {"field_name": "member_last_name", "type": "A/N", "length": 35, "from": 560, "to": 594, "comments": "Member Last Name"},
    {"field_name": "member_dob", "type": "N", "length": 8, "from": 595, "to": 602, "comments": "Member Date of Birth: YYYYMMDD"},
    {"field_name": "member_gender", "type": "A/N", "length": 1, "from": 603, "to": 603, "comments": "M=Male; F=Female"},
    {"field_name": "member_relationship", "type": "N", "length": 1, "from": 604, "to": 604, "comments": "1,2,3"},
    {"field_name": "prescriber_submitted_id", "type": "N", "length": 10, "from": 605, "to": 614, "comments": "Prescribing physician ID as submitted by pharmacy"},
    {"field_name": "prescriber_npi", "type": "N", "length": 10, "from": 615, "to": 624, "comments": "Prescribing physician NPI"},
    {"field_name": "prescriber_dea", "type": "N", "length": 9, "from": 625, "to": 633, "comments": "Prescribing physician DEA number; if available"},
    {"field_name": "prescriber_first_name", "type": "A/N", "length": 35, "from": 634, "to": 668, "comments": "Prescribing Physician First Name"},
    {"field_name": "prescriber_last_name", "type": "A/N", "length": 35, "from": 669, "to": 703, "comments": "Prescribing Physician Last Name"},
    {"field_name": "awp", "type": "S9(5)V9999", "length": 10, "from": 704, "to": 713, "comments": "UNIT AWP 4 implied decimal places"},
    {"field_name": "submitted_usual_and_customary_amt", "type": "S9(8)V99", "length": 10, "from": 714, "to": 723, "comments": "Usual and Customary Submitted by pharmacy"},
    {"field_name": "submitted_amt", "type": "S9(8)V99", "length": 10, "from": 724, "to": 733, "comments": "Total Amount Due submitted by pharmacy to TRx"},
    {"field_name": "submitted_ing_cost", "type": "S9(8)V99", "length": 10, "from": 734, "to": 743, "comments": "Total Ingredient Cost submitted by Pharmacy to TRx"},
    {"field_name": "submitted_dispensing_fee", "type": "S9(8)V99", "length": 10, "from": 744, "to": 753, "comments": "Total Dispensing Fee submitted by Pharmacy to TRx"},
    {"field_name": "client_paid_amt", "type": "S9(8)V99", "length": 10, "from": 754, "to": 763, "comments": "Total Amount to be Paid by client"},
    {"field_name": "client_ing_cost", "type": "S9(8)V99", "length": 10, "from": 764, "to": 773, "comments": "Total Ingredient Cost to be Paid by client"},
    {"field_name": "client_copay", "type": "S9(8)V99", "length": 10, "from": 774, "to": 783, "comments": "Total Copay Paid by client's member"},
    {"field_name": "client_deductible", "type": "S9(8)V99", "length": 10, "from": 784, "to": 793, "comments": "Total Deductible Paid by client's member; if applicable"},
    {"field_name": "client_coinsurance", "type": "S9(8)V99", "length": 10, "from": 794, "to": 803, "comments": "Total Coinsurance Paid by client's member; if applicable"},
    {"field_name": "client_sales_tax", "type": "S9(8)V99", "length": 10, "from": 804, "to": 813, "comments": "Total Sales Tax to be Paid to the pharmacy"},
    {"field_name": "client_dispensing_fee", "type": "S9(8)V99", "length": 10, "from": 814, "to": 823, "comments": "Total Dispensing Fee Paid by the client"},
    {"field_name": "diagnosis_code_qualifier", "type": "A/N", "length": 2, "from": 824, "to": 825, "comments": "Diagnosis Code Qualifier; if applicable"},
    {"field_name": "diagnosis_code", "type": "A/N", "length": 15, "from": 826, "to": 840, "comments": "Diagnosis Code; if applicable"},
    {"field_name": "reject_code1", "type": "A/N", "length": 2, "from": 841, "to": 842, "comments": "Claim Reject Code; NCPDP standard"},
    {"field_name": "reject_message1", "type": "A/N", "length": 50, "from": 843, "to": 892, "comments": "Local/custom reject message"},
    {"field_name": "reject_code2", "type": "A/N", "length": 2, "from": 893, "to": 894, "comments": "Claim Reject Code; NCPDP standard"},
    {"field_name": "reject_message2", "type": "A/N", "length": 50, "from": 895, "to": 944, "comments": "Local/custom response message"},
    {"field_name": "reject_code3", "type": "A/N", "length": 2, "from": 945, "to": 946, "comments": "Claim Reject Code; NCPDP standard"},
    {"field_name": "reject_message3", "type": "A/N", "length": 50, "from": 947, "to": 996, "comments": "Local/custom response message"},
    {"field_name": "group_contact_id", "type": "A/N", "length": 50, "from": 997, "to": 1046, "comments": "If applicable"},
    {"field_name": "employer_group_dept", "type": "A/N", "length": 20, "from": 1047, "to": 1066, "comments": "If applicable"},
    {"field_name": "employer_group_dept_name", "type": "A/N", "length": 50, "from": 1067, "to": 1116, "comments": "If applicable"},
    {"field_name": "employer_group_location", "type": "A/N", "length": 20, "from": 1117, "to": 1136, "comments": "If applicable"},
    {"field_name": "employer_group_location_name", "type": "A/N", "length": 50, "from": 1137, "to": 1186, "comments": "If applicable"},
    {"field_name": "filler", "type": "A/N", "length": 65, "from": 1187, "to": 1251, "comments": "For future use"},
]

# client_manager/utils.py (continued)
CLIENT_ACCOUNT_CODE_RULES = {
    "Allied": {"account_prefix": "SAPP"},
    "ASR": {"account_prefix": "6000"},
    "Lucent Health": {"account_prefix": "Lucent"},
}

# client_manager/utils.py (continued)
import logging
import re

logger = logging.getLogger(__name__)

def validate_txt_file(file_content, client_name):
    """
    Validate a .txt file content against the fixed-width layout and client-specific rules.
    Args:
        file_content (bytes): The content of the file.
        client_name (str): The name of the client (e.g., "Allied", "ASR", "Lucent Health").
    Returns:
        dict: {"is_valid": bool, "errors": list of error messages}
    """
    errors = []
    try:
        # Decode the file content
        content_str = file_content.decode('utf-8', errors='replace')
        lines = content_str.splitlines()
        if not lines:
            return {"is_valid": False, "errors": ["File is empty."]}

        # Validate each line
        for line_num, line in enumerate(lines, start=1):
            if len(line) < 1251:  # Total length as per layout
                errors.append(f"Line {line_num}: Line length is {len(line)}, expected 1251.")
                continue

            # Validate each field based on the layout
            for field in FILE_LAYOUT:
                field_name = field["field_name"]
                expected_length = field["length"]
                start = field["from"] - 1  # Convert to 0-based index
                end = field["to"]
                actual_content = line[start:end]
                actual_length = len(actual_content)

                # Check length
                if actual_length != expected_length:
                    errors.append(
                        f"Line {line_num}, Field {field_name}: Length is {actual_length}, expected {expected_length} (positions {start + 1}-{end})."
                    )

                # Check type (N = numeric, A/N = alphanumeric, S9 = signed numeric)
                field_type = field["type"]
                if field_type == "N" and actual_content.strip() and not actual_content.strip().isdigit():
                    errors.append(
                        f"Line {line_num}, Field {field_name}: Expected numeric value, got '{actual_content}' (positions {start + 1}-{end})."
                    )
                elif field_type.startswith("S9") and actual_content.strip():
                    # Basic check for signed numeric (allows for decimal and sign)
                    if not re.match(r'^-?\d*\.?\d*$', actual_content.strip()):
                        errors.append(
                            f"Line {line_num}, Field {field_name}: Expected signed numeric value, got '{actual_content}' (positions {start + 1}-{end})."
                        )

            # Client-specific account code validation
            if client_name in CLIENT_ACCOUNT_CODE_RULES:
                account_field = line[81:111]  # Account field (positions 82-111)
                expected_prefix = CLIENT_ACCOUNT_CODE_RULES[client_name]["account_prefix"]
                if not account_field.startswith(expected_prefix):
                    errors.append(
                        f"Line {line_num}: Account code '{account_field}' does not start with expected prefix '{expected_prefix}' (positions 82-111)."
                    )

        return {"is_valid": len(errors) == 0, "errors": errors}
    except Exception as e:
        logger.error(f"Error validating file for client {client_name}: {str(e)}", exc_info=True)
        return {"is_valid": False, "errors": [f"Error validating file: {str(e)}"]}