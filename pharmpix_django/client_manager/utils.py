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
    {"field_name": "pack_size", "type": "N", "length": 11, "from": 296, "to": 306, "comments": "Drug package"},
    {"field_name": "drug_strength", "type": "A/N", "length": 10, "from": 307, "to": 316, "comments": "Drug strength"},
    {"field_name": "quantity_dispensed", "type": "N", "length": 12, "from": 317, "to": 328, "comments": "Drug Quantity Dispensed"},
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


# UMR Accumulator File Layout - Detail Records (Record Type = 2)
UMR_ACCUMULATOR_LAYOUT = [
    {"field_name": "record_type", "type": "A/N", "length": 2, "from": 1, "to": 2, "comments": "Record Type: 1=Header, 2=Detail, 3=Trailer"},
    {"field_name": "member_id", "type": "A/N", "length": 15, "from": 3, "to": 17, "comments": "ID that uniquely identifies the cardholder"},
    {"field_name": "person_code", "type": "A/N", "length": 2, "from": 18, "to": 19, "comments": "Person code identifying the patient"},
    {"field_name": "first_name", "type": "A/N", "length": 25, "from": 20, "to": 44, "comments": "First Name of the Patient"},
    {"field_name": "middle_initial", "type": "A/N", "length": 1, "from": 45, "to": 45, "comments": "Middle Initial of the Patient"},
    {"field_name": "last_name", "type": "A/N", "length": 35, "from": 46, "to": 80, "comments": "Last Name of Patient"},
    {"field_name": "birth_date", "type": "A/N", "length": 8, "from": 81, "to": 88, "comments": "Date of Birth of Patient. Format CCYYMMDD"},
    {"field_name": "policy", "type": "A/N", "length": 12, "from": 89, "to": 100, "comments": "UMR Policy assigned to Patient"},
    {"field_name": "class", "type": "A/N", "length": 3, "from": 101, "to": 103, "comments": "UMR Class assigned to Patient"},
    {"field_name": "gender", "type": "A/N", "length": 1, "from": 104, "to": 104, "comments": "Gender: M=Male, F=Female, U=Unspecified"},
    {"field_name": "relationship", "type": "A/N", "length": 2, "from": 105, "to": 106, "comments": "Relationship: EE=Employee, SP=Spouse, CH=Child, OT=Other"},
    {"field_name": "claim_number", "type": "A/N", "length": 11, "from": 107, "to": 117, "comments": "Sendor assigned claim number"},
    {"field_name": "deductible", "type": "N", "length": 13, "from": 118, "to": 130, "comments": "Patient Deductible Applied Amount. Format: S9(9)v99"},
    {"field_name": "out_of_pocket", "type": "N", "length": 13, "from": 131, "to": 143, "comments": "Patient Out of Pocket Applied Amount. Format: S9(9)v99"},
    {"field_name": "plan_payment", "type": "N", "length": 13, "from": 144, "to": 156, "comments": "Plan Payment applying to a Maximum. Format: S9(9)v99"},
    {"field_name": "date_of_service", "type": "N", "length": 8, "from": 157, "to": 164, "comments": "Date of Service. Format CCYYMMDD"},
    {"field_name": "benefit_period_begin_date", "type": "A/N", "length": 8, "from": 165, "to": 172, "comments": "Benefit Period Begin Date. Format CCYYMMDD"},
    {"field_name": "benefit_period_end_date", "type": "A/N", "length": 8, "from": 173, "to": 180, "comments": "Benefit Period End Date. Format CCYYMMDD"},
    {"field_name": "accum_type", "type": "A/N", "length": 10, "from": 181, "to": 190, "comments": "Benefit type: INFERT, SPECIALTY, DIABETIC"},
    {"field_name": "network", "type": "A/N", "length": 6, "from": 191, "to": 196, "comments": "Network status: IN, OUT, TIER1, TIER2, TIER3"},
    {"field_name": "vendor_defined1", "type": "A/N", "length": 20, "from": 197, "to": 216, "comments": "Vendor-specific data"},
    {"field_name": "vendor_defined2", "type": "A/N", "length": 20, "from": 217, "to": 236, "comments": "Vendor-specific data"},
    {"field_name": "vendor_defined3", "type": "A/N", "length": 20, "from": 237, "to": 256, "comments": "Vendor-specific data"},
    {"field_name": "vendor_defined4", "type": "A/N", "length": 20, "from": 257, "to": 276, "comments": "Vendor-specific data"},
    {"field_name": "vendor_defined5", "type": "A/N", "length": 20, "from": 277, "to": 296, "comments": "Vendor-specific data"},
    {"field_name": "coinsurance_out_of_pocket", "type": "N", "length": 13, "from": 297, "to": 309, "comments": "Patient Coinsurance Out of Pocket. Format: S9(9)v99"},
    {"field_name": "copay_out_of_pocket", "type": "N", "length": 13, "from": 310, "to": 322, "comments": "Patient Copay Out of Pocket. Format: S9(9)v99"},
    {"field_name": "inpatient_deductible", "type": "N", "length": 13, "from": 323, "to": 335, "comments": "Patient Inpatient Deductible. Format: S9(9)v99"},
    {"field_name": "deductible_indicator", "type": "A/N", "length": 1, "from": 336, "to": 336, "comments": "Deductible Applied: Y/N"},
    {"field_name": "out_of_pocket_indicator", "type": "A/N", "length": 1, "from": 337, "to": 337, "comments": "Out of Pocket Applied: Y/N"},
    {"field_name": "infertility_indicator", "type": "A/N", "length": 1, "from": 338, "to": 338, "comments": "Infertility Applied: Y/N"},
    {"field_name": "filler", "type": "A/N", "length": 162, "from": 339, "to": 500, "comments": "Filler - Default to spaces"},
]

# Header and Trailer layouts for UMR files
UMR_HEADER_LAYOUT = [
    {"field_name": "record_type", "type": "A/N", "length": 2, "from": 1, "to": 2, "comments": "Record Type: 1=Header"},
    {"field_name": "file_name", "type": "A/N", "length": 30, "from": 3, "to": 32, "comments": "File Name (UMR_ACCUM_YYYYMMDD)"},
    {"field_name": "process_date", "type": "A/N", "length": 8, "from": 33, "to": 40, "comments": "Date file was created. Format: CCYYMMDD"},
    {"field_name": "process_time", "type": "A/N", "length": 6, "from": 41, "to": 46, "comments": "Time file was created. Format: HHMMSS"},
    {"field_name": "filler", "type": "A/N", "length": 454, "from": 47, "to": 500, "comments": "Filler - Spaces"},
]

