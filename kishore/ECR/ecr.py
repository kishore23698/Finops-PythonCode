import boto3

# Initialize Boto3 ECR client
ecr_client = boto3.client('ecr')


def get_ecr_repositories():
    response = ecr_client.describe_repositories()
    return response['repositories']


def get_repository_images(repository_name):
    response = ecr_client.describe_images(repositoryName=repository_name)
    return response['imageDetails']


def main():
    repositories = get_ecr_repositories()

    for repository in repositories:
        repository_name = repository['repositoryName']
        print(f"Repository: {repository_name}")

        images = get_repository_images(repository_name)
        for image in images:
            image_pushedtime = image.get('imagePushedAt')
            image_lastpulltime = image.get('lastRecordedPullTime')
            image_name = image.get('imagename')
            image_tags = image.get('imageTags', ['<no tags>'])
            image_size = image['imageSizeInBytes']
            print(
                f"Image_name: {image_name},- Tags: {image_tags}, Size: {image_size} bytes")
            print(f"lastpulltime: {image_lastpulltime}")
            print(f"pushedAtTime: {image_pushedtime}")


if __name__ == '__main__':
    main()
