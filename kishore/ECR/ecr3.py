import boto3

# Initialize Boto3 ECR client
ecr_client = boto3.client('ecr')

def get_ecr_repositories():
    response = ecr_client.describe_repositories()
    return response['repositories']

def get_repository_images(repository_name):
    response = ecr_client.describe_images(repositoryName=repository_name)
    return response['imageDetails']

def get_latest_image_uri(repository_uri, image_tag):
    return f"{repository_uri}:{image_tag}"

def main():
    repositories = get_ecr_repositories()

    for repository in repositories:
        repository_name = repository['repositoryName']
        repository_uri = repository['repositoryUri']
        print(f"Repository: {repository_name}")
        
        images = get_repository_images(repository_name)
        for image in images:
            image_pushedtime = image.get('imagePushedAt')
            image_lastpulltime = image.get('lastRecordedPullTime')
            image_tags = image.get('imageTags', ['<no tags>'])
            image_size = image['imageSizeInBytes']
            latest_image_tag = image_tags[-1] if image_tags else '<no tags>'
            latest_image_uri = get_latest_image_uri(repository_uri, latest_image_tag)
            
            print(f"Latest Image URI: {latest_image_uri}")
            print(f"Image Tags: {image_tags}")
            print(f"Image Size: {image_size} bytes")
            print(f"Pushed At: {image_pushedtime}")
            print(f"Last Pulled At: {image_lastpulltime}")
            print()

if __name__ == '__main__':
    main()