UMR_TRAILER_LAYOUT = [
    {"field_name": "record_type", "type": "A/N", "length": 2, "from": 1, "to": 2, "comments": "Record Type: 3=Trailer"},
    {"field_name": "file_name", "type": "A/N", "length": 30, "from": 3, "to": 32, "comments": "File Name"},
    {"field_name": "process_date", "type": "A/N", "length": 8, "from": 33, "to": 40, "comments": "Date file was created. Format: CCYYMMDD"},
    {"field_name": "process_time", "type": "A/N", "length": 6, "from": 41, "to": 46, "comments": "Time file was created. Format: HHMMSS"},
    {"field_name": "control_record_name", "type": "A/N", "length": 20, "from": 47, "to": 66, "comments": "Field name used in calculating Control Record Amount"},
    {"field_name": "control_record_count", "type": "N", "length": 8, "from": 67, "to": 74, "comments": "Number of data records in the file"},
    {"field_name": "control_record_amount", "type": "N", "length": 15, "from": 75, "to": 89, "comments": "Sum of data records. Format: S9(13)V99"},
    {"field_name": "filler", "type": "A/N", "length": 411, "from": 90, "to": 500, "comments": "Filler - Spaces"},
]

# client_manager/utils.py
CLIENT_ACCOUNT_CODE_RULES = {
    "ALLIED": {"account_prefix": "SAPP", "eligibility_filename_pattern": "Sapp_MEM_TRX"},
    "ASR": {"account_prefix": "6000", "eligibility_filename_pattern": "TRXALBION_PPX_ELIG"},
    "UMR": {"account_prefix": "EMP,SIMP,Cornell College", "eligibility_filename_pattern": "EMP_MEM_TRX_UMR"},
}

# Allied Eligibility Layout (updated to include other insurance fields)
ALLIED_ELIGIBILITY_LAYOUT = [
    {"field_name": "record_type", "type": "A/N", "required": True, "valid_values": ["D"], "comments": "Record Type: D=Detail"},
    {"field_name": "cardholder_id", "type": "A/N", "required": True, "comments": "Unique Cardholder ID"},
    {"field_name": "transaction_code", "type": "A/N", "required": True, "comments": "Transaction Code"},
    # {"field_name": "account_id", "type": "A/N", "required": True, "comments": "Client Account ID (e.g., SAPP01)"},
    {"field_name": "account_id", "type": "A/N", "required": False, "comments": "Client Account ID (e.g., SAPP01)"},
    {"field_name": "group_id", "type": "A/N", "required": True, "comments": "Group ID"},
    {"field_name": "coverage_id", "type": "A/N", "required": True, "comments": "Coverage ID"},
    {"field_name": "family_id", "type": "A/N", "required": True, "comments": "Family ID"},
    {"field_name": "name", "type": "A/N", "required": True, "comments": "First Name"},
    {"field_name": "middle_name", "type": "A/N", "required": False, "comments": "Middle Name"},
    {"field_name": "lastname1", "type": "A/N", "required": True, "comments": "Last Name 1"},
    {"field_name": "lastname2", "type": "A/N", "required": False, "comments": "Last Name 2"},
    {"field_name": "residential_address1", "type": "A/N", "required": True, "comments": "Residential Address Line 1"},
    {"field_name": "residential_address2", "type": "A/N", "required": False, "comments": "Residential Address Line 2"},
    {"field_name": "residential_city", "type": "A/N", "required": True, "comments": "Residential City"},
    {"field_name": "residential_state", "type": "A/N", "required": True, "comments": "Residential State"},
    {"field_name": "residential_zipcode", "type": "A/N", "required": True, "comments": "Residential Zipcode"},
    {"field_name": "postal_address1", "type": "A/N", "required": True, "comments": "Postal Address Line 1"},
    {"field_name": "postal_address2", "type": "A/N", "required": False, "comments": "Postal Address Line 2"},
    {"field_name": "postal_city", "type": "A/N", "required": True, "comments": "Postal City"},
    {"field_name": "postal_state", "type": "A/N", "required": True, "comments": "Postal State"},
    {"field_name": "postal_zipcode", "type": "A/N", "required": True, "comments": "Postal Zipcode"},
    {"field_name": "home_phone", "type": "A/N", "required": False, "comments": "Home Phone"},
    {"field_name": "work_phone", "type": "A/N", "required": False, "comments": "Work Phone"},
    {"field_name": "work_extension", "type": "A/N", "required": False, "comments": "Work Extension"},
    {"field_name": "hicn", "type": "A/N", "required": False, "comments": "Health Insurance Claim Number"},
    {"field_name": "marital_status", "type": "A/N", "required": False, "comments": "Marital Status"},
    {"field_name": "spouse_name", "type": "A/N", "required": False, "comments": "Spouse Name"},
    {"field_name": "representative_name", "type": "A/N", "required": False, "comments": "Representative Name"},
    {"field_name": "representative_phone", "type": "A/N", "required": False, "comments": "Representative Phone"},
    {"field_name": "rep_relationship", "type": "A/N", "required": False, "comments": "Representative Relationship"},
    {"field_name": "reform_ind", "type": "A/N", "required": False, "comments": "Reform Indicator"},
    {"field_name": "birthdate", "type": "N", "required": True, "format": "YYYYMMDD", "comments": "Birth Date"},
    {"field_name": "gender_code", "type": "A/N", "required": True, "valid_values": ["M", "F"], "comments": "Gender: M=Male, F=Female"},
    # {"field_name": "pregnancy_indicator", "type": "A/N", "required": True, "valid_values": ["0", "1"], "comments": "Pregnancy Indicator"},
    {"field_name": "pregnancy_indicator", "type": "A/N", "required": False, "valid_values": ["0", "1"], "comments": "Pregnancy Indicator"},
    {"field_name": "spanish_preference", "type": "A/N", "required": True, "valid_values": ["0", "1"], "comments": "Spanish Preference"},
    {"field_name": "email", "type": "A/N", "required": False, "comments": "Email Address"},
    {"field_name": "patient_suffix_person_code", "type": "A/N", "required": True, "comments": "Patient Suffix Person Code"},
    {"field_name": "patient_relation_id", "type": "N", "required": True, "comments": "Patient Relation ID"},
    {"field_name": "patient_related_to", "type": "A/N", "required": False, "comments": "Patient Related To"},
    {"field_name": "effective_date", "type": "N", "required": True, "format": "YYYYMMDD", "comments": "Effective Date"},
    {"field_name": "termination_date", "type": "N", "required": True, "format": "YYYYMMDD", "comments": "Termination Date"},
    {"field_name": "expiration_date", "type": "N", "required": True, "format": "YYYYMMDD", "comments": "Expiration Date"},
    {"field_name": "current_deductible_balance", "type": "N", "required": False, "comments": "Current Deductible Balance"},
    {"field_name": "ytd_ingredient_cost", "type": "N", "required": False, "comments": "Year-to-Date Ingredient Cost"},
    {"field_name": "current_troop_balance", "type": "N", "required": False, "comments": "Current TrOOP Balance"},
    {"field_name": "other_insurance1_insured_name", "type": "A/N", "required": False, "comments": "Other Insurance 1 Insured Name"},
    {"field_name": "other_insurance1_insured_address1", "type": "A/N", "required": False, "comments": "Other Insurance 1 Address Line 1"},
    {"field_name": "other_insurance1_insured_address2", "type": "A/N", "required": False, "comments": "Other Insurance 1 Address Line 2"},
    {"field_name": "other_insurance1_insured_city", "type": "A/N", "required": False, "comments": "Other Insurance 1 City"},
    {"field_name": "other_insurance1_insured_state", "type": "A/N", "required": False, "comments": "Other Insurance 1 State"},
    {"field_name": "other_insurance1_insured_zipcode", "type": "A/N", "required": False, "comments": "Other Insurance 1 Zipcode"},
    {"field_name": "other_insurance1_insured_phone", "type": "A/N", "required": False, "comments": "Other Insurance 1 Phone"},
    {"field_name": "other_insurance1_insurer", "type": "A/N", "required": False, "comments": "Other Insurance 1 Insurer"},
    {"field_name": "other_insurance1_insured_policy_no", "type": "A/N", "required": False, "comments": "Other Insurance 1 Policy Number"},
    {"field_name": "other_insurance1_insured_group_no", "type": "A/N", "required": False, "comments": "Other Insurance 1 Group Number"},
    {"field_name": "other_insurance2_insured_name", "type": "A/N", "required": False, "comments": "Other Insurance 2 Insured Name"},
    {"field_name": "other_insurance2_insured_address1", "type": "A/N", "required": False, "comments": "Other Insurance 2 Address Line 1"},
    {"field_name": "other_insurance2_insured_address2", "type": "A/N", "required": False, "comments": "Other Insurance 2 Address Line 2"},
    {"field_name": "other_insurance2_insured_city", "type": "A/N", "required": False, "comments": "Other Insurance 2 City"},
    {"field_name": "other_insurance2_insured_state", "type": "A/N", "required": False, "comments": "Other Insurance 2 State"},
    {"field_name": "other_insurance2_insured_zipcode", "type": "A/N", "required": False, "comments": "Other Insurance 2 Zipcode"},
    {"field_name": "other_insurance2_insured_phone", "type": "A/N", "required": False, "comments": "Other Insurance 2 Phone"},
    {"field_name": "other_insurance2_insurer", "type": "A/N", "required": False, "comments": "Other Insurance 2 Insurer"},
    {"field_name": "other_insurance2_insured_policy_no", "type": "A/N", "required": False, "comments": "Other Insurance 2 Policy Number"},
    {"field_name": "other_insurance2_insured_group_no", "type": "A/N", "required": False, "comments": "Other Insurance 2 Group Number"},
    {"field_name": "esrd", "type": "A/N", "required": False, "comments": "ESRD Indicator"},
    {"field_name": "participant_type", "type": "A/N", "required": True, "valid_values": ["I", "F"], "comments": "Participant Type"},
    {"field_name": "ytd_moop_amt", "type": "N", "required": False, "comments": "Year-to-Date MOOP Amount"},
    {"field_name": "load_status", "type": "A/N", "required": True, "valid_values": ["A","Y","I","F"], "comments": "Load Status"},
    {"field_name": "load_reject_code", "type": "A/N", "required": False, "comments": "Load Reject Code"},
    {"field_name": "member_status", "type": "A/N", "required": True, "valid_values": ["A","T","E"], "comments": "Member Status"}
]

