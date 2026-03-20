from goskill import GoSkill

skill = GoSkill(
    goal="Ship a refactor safely",
    criteria={
        "compile": "0 errors",
        "coverage": ">= 90%",
        "report": "complete",
    },
    max_hours=1,
)

result = skill.run(lambda: {
    "compile": "0 errors",
    "coverage": 95,
    "report": "complete",
})

print("Result:", result)
print("Status:", skill.status)
