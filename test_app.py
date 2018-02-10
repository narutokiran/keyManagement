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
        m_json.return_value={'Response':'user is authenticated'}
        stdin_, stdout_, stderr_ = mock.MagicMock(), mock.MagicMock(), mock.MagicMock()
        stdout_.channel.recv_exit_status.return_value = 0
        m_sshClient.return_value.exec_command.return_value = stdin_, stdout_, stderr_
        stdout_.read.return_value = "hi"
        m_open.return_value.__enter__.return_value.readlines.return_value = ["hi","hey"]
        out, status = app.delete_ssh()
        self.assertEqual(m_open.call_count, 2)
        self.assertEqual(m_sshClient.call_count, 1)
        assert status == 200


if __name__ == '__main__':
    unittest.main()