# UMR Eligibility Layout (same as Allied)
UMR_ELIGIBILITY_LAYOUT = ALLIED_ELIGIBILITY_LAYOUT

# ASR Eligibility Layout (unchanged)
ASR_ELIGIBILITY_LAYOUT = [
    {"field_name": "Cardholder Id", "type": "A/N", "required": True, "comments": "Unique Cardholder ID"},
    {"field_name": "rx group", "type": "A/N", "required": True, "comments": "RX Group (e.g., 6000)"},
    {"field_name": "customer group", "type": "A/N", "required": True, "comments": "Customer Group"},
    {"field_name": "family id", "type": "A/N", "required": True, "comments": "Family ID"},
    {"field_name": "firsle", "type": "A/N", "required": False, "comments": "Middle Name"},
    {"field_name": "lastt name", "type": "A/N", "required": True, "comments": "First Name"},
    {"field_name": "Midd name1", "type": "A/N", "required": True, "comments": "Last Name 1"},
    {"field_name": "last name2", "type": "A/N", "required": False, "comments": "Last Name 2"},
    {"field_name": "address1", "type": "A/N", "required": True, "comments": "Address Line 1"},
    {"field_name": "address2", "type": "A/N", "required": False, "comments": "Address Line 2"},
    {"field_name": "City", "type": "A/N", "required": True, "comments": "City"},
    {"field_name": "State", "type": "A/N", "required": True, "comments": "State"},
    {"field_name": "Zip", "type": "A/N", "required": True, "comments": "Zipcode"},
    {"field_name": "postal address1", "type": "A/N", "required": True, "comments": "Postal Address Line 1"},
    {"field_name": "postal address2", "type": "A/N", "required": False, "comments": "Postal Address Line 2"},
    {"field_name": "postal city", "type": "A/N", "required": True, "comments": "Postal City"},
    {"field_name": "postal state", "type": "A/N", "required": True, "comments": "Postal State"},
    {"field_name": "postal zip", "type": "A/N", "required": True, "comments": "Postal Zipcode"},
    {"field_name": "home phone", "type": "A/N", "required": False, "comments": "Home Phone"},
    {"field_name": "work phone", "type": "A/N", "required": False, "comments": "Work Phone"},
    {"field_name": "subscriber ssn", "type": "A/N", "required": False, "comments": "Subscriber SSN"},
    {"field_name": "marital status", "type": "A/N", "required": False, "comments": "Marital Status"},
    {"field_name": "date of birth", "type": "A/N", "required": True, "format": "MM-DD-YYYY", "comments": "Date of Birth"},
    {"field_name": "Gender", "type": "A/N", "required": True, "valid_values": ["M", "F"], "comments": "Gender: M=Male, F=Female"},
    {"field_name": "email", "type": "A/N", "required": False, "comments": "Email Address"},
    {"field_name": "person code", "type": "A/N", "required": True, "comments": "Person Code"},
    {"field_name": "patient relationship code", "type": "N", "required": True, "comments": "Patient Relationship Code"},
    {"field_name": "patient related to", "type": "A/N", "required": False, "comments": "Patient Related To"},
    {"field_name": "effective date", "type": "A/N", "required": True, "format": "MM-DD-YYYY", "comments": "Effective Date"},
    {"field_name": "termination date", "type": "A/N", "required": True, "format": "MM-DD-YYYY", "comments": "Termination Date"},
    {"field_name": "expiration date", "type": "A/N", "required": True, "format": "MM-DD-YYYY", "comments": "Expiration Date"},
    {"field_name": "participant type", "type": "A/N", "required": True, "valid_values": ["I", "F"], "comments": "Participant Type"},
    {"field_name": "member status", "type": "A/N", "required": True, "valid_values": ["A"], "comments": "Member Status"}
]

