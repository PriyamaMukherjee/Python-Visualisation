import pandas as pd
import sqlite3
conn = sqlite3.connect('FinalDB.db')
url1='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoCensusData.csv?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01'
url2='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoPublicSchools.csv?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01'
url3=('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoCrimeData.csv?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01')
df1 = pd.read_csv(url1)
df2 = pd.read_csv(url2)
df3 = pd.read_csv(url3)
df1.to_sql('Census_Data', conn, if_exists='replace', index=False)
df2.to_sql('Public_Schools', conn, if_exists='replace', index=False)
df3.to_sql('Crime_Data', conn, if_exists='replace', index=False)
cursor = conn.cursor()
#total number of crimes recorded in the CRIME table.
query = "SELECT COUNT(*) FROM Crime_Data"
cursor.execute(query)
print("Total number of crimes recorded:", cursor.fetchone()[0])
# community area names and numbers with per capita income less than 11000.
query = """
SELECT COMMUNITY_AREA_NUMBER, COMMUNITY_AREA_NAME, PER_CAPITA_INCOME
FROM Census_Data
WHERE PER_CAPITA_INCOME < 11000;
"""
cursor.execute(query)
results = cursor.fetchall()
print("Community areas with per capita income less than 11000:")
for row in results:
    print(f"Area Number: {row[0]}, Name: {row[1]}, Income: {row[2]}")
#all case numbers for crimes involving minors(children are not considered minors for the purposes of crime analysis)
query = """
SELECT CASE_NUMBER
FROM Crime_Data
WHERE DESCRIPTION LIKE '%MINOR%';
"""
cursor.execute(query)
results = cursor.fetchall()
print("Case numbers involving minors:")
for row in results:
    print(row[0])
#all kidnapping crimes involving a child
query = """
SELECT *
FROM Crime_Data
WHERE PRIMARY_TYPE = 'KIDNAPPING'
AND DESCRIPTION LIKE '%CHILD%';
"""
cursor.execute(query)
results = cursor.fetchall()
print("Kidnapping crimes involving a child:")
for row in results:
    print(row)
# the kind of crimes that were recorded at schools.
query = """
SELECT DISTINCT PRIMARY_TYPE
FROM Crime_Data
WHERE LOCATION_DESCRIPTION LIKE '%SCHOOL%';
"""
cursor.execute(query)
results = cursor.fetchall()
print("Types of crimes recorded at schools:")
for row in results:
    print(row[0])
#the type of schools along with the average safety score for each type
query = """
SELECT "Elementary, Middle, or High School" AS School_Type,
       AVG(SAFETY_SCORE) AS Average_Safety_Score
FROM Public_Schools
GROUP BY "Elementary, Middle, or High School";
"""
cursor.execute(query)
results = cursor.fetchall()
print("Average Safety Score by School Type:")
for row in results:
    print(f"{row[0]}: {round(row[1], 2)}")
# 5 community areas with highest % of households below poverty line
query = """
SELECT COMMUNITY_AREA_NAME, PERCENT_HOUSEHOLDS_BELOW_POVERTY
FROM Census_Data
ORDER BY PERCENT_HOUSEHOLDS_BELOW_POVERTY DESC
LIMIT 5;
"""
df_result = pd.read_sql_query(query, conn)
df_result
#community area is most crime prone? Display the coumminty area number only.
query = """
SELECT COMMUNITY_AREA_NUMBER
FROM Crime_Data
GROUP BY COMMUNITY_AREA_NUMBER
ORDER BY COUNT(*) DESC
LIMIT 1;
"""
cursor.execute(query)
area_number = cursor.fetchone()[0]
print("Most crime-prone community area number:", area_number)
# a sub-query to find the name of the community area with highest hardship index
query = """
SELECT COMMUNITY_AREA_NAME
FROM Census_Data
WHERE HARDSHIP_INDEX = (
    SELECT MAX(HARDSHIP_INDEX)
    FROM Census_Data
);
"""
cursor.execute(query)
result = cursor.fetchone()[0]
print("Community area with highest hardship index:", result)
# a sub-query to determine the Community Area Name with most number of crimes
query = """
SELECT COMMUNITY_AREA_NAME
FROM Census_Data
WHERE COMMUNITY_AREA_NUMBER = (
    SELECT COMMUNITY_AREA_NUMBER
    FROM Crime_Data
    GROUP BY COMMUNITY_AREA_NUMBER
    ORDER BY COUNT(*) DESC
    LIMIT 1
);
"""
cursor.execute(query)
result = cursor.fetchone()[0]
print("Community area with most number of crimes:", result)






