import urllib.parse
import urllib.request
import json
import sys

def get_duckduckgo_instant_answer(query):
    """
    Fetches an instant answer from DuckDuckGo without an API key.
    This demonstrates a free and API-key-less way to get web information
    using only Python's standard library.
    """
    encoded_query = urllib.parse.quote(query)
    # DuckDuckGo Instant Answer API endpoint is public and does not require an API key.
    # 'format=json': requests a JSON response.
    # 'no_html=1': removes HTML tags from text fields.
    # 'skip_disambig=1': attempts to skip disambiguation pages for a more direct answer.
    url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1&skip_disambig=1"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))

        # The 'AbstractText' field provides a concise summary.
        # 'AbstractURL' provides a link to the source of the information.
        abstract_text = data.get('AbstractText')
        abstract_url = data.get('AbstractURL')
        heading = data.get('Heading')

        if abstract_text:
            print(f"Query: {query}")
            print(f"--- Instant Answer ---")
            print(f"Topic: {heading if heading else 'N/A'}")
            print(f"Summary: {abstract_text}")
            if abstract_url:
                print(f"Source URL: {abstract_url}")
            print(f"----------------------")
        elif data.get('RelatedTopics'):
            # If no direct abstract, display the first few related topics if available.
            print(f"Query: {query}")
            print(f"--- Related Topics Found (no direct abstract) ---")
            for topic in data['RelatedTopics'][:3]: # Show up to 3 related topics
                if isinstance(topic, dict) and 'Text' in topic:
                    print(f"- {topic['Text']}")
                    if 'FirstURL' in topic:
                        print(f"  URL: {topic['FirstURL']}")
            print(f"------------------------------------------------")
        else:
            print(f"No instant answer or related topics found for '{query}'.")

    except urllib.error.URLError as e:
        print(f"Error connecting to DuckDuckGo: {e}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON response from DuckDuckGo.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        search_query = " ".join(sys.argv[1:])
    else:
        search_query = input("Enter your search query: ")

    if search_query:
        get_duckduckgo_instant_answer(search_query)
    else:
        print("Please provide a search query.")