ALLIED_TRX_PPX_MOOP_HEADER_LAYOUT = [
    {"from": 1, "to": 2, "field_name": "record_type", "length": 2, "type": "A"},
    {"from": 3, "to": 12, "field_name": "client_id", "length": 10, "type": "A"},
    {"from": 13, "to": 22, "field_name": "group_id", "length": 10, "type": "A"},
    {"from": 23, "to": 30, "field_name": "process_date", "length": 8, "type": "N"},
    {"from": 31, "to": 500, "field_name": "filler", "length": 470, "type": "A"}
]

ALLIED_TRX_PPX_MOOP_DETAIL_LAYOUT = [
    {"from": 1, "to": 2, "field_name": "record_type", "length": 2, "type": "A"},
    {"from": 3, "to": 12, "field_name": "member_id", "length": 10, "type": "A"},
    {"from": 13, "to": 22, "field_name": "group_id", "length": 10, "type": "A"},
    {"from": 23, "to": 30, "field_name": "date_of_service", "length": 8, "type": "N"},
    {"from": 31, "to": 40, "field_name": "moop_amount", "length": 10, "type": "S9(7)V99"},
    {"from": 41, "to": 50, "field_name": "deductible_amount", "length": 10, "type": "S9(7)V99"},
    {"from": 51, "to": 51, "field_name": "network", "length": 1, "type": "A"},
    {"from": 52, "to": 500, "field_name": "filler", "length": 449, "type": "A"}
]

ALLIED_TRX_PPX_MOOP_TRAILER_LAYOUT = [
    {"from": 1, "to": 2, "field_name": "record_type", "length": 2, "type": "A"},
    {"from": 3, "to": 10, "field_name": "record_count", "length": 8, "type": "N"},
    {"from": 11, "to": 500, "field_name": "filler", "length": 490, "type": "A"}
]

ASR_TRXALBION_HEADER_LAYOUT = [
    {"from": 1, "to": 2, "field_name": "record_type", "length": 2, "type": "A"},
    {"from": 3, "to": 12, "field_name": "client_id", "length": 10, "type": "A"},
    {"from": 13, "to": 22, "field_name": "plan_id", "length": 10, "type": "A"},
    {"from": 23, "to": 30, "field_name": "process_date", "length": 8, "type": "N"},
    {"from": 31, "to": 500, "field_name": "filler", "length": 470, "type": "A"}
]

ASR_TRXALBION_DETAIL_LAYOUT = [
    {"from": 1, "to": 2, "field_name": "record_type", "length": 2, "type": "A"},
    {"from": 3, "to": 12, "field_name": "member_id", "length": 10, "type": "A"},
    {"from": 13, "to": 22, "field_name": "plan_id", "length": 10, "type": "A"},
    {"from": 23, "to": 30, "field_name": "date_of_service", "length": 8, "type": "N"},
    {"from": 31, "to": 40, "field_name": "accum_amount", "length": 10, "type": "S9(7)V99"},
    {"from": 41, "to": 41, "field_name": "network", "length": 1, "type": "A"},
    {"from": 42, "to": 500, "field_name": "filler", "length": 459, "type": "A"}
]

ASR_TRXALBION_TRAILER_LAYOUT = [
    {"from": 1, "to": 2, "field_name": "record_type", "length": 2, "type": "A"},
    {"from": 3, "to": 10, "field_name": "record_count", "length": 8, "type": "N"},
    {"from": 11, "to": 500, "field_name": "filler", "length": 490, "type": "A"}
]



# client_manager/utils.py (continued)
import logging
import re
import os
import csv

logger = logging.getLogger(__name__)

def pad_or_truncate(value, length, pad_char=' '):
    """
    Pad or truncate a string to the specified length.
    Args:
        value (str): The input string.
        length (int): The desired length.
        pad_char (str): Character to use for padding (default: space).
    Returns:
        str: The string padded or truncated to the specified length.
    """
    if len(value) > length:
        return value[:length]
    return value.ljust(length, pad_char)

def replace_special_chars(value):
    """
    Replace special characters (-, _, __, +) with '0' in the given string.
    Args:
        value (str): The input string to process.
    Returns:
        str: The processed string with special characters replaced by '0'.
    """
    if not value:
        return value
    # Replace -, _, +, and ensure __ is handled (though __ is just two _)
    for char in ['-', '_', '+']:
        value = value.replace(char, '0')
    return value

# Additional helper function to extract date from filename
def extract_date_from_pblxv_filename(filename):
    """
    Extract date from PBLXV426_P_ filename.
    Expected format: PBLXV426_P_TransparentRx_YYYYMMDD.txt
    
    Args:
        filename (str): The filename to extract date from
    Returns:
        str or None: The extracted date in YYYYMMDD format, or None if not found
    """
    import re
    
    # Pattern to match PBLXV426_P_*_YYYYMMDD.txt
    pattern = r'PBLXV426_P_.*_(\d{8})\.txt$'
    match = re.search(pattern, filename)
    
    if match:
        return match.group(1)
    
    return None

