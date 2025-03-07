# wearable_integration.py
import requests

def fetch_wearable_data(api_token):
    """
    Connects to a wearable API (example uses a Fitbit-like endpoint)
    and fetches the resting heart rate data.
    """
    headers = {'Authorization': f'Bearer {api_token}'}
    # Replace the URL with the correct endpoint for your wearable device API
    url = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Example extraction; adjust as per your API response structure
        heart_rate = data.get('activities-heart', [{}])[0].get('value', {}).get('restingHeartRate', None)
        return {'heart_rate': heart_rate}
    else:
        return None
