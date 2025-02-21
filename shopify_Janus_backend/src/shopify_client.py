import requests
import os

SHOPIFY_STORE = os.getenv("SHOPIFY_STORE")
SHOPIFY_ADMIN_API_URL = f"https://{SHOPIFY_STORE}/admin/api/2024-01/graphql.json"
HEADERS = {
    "X-Shopify-Access-Token": os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN"),
    "Content-Type": "application/json"
}

def upload_image_to_shopify(image_url):
    """Uploads an image to Shopify."""
    query = """
    mutation fileCreate($files: [FileCreateInput!]!) {
        fileCreate(files: $files) {
            files { id url }
            userErrors { field message }
        }
    }
    """
    variables = {"files": [{"originalSource": image_url, "contentType": "IMAGE"}]}

    response = requests.post(SHOPIFY_ADMIN_API_URL, headers=HEADERS, json={"query": query, "variables": variables})
    return response.json()

def create_shopify_product(title, image_url):
    """Creates a Shopify product with the AI-generated image."""
    query = """
    mutation {
        productCreate(input: {
            title: "%s",
            images: [{ src: "%s" }]
        }) {
            product {
                id
                title
                onlineStoreUrl
            }
            userErrors { field message }
        }
    }
    """ % (title, image_url)

    response = requests.post(SHOPIFY_ADMIN_API_URL, headers=HEADERS, json={"query": query})
    return response.json()