import ftplib
import ssl
from ftplib import FTP
from io import BytesIO
import cv2

from config import ftp_config


class FTP_Server:
    """
    Class created for FTP server communication
    :param debug: Set it to true in case you want to receive more debugging feedback from server
    """
    def __init__(self, debug: bool = False):

        if not ftp_config.use_ftp:
            return

        self.server = ftp_config.server
        self.port = ftp_config.port
        self.user = ftp_config.user
        self.password = ftp_config.password

        self.remote_file_name = 'raw_tomato_data.txt'

        self.ftp = ftplib.FTP()

        if debug:
            self.ftp.set_debuglevel(2)

    def connect(self):
        if not ftp_config.use_ftp:
            return
        try:
            print(f'Connecting to FTP server at {self.server}:{self.port} using TLS...')
            self.ftp.connect(self.server, self.port)
            self.ftp.set_pasv(False)
            self.ftp.login(self.user, self.password)
            print(f'Connected to server {self.server}')
        except Exception as e:
            print(f'Error when connecting to ftp server {self.server} with user {self.user}')
            print(f'Error: {e}')

    def send_data(self, data: bytes, remote_file_name: str = None):
        """
        Base function for sending bytes data into a file on the ftp server
        Note: remote_file_name decides the file extension
        :param data: Bynary data you want to send
        :param remote_file_name: The name of the file you want to send it to
        :return:
        """
        if not ftp_config.use_ftp:
            return

        if self.ftp is None:
            print('You haven\'t logged in ftp server!\n'
                  'Please do so by calling the .connect() function before sending data!')
            return
        if remote_file_name is not None:
            self.remote_file_name = remote_file_name
        try:
            # Upload the file to the current directory (after changing folder)
            print(f'Sending data to {self.remote_file_name}...')
            with BytesIO(data) as file_obj:
                self.ftp.storbinary(f'STOR {self.remote_file_name}', file_obj)
            print(f'Data is uploaded successfully as {self.remote_file_name}')
        except Exception as e:
            print(f'Error when sending data over FTP to server {self.server} with user {self.user}')
            print(f'Error: {e}')

    def send_image_data_from_result(self, result, filename):
        """
        Function dedicated to sending an image from model into a file on the server
        :param result: The results from the model (What detector.model(frame) returns)
        :param filename: The name of the file you want to write it into
        :return:
        """
        try:
            print(f'Processing result to send image as {filename}...')
            annotated_image = result.plot()
            success, buffer = cv2.imencode('.jpg', annotated_image)
            if not success:
                raise ValueError('Failed to encode image using OpenCV!')
            self.remote_file_name = filename
            self.send_data(buffer.tobytes())
        except Exception as e:
            print(f'Error when sending image data over ftp to server {self.server} with user {self.user}')
            print(f'Error: {e}')


ftp_server = FTP_Server()

if __name__ == '__main__':
    ftp_server.connect()
    ftp_server.send_data(b'test', remote_file_name="testfile.txt")  # Test sending to subfolder
    ftp_server.ftp.quit()
