import requests
import os
import json

# I have no idea how often this changes/resets, but if I had to guess it would be ever time you logged out or otherwise deleted the session
# You need to include the "Bearer" text here
token = "Bearer abc"
user_agent = "totally not a college board data scraper"

subject_id = 8; # ID of the subject of the specific class we are taking (8 is the ID for computer science)
education_per = 24; # Not fully sure what this is yet, I'm still working on understanding what college board means by this

os.system("bash ap.sh")

f = open("api.json", "r")
stuff = f.read() 
# Step one: scan the subject for all assignments:

# Now in stuff we have all of the resources posted by the teacher
# Let's sort that and find the assignments posted

asIDs = [] # blank array for assignments IDs

for thing in json.loads(stuff)["data"]["courseOutline"]["units"]: # sort through each unit and search for tasks
    for unit in thing["subunits"]: # search each subunit
        for sub in unit["resources"]:
            if sub["__typename"] == "AssessmentResource": # searches for assignments posted by the teacher
                asIDs.append(sub["assessmentId"])

print("Downloaded " + str(len(asIDs)) + " from CollegeBoard...")

# all you need to make the request is the GraphQL request in JSON

for thingtodo in asIDs:
    result = requests.post("https://apc-api-production.collegeboard.org/fym/graphql", json={"query":"query assignmentsOverviewStudent($subjectId: Int!, $assessmentIds: [Int]!) {\n  assignmentsOverviewStudent {\n    assignments(subjectId: $subjectId, assessmentIds: $assessmentIds) {\n      id\n      name\n      assessmentId\n      date\n      headline\n      link\n      status\n      scoringCompletedAt\n      showResults\n      timer\n      learnosityActivityId\n      learnositySubmittedAt\n      submittedAt\n      printToggle\n      studentScoring\n      assignmentCreatedAt\n      sessionScore\n      __typename\n    }\n    __typename\n  }\n}\n","variables":{"subjectId":subject_id,"assessmentIds":[thingtodo]},"operationName":"assignmentsOverviewStudent"}, headers={"User-agent": user_agent, "Authorization": token})

    try:
        for task in result.json()["data"]["assignmentsOverviewStudent"]["assignments"]:
            print("You scored a " + str(round(task["sessionScore"] * 100, 1)) + "% on " + task["name"]) # CB sends us the score out of 1, so I multiply it by 100 and round to 1 decimal place via the round() function
    except:
        print("Bad API key/Error on college board servers \n \n HTTP: " + str(result.status_code) + " \n \n JSON: " + str(result.json()))

classes = requests.post("https://apc-api-production.collegeboard.org/fym/graphql", json={"query":"query me {\n  me {\n    id\n    email\n    initId\n    username\n    firstName\n    lastName\n    userRole\n    isStudent\n    ssoLogin\n    pilot\n    generateData\n    registeredDate\n    importId\n    preferences {\n      preference\n      value\n      context\n      contextId\n      __typename\n    }\n    sections {\n      id\n      masterSubjectId\n      name\n      educationPeriod\n      parentId\n      importId\n      teacherId\n      teacherCbPersonId\n      sectionType\n      __typename\n    }\n    schoolSet {\n      initId\n      groupImportId\n      name\n      parentId\n      timezone\n      __typename\n    }\n    programs\n    lastLogin\n    __typename\n  }\n  teacherSubjects {\n    id\n    name\n    subjectProgram\n    classes {\n      id\n      name\n      parentId\n      educationPeriod\n      students {\n        id: initId\n        firstName\n        lastName\n        apuid\n        email\n        __typename\n      }\n      studentsPrior {\n        id: initId\n        firstName\n        lastName\n        apuid\n        email\n        __typename\n      }\n      __typename\n    }\n    educationPeriods {\n      id\n      displayValue\n      contentAvailableAt\n      endDate\n      __typename\n    }\n    subjects {\n      initId\n      name\n      __typename\n    }\n    __typename\n  }\n  studentSubjects {\n    id\n    name\n    subjectProgram\n    initId\n    __typename\n  }\n  adminSubjects {\n    id\n    initId\n    importId\n    masterSubjectId\n    name\n    parentId\n    subjectProgram\n    type\n    url\n    containsSecureQuestions\n    __typename\n  }\n  contentTaggingSubjects {\n    id\n    initId\n    importId\n    masterSubjectId\n    name\n    parentId\n    subjectProgram\n    type\n    url\n    __typename\n  }\n  educationPeriods {\n    id\n    displayValue\n    contentAvailableAt\n    endDate\n    __typename\n  }\n  currentEducationPeriod {\n    id\n    displayValue\n    endDate\n    __typename\n  }\n  nextEducationPeriod {\n    id\n    displayValue\n    __typename\n  }\n}\n","operationName":"me"}, headers={"User-agent": user_agent, "Authorization": token})

try:
    print("=====================================")
    print("You are enrolled in:")
    for _class in classes.json()["data"]["studentSubjects"]:
        print(_class["name"])
except:
    print("Bad API key/Error on college board servers (in classes section) \n \n HTTP: " + str(classes.status_code) + " \n \n JSON: " + str(classes.json()))
