pip freeze > requirements.txt
docker buildx build --platform linux/amd64 -t uhaku/black-jack-21:latest . --push