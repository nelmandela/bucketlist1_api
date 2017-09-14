"""Tests for bucketlist endpoints."""
import json

from tests import BaseTestCase


class BucketlistTestCase(BaseTestCase):
    """Test for API endpoints."""

    def test_add_bucketlist(self):
        new_bucketlist = {
                            "name": "Testing"
                        }
        response = self.client.post('/api/v1/bucketlists', data=new_bucketlist,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 201)

    def test_register_existing_bucketlist(self):
        response = self.client.post('/api/v1/bucketlists', data=self.bucketlist,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 409)

    def test_add_empty_bucketlist(self):
        new_bucketlist = {
                            "name": ""
                        }
        response = self.client.post('/api/v1/bucketlists', data=new_bucketlist,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_get_bucketlists(self):
        """Test that endpoint fetches all bucketlists."""
        new_bucketlist = {
                            "name": "Testing"
                        }
        response = self.client.post('/api/v1/bucketlists', data=new_bucketlist,
                                    headers=self.headers)

        self.assertEqual(response.status_code, 201)
        response = self.client.get("/api/v1/bucketlists",
                                   headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(json.loads(response.data)) == 2)


    def test_update_bucketlists(self):
        """Test that endpoint updates bucketlist"""
        new_bucketlist = {
                            "name": "Testing"
                        }
        response = self.client.put('/api/v1/bucketlists/1', data=new_bucketlist,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_update_bucketlists_invalid_token(self):
        """Test that endpoint updates bucketlist"""
        new_bucketlist = {
                            "name": "Testing"
                        }
        response = self.client.put('/api/v1/bucketlists/1', data=new_bucketlist,
                                    headers=self.headers_2)
        self.assertEqual(response.status_code, 404)

    def test_update_bucketlists_with_same_name(self):
        """Test that endpoint updates bucketlist"""
        new_bucketlist = {
                            "name": "travel"
                        }
        response = self.client.put('/api/v1/bucketlists/1', data=new_bucketlist,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 409)


    def test_update_empty_bucketlists(self):
        """Test that endpoint updates bucketlist"""
        new_bucketlist = {
                            "name": ""
                        }
        response = self.client.put('/api/v1/bucketlists/1', data=new_bucketlist,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 400)
    
    def test_delete_buckelists(self):
        """Test that endpoints deletes bucketlists"""
        response = self.client.delete('/api/v1/bucketlists/1',headers=self.headers)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_buckelists_invalid_token(self):
        """Test that endpoints deletes bucketlists"""
        response = self.client.delete('/api/v1/bucketlists/1',headers=self.headers_2)
        self.assertEqual(response.status_code, 404)
    
    def test_delete_empty_buckelists(self):
        """Test that endpoints deletes bucketlists"""
        response = self.client.delete('/api/v1/bucketlists/66',headers=self.headers)
        self.assertEqual(response.status_code, 404)


