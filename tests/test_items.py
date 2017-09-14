"""Tests for items endpoints."""
import json

from tests import BaseTestCase


class ItemlistTestCase(BaseTestCase):
    """Test for API endpoints."""

    def setUp(self):
        BaseTestCase.setUp(self)
        self.item = {
            "name": "item 1"
        }
        self.item2 = {
            "name": "item 2"
        }
        response = self.client.post('/api/v1/bucketlists/1/items', data=self.item2,
                                    headers=self.headers)

    def test_add_item(self):
        response = self.client.post('/api/v1/bucketlists/1/items', data=self.item,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 201)
        response = json.loads(response.data.decode('utf8'))
        self.assertEqual(response["message"], "Item created")

    def test_register_existing_item(self):
        response = self.client.post('/api/v1/bucketlists/1/items', data=self.item2,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode('utf8'))
        self.assertIn(response_msg['message'],"Item already exists")

    def test_item_name_required(self):
        item = {
            "name": ""
        }
        response = self.client.post('/api/v1/bucketlists/1/items', data=item,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode('utf8'))
        self.assertIn(response_msg['message'],"Provide an item name")

    
    def test_get_items(self):
        """Test that endpoint fetches all items."""
        new_item = {
            "name": "Hiking"
        }
        response = self.client.post('/api/v1/bucketlists/1/items', data=new_item,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 201)
        response = self.client.get("/api/v1/bucketlists/1/items",
                                   headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(json.loads(response.data)) == 2)
        response = json.loads(response.data)
        self.assertEqual(len(response), 2)

    def test_update_items(self):
        """Test that endpoint updates item"""
        new_item = {
                            "name": "Hiking"
                        }
        response = self.client.put('/api/v1/bucketlists/1/items/1', data=new_item,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode('utf8'))
        self.assertIn(response_msg['message'],"Item updated")

    def test_update_items_with_invalid_token(self):
        """Test if endpoint updates item without a valid token"""
        new_item = {
                            "name": "Hiking"
                        }
        response = self.client.put('/api/v1/bucketlists/1/items/1', data=new_item,
                                    headers=self.headers_2)
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode('utf8'))
        self.assertIn(response_msg['message'],"Bucketlist not found")

    def test_update_items_with_same_name(self):
        """Test if endpoint updates item with same name"""
        new_item = {
                            "name": "CapeTown"
                        }
        response = self.client.put('/api/v1/bucketlists/1/items/1', data=new_item,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode('utf8'))
        self.assertIn(response_msg['message'],"Pro1 a username")

    def test_update_empty_items(self):
        """Test if endpoint updates an empty item"""
        new_item = {
                            "name": ""
                        }
        response = self.client.put('/api/v1/bucketlists/1/items/1', data=new_item,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode('utf8'))
        self.assertIn(response_msg['message'],"Provide an item name")

    def test_delete_items(self):
        """Test that endpoints deletes items"""
        response = self.client.delete('/api/v1/bucketlists/1/items/1',headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode('utf8'))
        self.assertIn(response_msg['message'],"Item deleted")    

    # def test_delete_items_invalid_token(self):
    #     """Test that endpoints deletes items"""
    #     response = self.client.delete('/api/v1/bucketlists/1/items/1',headers=self.headers_2)
    #     self.assertEqual(response.status_code, 404)
    #     response_msg = json.loads(response.data.decode('utf8'))
    #     self.assertIn(response_msg['message'],"Bucketlist not found")

    def test_delete_empty_items(self):
        """Test if endpoints deletes items"""
        response = self.client.delete('/api/v1/bucketlists/1/items/66',headers=self.headers)
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode('utf8'))
        self.assertIn(response_msg['message'],"Item not found")