def validate_PBLXV_file(file_content, client_name, selected_date=None):
    """
    Validate a PBLXV426_P_ file content against the UMR accumulator layout.
    This function validates:
    1. First and last lines contain UMR_ACCUM_YYYYMMDD format
    2. All lines have consistent length matching the UMR accumulator layout
    3. Record type validation for each line
    
    Args:
        file_content (bytes): The content of the file.
        client_name (str): The name of the client.
        selected_date (str, optional): The selected date in YYYYMMDD format. If None, uses today's date.
    Returns:
        dict: {"is_valid": bool, "errors": list of error messages}
    """
    import re
    from datetime import datetime
    
    errors = []
    
    try:
        # Decode the file content
        content_str = file_content.decode('utf-8', errors='replace')
        lines = content_str.splitlines()
        
        if not lines:
            return {"is_valid": False, "errors": ["File is empty."]}
        
        # Determine expected date - use selected_date or today's date
        if selected_date:
            expected_date = selected_date
        else:
            expected_date = datetime.now().strftime('%Y%m%d')
        
        expected_filename_pattern = f"UMR_ACCUM_{expected_date}"
        
        # Validate first line (Header - Record Type 1)
        first_line = lines[0]
        if len(first_line) < 32:
            errors.append("Line 1 (Header): Line is too short to contain filename.")
        else:
            # Extract filename from header (positions 3-32 based on UMR_HEADER_LAYOUT)
            filename_in_header = first_line[2:32].strip()
            if not filename_in_header.startswith("UMR_ACCUM_"):
                errors.append(f"Line 1 (Header): Filename '{filename_in_header}' does not start with 'UMR_ACCUM_'.")
            elif filename_in_header != expected_filename_pattern:
                errors.append(f"Line 1 (Header): Filename '{filename_in_header}' does not match expected pattern '{expected_filename_pattern}'.")
        
        # Validate last line (Trailer - Record Type 3)
        if len(lines) > 1:
            last_line = lines[-1]
            if len(last_line) < 32:
                errors.append(f"Line {len(lines)} (Trailer): Line is too short to contain filename.")
            else:
                # Extract filename from trailer (positions 3-32 based on UMR_TRAILER_LAYOUT)
                filename_in_trailer = last_line[2:32].strip()
                if not filename_in_trailer.startswith("UMR_ACCUM_"):
                    errors.append(f"Line {len(lines)} (Trailer): Filename '{filename_in_trailer}' does not start with 'UMR_ACCUM_'.")
                elif filename_in_trailer != expected_filename_pattern:
                    errors.append(f"Line {len(lines)} (Trailer): Filename '{filename_in_trailer}' does not match expected pattern '{expected_filename_pattern}'.")
        
        # Validate each line for length and basic structure
        for line_num, line in enumerate(lines, start=1):
            if len(line) < 2:
                errors.append(f"Line {line_num}: Line is too short to determine record type.")
                continue
            
            # Get record type (first 2 characters)
            record_type = line[0:2].strip()
            
            # Determine expected length based on record type
            if record_type == "1":  # Header
                expected_length = 500
                layout = UMR_HEADER_LAYOUT
            elif record_type == "2":  # Detail
                expected_length = 500
                layout = UMR_ACCUMULATOR_LAYOUT
            elif record_type == "3":  # Trailer
                expected_length = 500
                layout = UMR_TRAILER_LAYOUT
            else:
                errors.append(f"Line {line_num}: Invalid record type '{record_type}'. Expected 1 (Header), 2 (Detail), or 3 (Trailer).")
                continue
            
            # Check line length
            actual_length = len(line)
            if actual_length != expected_length:
                errors.append(f"Line {line_num}: Line length is {actual_length}, expected {expected_length} for record type {record_type}.")
                continue
            
            # Additional validation for header and trailer lines
            if record_type == "1":  # Header validation
                # Validate process date format (positions 33-40)
                if len(line) >= 40:
                    process_date = line[32:40].strip()
                    if process_date and not re.match(r'^\d{8}$', process_date):
                        errors.append(f"Line {line_num} (Header): Invalid process date format '{process_date}'. Expected CCYYMMDD.")
                
                # Validate process time format (positions 41-46)
                if len(line) >= 46:
                    process_time = line[40:46].strip()
                    if process_time and not re.match(r'^\d{6}$', process_time):
                        errors.append(f"Line {line_num} (Header): Invalid process time format '{process_time}'. Expected HHMMSS.")
            
            elif record_type == "3":  # Trailer validation
                # Validate process date format (positions 33-40)
                if len(line) >= 40:
                    process_date = line[32:40].strip()
                    if process_date and not re.match(r'^\d{8}$', process_date):
                        errors.append(f"Line {line_num} (Trailer): Invalid process date format '{process_date}'. Expected CCYYMMDD.")
                
                # Validate process time format (positions 41-46)
                if len(line) >= 46:
                    process_time = line[40:46].strip()
                    if process_time and not re.match(r'^\d{6}$', process_time):
                        errors.append(f"Line {line_num} (Trailer): Invalid process time format '{process_time}'. Expected HHMMSS.")
                
                # Validate control record count (positions 67-74)
                if len(line) >= 74:
                    control_count = line[66:74].strip()
                    if control_count and not control_count.isdigit():
                        errors.append(f"Line {line_num} (Trailer): Invalid control record count '{control_count}'. Expected numeric value.")
                
                # Validate control record amount (positions 75-89)
                if len(line) >= 89:
                    control_amount = line[74:89].strip()
                    if control_amount and not re.match(r'^-?\d*\.?\d*$', control_amount.replace('{', '').replace('}', '')):
                        errors.append(f"Line {line_num} (Trailer): Invalid control record amount format '{control_amount}'.")
            
            elif record_type == "2":  # Detail record validation
                # Validate member_id (positions 3-17)
                if len(line) >= 17:
                    member_id = line[2:17].strip()
                    if not member_id:
                        errors.append(f"Line {line_num} (Detail): Member ID is empty (positions 3-17).")
                
                # Validate birth_date format (positions 81-88)
                if len(line) >= 88:
                    birth_date = line[80:88].strip()
                    if birth_date and not re.match(r'^\d{8}$', birth_date):
                        errors.append(f"Line {line_num} (Detail): Invalid birth date format '{birth_date}'. Expected CCYYMMDD (positions 81-88).")
                
                # Validate gender (position 104)
                if len(line) >= 104:
                    gender = line[103:104].strip()
                    if gender and gender not in ['M', 'F', 'U']:
                        errors.append(f"Line {line_num} (Detail): Invalid gender '{gender}'. Expected M, F, or U (position 104).")
                
                # Validate relationship (positions 105-106)
                if len(line) >= 106:
                    relationship = line[104:106].strip()
                    if relationship and relationship not in ['EE', 'SP', 'CH', 'OT']:
                        errors.append(f"Line {line_num} (Detail): Invalid relationship '{relationship}'. Expected EE, SP, CH, or OT (positions 105-106).")
                
                # Validate date_of_service format (positions 157-164)
                if len(line) >= 164:
                    service_date = line[156:164].strip()
                    if service_date and not re.match(r'^\d{8}$', service_date):
                        errors.append(f"Line {line_num} (Detail): Invalid service date format '{service_date}'. Expected CCYYMMDD (positions 157-164).")
        
        # Additional file structure validation
        if len(lines) < 2:
            errors.append("File must contain at least a header and trailer record.")
        else:
            # Check if first line is header (record type 1)
            if not lines[0].startswith("1"):
                errors.append("First line must be a header record (record type 1).")
            
            # Check if last line is trailer (record type 3)
            if not lines[-1].startswith("3"):
                errors.append("Last line must be a trailer record (record type 3).")
            
            # Count detail records and validate against trailer
            detail_count = sum(1 for line in lines if line.startswith("2"))
            if len(lines) >= 3:  # Has header, at least one detail, and trailer
                last_line = lines[-1]
                if len(last_line) >= 74:
                    trailer_count = last_line[66:74].strip()
                    if trailer_count.isdigit() and int(trailer_count) != detail_count:
                        errors.append(f"Trailer record count ({trailer_count}) does not match actual detail record count ({detail_count}).")
        
        return {"is_valid": len(errors) == 0, "errors": errors}
        
    except Exception as e:
        logger.error(f"Error validating PBLXV file for client {client_name}: {str(e)}", exc_info=True)
        return {"is_valid": False, "errors": [f"Error validating PBLXV file: {str(e)}"]}

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
        # if not lines:
        #     return {"is_valid": False, "errors": ["File is empty."]}

        # Validate each line
        for line_num, line in enumerate(lines, start=1):
            # if len(line) < 1251:  # Total length as per layout
            #     errors.append(f"Line {line_num}: Line length is {len(line)}, expected 1251.")
            #     continue

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
                account_field = account_field.strip()  # Remove leading/trailing spaces
                expected_prefix = CLIENT_ACCOUNT_CODE_RULES[client_name]["account_prefix"]
                if client_name == "UMR":
                    if account_field not in expected_prefix.split(','):
                        errors.append(
                           f"Line {line_num}: Account code '{account_field}' does not start with expected prefix '{expected_prefix}' (positions 82-111)."
                        )    
                elif not account_field.startswith(expected_prefix):
                    errors.append(
                        f"Line {line_num}: Account code '{account_field}' does not start with expected prefix '{expected_prefix}' (positions 82-111)."
                    )
                else:
                    pass

        return {"is_valid": len(errors) == 0, "errors": errors}
    except Exception as e:
        logger.error(f"Error validating file for client {client_name}: {str(e)}", exc_info=True)
        return {"is_valid": False, "errors": [f"Error validating file: {str(e)}"]}

