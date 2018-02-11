import unittest
import mock
import app

class TestSSHAccess(unittest.TestCase):
    """
    Test post and delete method
    """
    def setUp(self):
        pass
    def tearDown(self):
        pass
    
    @mock.patch.object(app, 'jsonify')
    @mock.patch.object(app, 'request')
    @mock.patch.object(app, 'SSHClient')
    @mock.patch.object(app, 'load')
    @mock.patch.object(app, 'open')
    def test_post_successful(self,m_open, m_load, 
                             m_sshClient, m_reqJson,
                             m_json):
        """
        Add successful
        """
        m_reqJson.json = {'username':'xxxx',
                          'password':'yyyy'}
        m_load.return_value={'allowed_users':['xxxx']}
        m_json.return_value={'Response':'user is authenticated'}
        stdin_, stdout_, stderr_ = mock.MagicMock(), mock.MagicMock(), mock.MagicMock()
        stdout_.channel.recv_exit_status.return_value = 0
        m_sshClient.return_value.exec_command.return_value = stdin_, stdout_, stderr_
        out, status = app.add_ssh()
        self.assertEqual(m_open.call_count, 3)
        self.assertEqual(m_load.call_count, 1)
        self.assertEqual(m_sshClient.call_count, 1)
        assert status == 200
    
    @mock.patch.object(app, 'make_response')
    @mock.patch.object(app, 'jsonify')
    @mock.patch.object(app, 'request')
    @mock.patch.object(app, 'SSHClient')
    @mock.patch.object(app, 'load')
    @mock.patch.object(app, 'open')
    def test_post_fail_user_auth(self,m_open, m_load, 
                                 m_sshClient, m_reqJson,
                                 m_json, m_make_resp):
        """
        add fail at user auth
        """
        m_reqJson.json = {'username':'xxxx',
                          'password':'yyyy'}
        m_load.return_value={'allowed_users':['xxxx']}
        m_json.return_value={'Authentication Error':'User is authenticated already'}
        stdin_, stdout_, stderr_ = mock.MagicMock(), mock.MagicMock(), mock.MagicMock()
        stdout_.channel.recv_exit_status.return_value = 0
        stdout_.read.return_value = "hi"
        m_make_resp.return_value = 400
        m_open.return_value.__enter__.return_value.readlines.return_value = ["hi","hey"]
        m_sshClient.return_value.exec_command.return_value = stdin_, stdout_, stderr_
        app.add_ssh()
        self.assertEqual(m_open.call_count, 2)
        self.assertEqual(m_load.call_count, 1)
        self.assertEqual(m_sshClient.call_count, 1)
        self.assertEqual(m_make_resp.call_count, 1)
    
    @mock.patch.object(app, 'jsonify')
    @mock.patch.object(app, 'make_response')
    @mock.patch.object(app, 'request')
    def test_post_fail_arguments(self, m_req, 
                                 m_make_resp, m_json):
        """
        Add fail at missing arguments
        """
        m_json.return_value = {'Error':'Missing arguements'}
        m_req.json = {'username':'xxxx'}
        m_make_resp.return_value = 400
        app.add_ssh()
        self.assertEqual(m_make_resp.call_count, 1)
    
    @mock.patch.object(app, 'make_response')
    @mock.patch.object(app, 'jsonify')
    @mock.patch.object(app, 'request')
    @mock.patch.object(app, 'load')
    @mock.patch.object(app, 'open')
    def test_post_fail_allowed_users(self,m_open, m_load, 
                                     m_reqJson, m_json,
                                     m_make_resp):
        """
        Add fail at allowed users
        """
        m_reqJson.json = {'username':'xxxx',
                          'password':'yyyy'}
        m_load.return_value={'allowed_users':['zzzz']}
        m_json.return_value={'Authentication Error': "User is not allowed to access the server"}
        m_make_resp.return_value = 400
        app.add_ssh()
        self.assertEqual(m_make_resp.call_count, 1)
        self.assertEqual(m_open.call_count, 1)
        self.assertEqual(m_load.call_count, 1)
        

    @mock.patch.object(app, 'jsonify')
    @mock.patch.object(app, 'request')
    @mock.patch.object(app, 'SSHClient')
    @mock.patch.object(app, 'open')
    def test_delete_successful(self,m_open, m_sshClient, 
                               m_reqJson, m_json):
        """
        Delete successful
        """
        m_reqJson.json = {'username':'xxxx',
                          'password':'yyyy'}
        m_json.return_value={'Response':"Authenticated is removed successfully"}
        stdin_, stdout_, stderr_ = mock.MagicMock(), mock.MagicMock(), mock.MagicMock()
        stdout_.channel.recv_exit_status.return_value = 0
        m_sshClient.return_value.exec_command.return_value = stdin_, stdout_, stderr_
        stdout_.read.return_value = "hi"
        m_open.return_value.__enter__.return_value.readlines.return_value = ["hi","hey"]
        out, status = app.delete_ssh()
        self.assertEqual(m_open.call_count, 2)
        self.assertEqual(m_sshClient.call_count, 1)
        assert status == 200
    
    @mock.patch.object(app, 'make_response')
    @mock.patch.object(app, 'jsonify')
    @mock.patch.object(app, 'request')
    @mock.patch.object(app, 'SSHClient')
    @mock.patch.object(app, 'open')
    def test_delete_fail_auth(self,m_open, m_sshClient, 
                               m_reqJson, m_json, m_make_resp):
        """
        Delete fail at auth
        """
        m_reqJson.json = {'username':'xxxx',
                          'password':'yyyy'}
        m_json.return_value={'Authentication Error':'User is not authenticated already'}
        stdin_, stdout_, stderr_ = mock.MagicMock(), mock.MagicMock(), mock.MagicMock()
        stdout_.channel.recv_exit_status.return_value = 0
        m_sshClient.return_value.exec_command.return_value = stdin_, stdout_, stderr_
        stdout_.read.return_value = "hoo"
        m_make_resp.return_value = 400
        m_open.return_value.__enter__.return_value.readlines.return_value = ["hi","hey"]
        app.delete_ssh()
        self.assertEqual(m_open.call_count, 1)
        self.assertEqual(m_sshClient.call_count, 1)
        self.assertEqual(m_make_resp.call_count, 1)
    
    @mock.patch.object(app, 'make_response')
    @mock.patch.object(app, 'jsonify')
    @mock.patch.object(app, 'request')
    @mock.patch.object(app, 'SSHClient')
    def test_delete_fail_pub(self, m_sshClient, 
                             m_reqJson, m_json,
                             m_make_resp):
        """
        Delete fail at public key
        """
        m_reqJson.json = {'username':'xxxx',
                          'password':'yyyy'}
        m_json.return_value={'Public key error': "Error in reading public key"}
        stdin_, stdout_, stderr_ = mock.MagicMock(), mock.MagicMock(), mock.MagicMock()
        stdout_.channel.recv_exit_status.return_value = 1
        m_sshClient.return_value.exec_command.return_value = stdin_, stdout_, stderr_
        m_make_resp.return_value = 400
        app.delete_ssh()
        self.assertEqual(m_sshClient.call_count, 1)
        self.assertEqual(m_make_resp.call_count, 1)
    
    @mock.patch.object(app, 'jsonify')
    @mock.patch.object(app, 'make_response')
    @mock.patch.object(app, 'request')
    def test_delete_fail_arguments(self, m_req, 
                                 m_make_resp, m_json):
        """
        Delete fail at missing arguments
        """
        m_json.return_value = {'Error':'Missing arguements'}
        m_req.json = {'username':'xxxx'}
        m_make_resp.return_value = 400
        app.delete_ssh()
        self.assertEqual(m_make_resp.call_count, 1)
    


if __name__ == '__main__':
    unittest.main()