import flordb as flor

from extraction.scai import professor_names as scai_professors

# TODO: Add more departments
departments = {
    "SCAI": sorted(scai_professors),
}

for dept in flor.loop("department", departments):
    names = departments[dept]

    for i in flor.loop("faculty", range(len(names))):
        flor.log("name", names[i])
