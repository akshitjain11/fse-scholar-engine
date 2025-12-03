import flordb as flor

from extraction.scai import professor_names as scai_professors

# TODO: Add more departments
departments = {
    "SCAI": scai_professors,
}

for dept in flor.loop("department", departments):
    names = departments[dept]

    for i, name in flor.loop("faculty", enumerate(sorted(names))):
        flor.log("name", name)
