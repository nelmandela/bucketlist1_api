"""Tests for bucketlist endpoints."""
import json

from tests import BaseTestCase


class BucketlistTestCase(BaseTestCase):
    """Test for API endpoints."""

    def test_add_bucketlist(self):
        """Test that endpoint adds bucketlists"""
        new_bucketlist = {
                            "name": "Testing"
                        }
        response = self.client.post('/api/v1/bucketlists', data=new_bucketlist,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 201)
        response = json.loads(response.data.decode('utf8'))
        self.assertEqual(response["message"], "Bucketlist created")

    def test_add_existing_bucketlist(self):
        """Test that adding an existing bucketlist fails"""
        response = self.client.post('/api/v1/bucketlists', data=self.bucketlist,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 409)
        response = json.loads(response.data.decode('utf8'))
        self.assertEqual(response["message"], "Bucketlist already exists")

    def test_add_empty_bucketlist(self):
        """Test that endpoint adds bucketlists"""
        new_bucketlist = {
                            "name": ""
                        }
        response = self.client.post('/api/v1/bucketlists', data=new_bucketlist,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.data.decode('utf8'))
        self.assertEqual(response["message"], "Provide a bucketlist name")

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
        response = json.loads(response.data.decode('utf8'))
        self.assertEqual(response["message"], "Bucketlist updated")

    def test_update_bucketlists_with_same_name(self):
        """Test that updating a bucketlist with same name fails"""
        new_bucketlist = {
                            "name": "travel"
                        }
        response = self.client.put('/api/v1/bucketlists/1', data=new_bucketlist,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 409)
        response = json.loads(response.data.decode('utf8'))
        self.assertEqual(response["message"], "Bucketlist already exists")


    def test_update_empty_bucketlists(self):
        """Test that updating empty bucketlist fails"""
        new_bucketlist = {
                            "name": ""
                        }
        response = self.client.put('/api/v1/bucketlists/1', data=new_bucketlist,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.data.decode('utf8'))
        self.assertEqual(response["message"], "Provide a bucketlist name")
    
    def test_delete_buckelists(self):
        """Test that endpoints deletes bucketlists"""
        response = self.client.delete('/api/v1/bucketlists/1',headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data.decode('utf8'))
        self.assertEqual(response["message"], "Item deleted")
    
    def test_delete_empty_buckelists(self):
        """Test that deleting an empty bucketlist fails"""
        response = self.client.delete('/api/v1/bucketlists/66',headers=self.headers)
        self.assertEqual(response.status_code, 404)
        response = json.loads(response.data.decode('utf8'))
        self.assertEqual(response["message"], "Bucketlist not found")


