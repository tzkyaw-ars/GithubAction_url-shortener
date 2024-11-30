import pytest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, generate_short_code

def test_home_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_short_code_generation():
    # Test multiple short code generations
    codes = set()
    for _ in range(100):
        code = generate_short_code()
        assert len(code) == 6
        assert code not in codes
        codes.add(code)

def test_url_shortening():
    client = app.test_client()
    response = client.post('/', data={'url': 'https://example.com'})
    assert response.status_code == 200
    assert b'http://' in response.data