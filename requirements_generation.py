import subprocess

def generate_requirements():
    # Run 'pip freeze' and capture the output
    result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)

    # Get the list of installed packages (i.e., the output of 'pip freeze')
    requirements = result.stdout

    # Write the output to a 'requirements.txt' file
    with open('requirements.txt', 'w') as file:
        file.write(requirements)

    print("requirements.txt has been generated!")

# Call the function to generate the requirements file
generate_requirements()