def validate_umr_accumulator_file(file_content, client_name):
    """
    Validate a UMR accumulator .txt file content against the UMR accumulator layout.
    Args:
        file_content (bytes): The content of the file.
        client_name (str): The name of the client.
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

        # Validate each line based on record type
        for line_num, line in enumerate(lines, start=1):
            if len(line) < 2:
                errors.append(f"Line {line_num}: Line is too short to determine record type.")
                continue

            # Get record type
            record_type = line[0:2].strip()
            
            # Select appropriate layout based on record type
            if record_type == "1":
                layout = UMR_HEADER_LAYOUT
                expected_length = 500
            elif record_type == "2":
                layout = UMR_ACCUMULATOR_LAYOUT
                expected_length = 500
            elif record_type == "3":
                layout = UMR_TRAILER_LAYOUT
                expected_length = 500
            else:
                errors.append(f"Line {line_num}: Invalid record type '{record_type}'. Expected 1, 2, or 3.")
                continue

            # Check line length
            if len(line) != expected_length:
                errors.append(f"Line {line_num}: Line length is {len(line)}, expected {expected_length}.")
                continue

            # Validate each field based on the selected layout
            for field in layout:
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

                # Check type validation for non-filler fields
                if field_name != "filler":
                    field_type = field["type"]
                    
                    # For numeric fields, check if content is numeric when not empty/spaces
                    if field_type == "N" and actual_content.strip() and not actual_content.strip().replace('-', '').replace('.', '').isdigit():
                        errors.append(
                            f"Line {line_num}, Field {field_name}: Expected numeric value, got '{actual_content}' (positions {start + 1}-{end})."
                        )
                    
                    # For date fields, validate format if not empty
                    if field_name in ["birth_date", "date_of_service", "benefit_period_begin_date", "benefit_period_end_date", "process_date"] and actual_content.strip():
                        if not re.match(r'^\d{8}$', actual_content.strip()):
                            errors.append(
                                f"Line {line_num}, Field {field_name}: Invalid date format '{actual_content}'. Expected CCYYMMDD (positions {start + 1}-{end})."
                            )
                    
                    # For time fields, validate format if not empty
                    if field_name == "process_time" and actual_content.strip():
                        if not re.match(r'^\d{6}$', actual_content.strip()):
                            errors.append(
                                f"Line {line_num}, Field {field_name}: Invalid time format '{actual_content}'. Expected HHMMSS (positions {start + 1}-{end})."
                            )
                    
                    # Validate specific field values
                    if field_name == "gender" and actual_content.strip() and actual_content.strip() not in ['M', 'F', 'U']:
                        errors.append(
                            f"Line {line_num}, Field {field_name}: Invalid gender value '{actual_content}'. Expected M, F, or U (positions {start + 1}-{end})."
                        )
                    
                    if field_name == "relationship" and actual_content.strip() and actual_content.strip() not in ['EE', 'SP', 'CH', 'OT']:
                        errors.append(
                            f"Line {line_num}, Field {field_name}: Invalid relationship value '{actual_content}'. Expected EE, SP, CH, or OT (positions {start + 1}-{end})."
                        )
                    
                    if field_name == "accum_type" and actual_content.strip() and actual_content.strip() not in ['INFERT', 'SPECIALTY', 'DIABETIC']:
                        errors.append(
                            f"Line {line_num}, Field {field_name}: Invalid accum_type value '{actual_content}'. Expected INFERT, SPECIALTY, or DIABETIC (positions {start + 1}-{end})."
                        )
                    
                    if field_name == "network" and actual_content.strip() and actual_content.strip() not in ['IN', 'OUT', 'TIER1', 'TIER2', 'TIER3']:
                        errors.append(
                            f"Line {line_num}, Field {field_name}: Invalid network value '{actual_content}'. Expected IN, OUT, TIER1, TIER2, or TIER3 (positions {start + 1}-{end})."
                        )
                    
                    # Validate Y/N indicators
                    if field_name in ["deductible_indicator", "out_of_pocket_indicator", "infertility_indicator"] and actual_content.strip() and actual_content.strip() not in ['Y', 'N']:
                        errors.append(
                            f"Line {line_num}, Field {field_name}: Invalid indicator value '{actual_content}'. Expected Y or N (positions {start + 1}-{end})."
                        )

        return {"is_valid": len(errors) == 0, "errors": errors}
    except Exception as e:
        logger.error(f"Error validating UMR accumulator file for client {client_name}: {str(e)}", exc_info=True)
        return {"is_valid": False, "errors": [f"Error validating UMR accumulator file: {str(e)}"]}

# Updated validation function that can auto-detect date from filename
def validate_PBLXV_file_with_auto_date(file_content, client_name, filename=None, selected_date=None):
    """
    Enhanced PBLXV file validation that can auto-detect date from filename.
    
    Args:
        file_content (bytes): The content of the file.
        client_name (str): The name of the client.
        filename (str, optional): The filename to extract date from.
        selected_date (str, optional): The selected date in YYYYMMDD format. Takes precedence over filename date.
    Returns:
        dict: {"is_valid": bool, "errors": list of error messages}
    """
    # Determine the expected date
    expected_date = selected_date
    
    if not expected_date and filename:
        expected_date = extract_date_from_pblxv_filename(filename)
    
    if not expected_date:
        from datetime import datetime
        expected_date = datetime.now().strftime('%Y%m%d')
    
    return validate_PBLXV_file(file_content, client_name, expected_date)

def validate_and_correct_RxEOB_umr_accumulator_file(file_content, client_name, output_file_path=None):
    """
    Validate and correct a UMR accumulator .txt file content against the UMR accumulator layout.
    Replace special characters in member_id with '0'.
    Optionally write the corrected content to an output file.
    Args:
        file_content (bytes): The content of the file.
        client_name (str): The name of the client.
        output_file_path (str, optional): Path to save the corrected file.
    Returns:
        dict: {"is_valid": bool, "errors": list, "corrected_lines": list}
    """
    errors = []
    corrected_lines = []
    
    try:
        # Decode the file content
        content_str = file_content.decode('utf-8', errors='replace')
        lines = content_str.splitlines()
        if not lines:
            return {"is_valid": False, "errors": ["File is empty."], "corrected_lines": []}

        # Validate and correct each line
        for line_num, line in enumerate(lines, start=1):
            if len(line) < 2:
                errors.append(f"Line {line_num}: Line is too short to determine record type.")
                continue

            # Get record type
            record_type = line[0:2].strip()
            if record_type != "2":  # Only process detail records (type 2) based on provided file
                errors.append(f"Line {line_num}: Expected detail record (type 2), got '{record_type}'.")
                corrected_lines.append(line)  # Preserve non-detail records unchanged
                continue

            # Validate line length
            expected_length = 500
            if len(line) != expected_length:
                errors.append(f"Line {line_num}: Line length is {len(line)}, expected {expected_length}.")
                # Attempt to pad or truncate to continue validation
                line = pad_or_truncate(line, expected_length)

            # Parse and validate fields
            corrected_fields = []
            for field in UMR_ACCUMULATOR_LAYOUT:
                field_name = field["field_name"]
                expected_length = field["length"]
                start = field["from"] - 1
                end = field["to"]
                actual_content = line[start:end] if len(line) >= end else line[start:] + ' ' * (end - len(line))
                actual_length = len(actual_content)

                # Check length
                if actual_length != expected_length:
                    errors.append(
                        f"Line {line_num}, Field {field_name}: Length is {actual_length}, expected {expected_length} (positions {start + 1}-{end})."
                    )
                    actual_content = pad_or_truncate(actual_content, expected_length)

                # Type validation
                field_type = field["type"]
                if field_type == "N" and actual_content.strip() and not actual_content.strip().replace('-', '').replace('.', '').isdigit():
                    errors.append(
                        f"Line {line_num}, Field {field_name}: Expected numeric value, got '{actual_content}' (positions {start + 1}-{end})."
                    )

                # Date validation
                if field_name in ["birth_date", "date_of_service", "benefit_period_begin_date", "benefit_period_end_date"] and actual_content.strip():
                    if not re.match(r'^\d{8}$', actual_content.strip()):
                        errors.append(
                            f"Line {line_num}, Field {field_name}: Invalid date format '{actual_content}'. Expected CCYYMMDD (positions {start + 1}-{end})."
                        )

                # Specific field validations
                if field_name == "gender" and actual_content.strip() and actual_content.strip() not in ['M', 'F', 'U']:
                    errors.append(
                        f"Line {line_num}, Field {field_name}: Invalid gender value '{actual_content}'. Expected M, F, or U (positions {start + 1}-{end})."
                    )
                if field_name == "relationship" and actual_content.strip() and actual_content.strip() not in ['EE', 'SP', 'CH', 'OT']:
                    errors.append(
                        f"Line {line_num}, Field {field_name}: Invalid relationship value '{actual_content}'. Expected EE, SP, CH, or OT (positions {start + 1}-{end})."
                    )
                if field_name == "accum_type" and actual_content.strip() and actual_content.strip() not in ['INFERT', 'SPECIALTY', 'DIABETIC']:
                    errors.append(
                        f"Line {line_num}, Field {field_name}: Invalid accum_type value '{actual_content}'. Expected INFERT, SPECIALTY, or DIABETIC (positions {start + 1}-{end})."
                    )
                if field_name == "network" and actual_content.strip() and actual_content.strip() not in ['IN', 'OUT', 'TIER1', 'TIER2', 'TIER3']:
                    errors.append(
                        f"Line {line_num}, Field {field_name}: Invalid network value '{actual_content}'. Expected IN, OUT, TIER1, TIER2, or TIER3 (positions {start + 1}-{end})."
                    )
                if field_name in ["deductible_indicator", "out_of_pocket_indicator", "infertility_indicator"] and actual_content.strip() and actual_content.strip() not in ['Y', 'N']:
                    errors.append(
                        f"Line {line_num}, Field {field_name}: Invalid indicator value '{actual_content}'. Expected Y or N (positions {start + 1}-{end})."
                    )

                # Special character replacement for member_id
                if field_name == "member_id":
                    actual_content = replace_special_chars(actual_content)
                    actual_content = pad_or_truncate(actual_content, expected_length)

                corrected_fields.append(actual_content)

            # Construct corrected line
            corrected_line = ''.join(corrected_fields)
            corrected_lines.append(corrected_line)

        # Write corrected file if output path provided
        if output_file_path:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                for line in corrected_lines:
                    f.write(line + '\n')

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "corrected_lines": corrected_lines
        }

    except Exception as e:
        logger.error(f"Error validating and correcting UMR accumulator file for client {client_name}: {str(e)}", exc_info=True)
        return {
            "is_valid": False,
            "errors": [f"Error validating and correcting UMR accumulator file: {str(e)}"],
            "corrected_lines": []
        }

def validate_file(file_path):
    """
    Validate a file: check if it exists and is not empty.
    Returns a dict with validation result and errors (if any).
    """
    validation_result = {"is_valid": True, "errors": []}

    if not os.path.exists(file_path):
        validation_result["is_valid"] = False
        validation_result["errors"].append(f"File does not exist: {file_path}")
        return validation_result

    if os.path.getsize(file_path) == 0:
        validation_result["is_valid"] = False
        validation_result["errors"].append(f"File is empty: {file_path}")

    return validation_result


def validate_eligibility_file(file_content, client_name):
    """
    Validate an Eligibility file based on the client-specific layout.
    Args:
        file_content (bytes): The content of the Eligibility file.
        client_name (str): The name of the client (e.g., 'Allied', 'ASR', 'UMR').
    Returns:
        dict: {"is_valid": bool, "errors": list of error messages}
    """
    errors = []
    try:
        # Decode file content
        content_str = file_content.decode('utf-8', errors='replace')
        lines = content_str.splitlines()

        if not lines:
            return {"is_valid": False, "errors": ["File is empty."]}

        # Select layout based on client
        if client_name not in CLIENT_ACCOUNT_CODE_RULES:
            return {"is_valid": False, "errors": [f"Unknown client: {client_name}"]}

        if client_name == "ALLIED":
            layout = ALLIED_ELIGIBILITY_LAYOUT
        elif client_name == "ASR":
            layout = ASR_ELIGIBILITY_LAYOUT
        elif client_name == "UMR":
            layout = UMR_ELIGIBILITY_LAYOUT
        else:
            return {"is_valid": False, "errors": [f"No eligibility layout defined for client: {client_name}"]}

        expected_headers = [field["field_name"] for field in layout]
        headers = lines[0].split('\t')

        # Validate headers
        if headers != expected_headers:
            errors.append(f"Invalid headers. Expected: {expected_headers}, Got: {headers}")
            return {"is_valid": False, "errors": errors}

        # Get client-specific rules
        account_prefix = CLIENT_ACCOUNT_CODE_RULES[client_name]["account_prefix"]
        date_format = "MM-DD-YYYY" if client_name == "ASR" else "YYYYMMDD"

        # Parse file as tab-delimited
        reader = csv.reader(lines[1:], delimiter='\t')
        for line_num, row in enumerate(reader, start=2):
            if len(row) != len(expected_headers):
                errors.append(f"Line {line_num}: Incorrect number of fields. Expected {len(expected_headers)}, Got {len(row)}")
                continue

            # Map row to field names
            record = dict(zip(expected_headers, row))
            # logger.info(f"row::{row}, line_num::{line_num}")
            # if record:
            #     logger.info(f"record::{record}, line_num::{line_num}")
            #     break
            # Validate each field based on layout
            for field in layout:
                field_name = field["field_name"]
                value = record[field_name].strip()
                field_type = field["type"]
                required = field.get("required", False)
                valid_values = field.get("valid_values", None)
                format_spec = field.get("format", None)
                # Check required fields
                if required and not value:
                    errors.append(f"Line {line_num}: {field_name} is empty but required.")

                # Validate specific fields
                if field_name in ["account_id", "rx group"] and value:
                    if not value.startswith(account_prefix):
                        errors.append(f"Line {line_num}: {field_name} '{value}' does not start with expected prefix '{account_prefix}'.")

                # Validate date fields
                if format_spec and value:
                    if format_spec == "YYYYMMDD" and not re.match(r'^\d{8}$', value):
                        errors.append(f"Line {line_num}: Invalid {field_name} format '{value}'. Expected YYYYMMDD.")
                    elif format_spec == "MM-DD-YYYY" and not re.match(r'^\d{2}-\d{2}-\d{4}$', value):
                        errors.append(f"Line {line_num}: Invalid {field_name} format '{value}'. Expected MM-DD-YYYY.")

                # Validate valid_values
                if valid_values and value and value not in valid_values:
                    errors.append(f"Line {line_num}: Invalid {field_name} '{value}'. Expected one of {valid_values}.")

                # Validate numeric fields
                if field_type == "N" and value and not re.match(r'^-?\d*\.?\d*$', value):
                    errors.append(f"Line {line_num}: Invalid {field_name} '{value}'. Expected numeric value.")

        return {"is_valid": len(errors) == 0, "errors": errors}

    except Exception as e:
        logger.error(f"Error validating Eligibility file for client {client_name}: {str(e)}", exc_info=True)
        return {"is_valid": False, "errors": [f"Error validating Eligibility file: {str(e)}"]}


def validate_txt_file_10PM_Accumlator(file_content, client_name):
    """
    Validate a 5PM Accumulator file based on client-specific layouts.
    Args:
        file_content (bytes): The content of the file.
        client_name (str): The name of the client (e.g., "ALLIED", "ASR", "UMR").
    Returns:
        dict: {"is_valid": bool, "errors": list of error messages}
    """
    errors = []
    try:
        content_str = file_content.decode('utf-8', errors='replace')
        lines = content_str.splitlines()
        if not lines:
            return {"is_valid": False, "errors": ["File is empty."]}

        # Select layout based on client
        if client_name == "ALLIED":
            header_layout = ALLIED_TRX_PPX_MOOP_HEADER_LAYOUT
            detail_layout = ALLIED_TRX_PPX_MOOP_DETAIL_LAYOUT
            trailer_layout = ALLIED_TRX_PPX_MOOP_TRAILER_LAYOUT
        elif client_name == "ASR":
            header_layout = ASR_TRXALBION_HEADER_LAYOUT
            detail_layout = ASR_TRXALBION_DETAIL_LAYOUT
            trailer_layout = ASR_TRXALBION_TRAILER_LAYOUT
        elif client_name == "UMR":
            header_layout = UMR_HEADER_LAYOUT
            detail_layout = UMR_ACCUMULATOR_LAYOUT
            trailer_layout = UMR_TRAILER_LAYOUT
        else:
            return {"is_valid": False, "errors": [f"No validation layout defined for client {client_name}."]}

        expected_length = 500  # Consistent length for all clients

        for line_num, line in enumerate(lines, start=1):
            if len(line) < 2:
                errors.append(f"Line {line_num}: Line too short to determine record type.")
                continue

            record_type = line[0:2].strip()
            if record_type == "1":
                layout = header_layout
            elif record_type == "2":
                layout = detail_layout
            elif record_type == "3":
                layout = trailer_layout
            else:
                errors.append(f"Line {line_num}: Invalid record type '{record_type}'. Expected 1, 2, or 3.")
                continue

            if len(line) != expected_length:
                errors.append(f"Line {line_num}: Line length is {len(line)}, expected {expected_length}.")
                continue

            for field in layout:
                start = field["from"] - 1
                end = field["to"]
                value = line[start:end].strip()
                field_name = field["field_name"]
                field_type = field["type"]

                if field_name != "filler":
                    if len(value) != field["length"]:
                        errors.append(f"Line {line_num}, Field {field_name}: Length is {len(value)}, expected {field['length']} (positions {start + 1}-{end}).")

                    if field_type == "N" and value and not value.replace('-', '').replace('.', '').isdigit():
                        errors.append(f"Line {line_num}, Field {field_name}: Expected numeric, got '{value}' (positions {start + 1}-{end}).")
                    elif field_type.startswith("S9") and value and not re.match(r'^-?\d*\.?\d*$', value):
                        errors.append(f"Line {line_num}, Field {field_name}: Expected signed numeric, got '{value}' (positions {start + 1}-{end}).")

                    if field_name in ["process_date", "date_of_service"] and value:
                        if not re.match(r'^\d{8}$', value):
                            errors.append(f"Line {line_num}, Field {field_name}: Invalid date format '{value}', expected YYYYMMDD (positions {start + 1}-{end}).")
                    if field_name == "network" and value and value not in ['I', 'O', '1', '2', '3']:  # Simplified for IN/OUT or TIER1-3
                        errors.append(f"Line {line_num}, Field {field_name}: Invalid network '{value}', expected I, O, 1, 2, or 3 (positions {start + 1}-{end}).")

        # Structural validations
        if len(lines) < 2 or not lines[0].startswith("1") or not lines[-1].startswith("3"):
            errors.append("File must start with Header (1) and end with Trailer (3).")
        detail_count = sum(1 for line in lines if line.startswith("2"))
        trailer_record_count_field = trailer_layout[1]["from"] - 1, trailer_layout[1]["to"]  # record_count field
        if len(lines) > 2 and lines[-1][trailer_record_count_field[0]:trailer_record_count_field[1]].strip().isdigit():
            trailer_count = int(lines[-1][trailer_record_count_field[0]:trailer_record_count_field[1]].strip())
            if trailer_count != detail_count:
                errors.append(f"Trailer record count {trailer_count} does not match detail count {detail_count}.")

        return {"is_valid": len(errors) == 0, "errors": errors}
    except Exception as e:
        logger.error(f"Error validating 5PM file for {client_name}: {str(e)}", exc_info=True)
        return {"is_valid": False, "errors": [f"Error validating file: {str(e)}"]}