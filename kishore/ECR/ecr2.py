import boto3

# Initialize Boto3 ECR client
ecr_client = boto3.client('ecr')

def get_ecr_repositories():
    response = ecr_client.describe_repositories()
    return response['repositories']

def get_repository_images(repository_name):
    response = ecr_client.describe_images(repositoryName=repository_name)
    return response['imageDetails']

def get_image_uri(repository_name, image_digest):
    response = ecr_client.batch_get_image(repositoryName=repository_name, imageIds=[{'imageDigest': image_digest}])
    return response['images'][0]['imageManifest']

def main():
    repositories = get_ecr_repositories()

    for repository in repositories:
        repository_name = repository['repositoryName']
        print(f"Repository: {repository_name}")

        images = get_repository_images(repository_name)
        for image in images:
            image_pushedtime = image.get('imagePushedAt')
            image_lastpulltime = image.get('lastRecordedPullTime')
            image_name = image.get('imageTags', ['<no tags>'])
            image_size = image['imageSizeInBytes']
            image_digest = image['imageDigest']
            
            # Retrieve image URI using the repository name and image digest
            image_uri = get_image_uri(repository_name, image_digest)
            
            print(f"Image Name: {image_name}, Tags: {image.get('imageTags', ['<no tags>'])}, Size: {image_size} bytes")
            print(f"Last Pull Time: {image_lastpulltime}")
            print(f"Pushed At Time: {image_pushedtime}")
            print(f"Image URI: {image_uri}")

if __name__ == '__main__':
    main()
