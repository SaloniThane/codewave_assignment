# codewave_assignment
# Clone the repository
git clone https://github.com/SaloniThane/codewave_assignment.git

# Change into the project directory
cd codewave_assignment

# Install dependencies
pip install -r requirements.txt

# Build the Docker image
docker build -t codewaveassignment.

# Run the Docker container
docker run -p 5000:5000 -d codewaveassignment 
