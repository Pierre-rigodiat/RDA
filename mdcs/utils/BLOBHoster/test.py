import unittest
from utils.BLOBHoster.BLOBHosterFactory import BLOBHosterFactory


class TestGridFS(unittest.TestCase):
    def setUp(self):
        print "In method ", self._testMethodName
        BLOB_HOSTER = 'GridFS'
        BLOB_HOSTER_USER = "mgi_user"
        BLOB_HOSTER_PSWD = "mgi_password"
        BLOB_HOSTER_URI = "mongodb://" + BLOB_HOSTER_USER + ":" + BLOB_HOSTER_PSWD + "@localhost/mgi"
        MDCS_URI = 'http://127.0.0.1:8000'
        
        blobHosterFactory = BLOBHosterFactory(BLOB_HOSTER, BLOB_HOSTER_URI, BLOB_HOSTER_USER, BLOB_HOSTER_PSWD, MDCS_URI)
        self.blobHoster = blobHosterFactory.createBLOBHoster()
            
    def testSetGetText(self):              
        text = 'test'       
        handle = self.blobHoster.save(text)        
        out = self.blobHoster.get(handle)
        print text + " = " + out
        self.assertEqual(text, out)
    
#     def testSetGetImage(self):
#         import base64
#         with open('Penguins.jpg','rb') as imageFile:
#             imageStr = base64.b64encode(imageFile.read())
#             handle = self.blobHoster.save(imageStr)        
#         out = self.blobHoster.get(handle)
#         self.assertEqual(imageStr, out)
#         fh = open("Penguins.out.jpg", "wb")
#         fh.write(out.decode('base64'))
#         fh.close()

    def testSetGetImage(self):
        with open('Penguins.jpg','rb') as imageFile:
            handle = self.blobHoster.save(imageFile)        
        
        out = self.blobHoster.get(handle)
        
        with open("Penguins.out.jpg", "wb") as imageFile:
            imageFile.write(out)        
        
    def testList(self):
        handles = self.blobHoster.list()
        
if __name__ == '__main__':
    unittest.main()
    