import kagglehub

# Download latest version
path = kagglehub.dataset_download("tunguz/200000-jeopardy-questions")

print("Path to dataset files:", path)
