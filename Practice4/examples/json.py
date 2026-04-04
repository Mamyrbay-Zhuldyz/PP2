#Example 1
import json

json_string = '{"name": "Alice", "age": 25, "city": "New York"}'
python_dict = json.loads(json_string)
print(python_dict['name'])

#Example 2
import json

data = {
    "name": "Bob",
    "age": 30,
    "hobbies": ["reading", "swimming"],
    "married": False
}

json_string = json.dumps(data)
print(json_string)

#Example 3
import json

data = {
    "students": [
        {"name": "Alice", "grade": 85},
        {"name": "Bob", "grade": 92},
        {"name": "Charlie", "grade": 78}
    ]
}

with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)

#Example 4
import json

with open('sample-data.json', 'r') as file:
    data = json.load(file)
    print(data)

#Example 5
import json

sample_data = '''
{
    "company": "Tech Corp",
    "employees": [
        {"id": 1, "name": "John", "department": "IT"},
        {"id": 2, "name": "Jane", "department": "HR"}
    ],
    "location": "New York"
}
'''

data = json.loads(sample_data)
print(f"Company: {data['company']}")
print(f"Number of employees: {len(data['employees'])}")

for emp in data['employees']:
    print(f"Employee {emp['id']}: {emp['name']} - {emp['department']}")