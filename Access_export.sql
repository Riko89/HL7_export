SELECT 
HORIZON.[LAB ID] AS LAB_ID, 
HORIZON.[SPECIMEN ID] AS REQ_ID, 
'---' AS [PHYSICIAN_ACCOUNT_ID], 
'---' AS [PHYSICIAN_OFFICE], 
'---' AS [PHYSICIAN_NPI_NUM],
IIF(HORIZON.[RECEIVE] is NOT NULL, Year(HORIZON.[RECEIVE]) & 
    Right('0' & Month(HORIZON.[RECEIVE]), 2) & 
    Right('0' & Day(HORIZON.[RECEIVE]), 2), '')
	AS DATE_OF_SERVICE,
IIF(RESULTS2.[REPORT_TO] is NOT NULL, Year(RESULTS2.[REPORT_TO]) & 
    Right('0' & Month(RESULTS2.[REPORT_TO]), 2) & 
    Right('0' & Day(RESULTS2.[REPORT_TO]), 2), '')
	AS REPORT_DATE,
REPLACE(UCASE(DONORS.[Last Name]) & ' ' & UCASE(DONORS.[First Name] & ' '), ' ', '^') AS PATIENT_NAME,
DONORS.[SSN] AS PATIENT_SSN,
DONORS.[PT Street Address] & '^^' & DONORS.[PT City] & '^' & DONORS.[PT State] & ' ' & DONORS.[PT Zip code] AS PATIENT_ADDRESS,
DONORS.[Phone]AS PATIENT_PHONE,
IIF(DONORS.[Date of Birth (MM/DD/YYYY)] is NOT NULL AND IsDate(DONORS.[Date of Birth (MM/DD/YYYY)]),
Year(DONORS.[Date of Birth (MM/DD/YYYY)]) & 
    Right('0' & Month(DONORS.[Date of Birth (MM/DD/YYYY)]), 2) & 
    Right('0' & Day(DONORS.[Date of Birth (MM/DD/YYYY)]), 2), '') 
	AS PATIENT_DOB,
IIF(UCASE(DONORS.[Sex]) like 'M*', 'M',
	IIF(UCASE(DONORS.[Sex]) like 'F*', 'F', 'U')) 
	AS PATIENT_SEX,
'---' AS [DX_CODE],
DONORS.[Insurance Name] AS INS1_NAME,
DONORS.[Policy Number] AS INS1_POLICY_NUM,
DONORS.[Group Number] AS INS1_GRP_NUM,
Left(DONORS.[Subscriber name (First Last)], InStr(DONORS.[Subscriber name (First Last)],' ')-1) AS INS1_FIRST_NAME_ON_INSURANCE,
Mid(DONORS.[Subscriber name (First Last)],InStr(DONORS.[Subscriber name (First Last)],' ')+1) AS INS1_LAST_NAME_ON_INSURANCE,
DONORS.[Relationship to Patient] AS INS1_RELATIONSHIP_TO_INSURER,
DONORS.[Insurance Street Address] & '^^' & DONORS.[City] & '^' & DONORS.[State] & ' ' & DONORS.[PT Zip code] AS INS1_ADDRESS,
DONORS.[Insurance Phone Number] AS INS1_PHONE,
'Covid-19' AS TYPE_OF_TEST,
'' AS DRUG_CLASS,
'' AS DRUG_SUBCLASS,
'' AS DRUG_TEST,
RESULTS2.[C19] AS RESULTS,
'' AS POSITION
FROM ((BILLING RIGHT JOIN DONORS ON BILLING.[CLIENT NAME] = DONORS.[Client Name]) LEFT JOIN HORIZON ON DONORS.[Specimen ID] = HORIZON.[SPECIMEN ID]) LEFT JOIN RESULTS2 ON HORIZON.[LAB ID] = RESULTS2.LABID
WHERE HORIZON.[RECEIVE] > DateSerial(Year(Now()), Month(Now()), Day(Now()) - 90)
AND DONORS.[Subscriber name (First Last)] LIKE '* *'