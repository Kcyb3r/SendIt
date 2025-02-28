# SendIt
![image](https://github.com/user-attachments/assets/dccd6989-8df2-4f50-99fa-d40c68fc0d93)



<div class="logo">
    <img src="images/sendit-logo.png" alt="SendIt Logo" class="sendit-logo" />
</div>
  .logo {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px; /* Adjust margin as needed */
}

.sendit-logo {
    width: 150px; /* Adjust size as needed */
    height: auto; /* Maintain aspect ratio */
}



SendIt is a simple and efficient file transfer tool that allows users to send and receive files over a network using a graphical user interface (GUI). Built with Python and Tkinter, SendIt leverages SSL for secure file transfers.

## Features

- **Secure File Transfer**: Uses SSL to encrypt the connection between sender and receiver.
- **User-Friendly Interface**: Easy-to-use GUI for selecting files and managing transfers.
- **File History**: Keeps track of received files with timestamps.
- **Cross-Platform**: Works on any platform that supports Python and Tkinter.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- OpenSSL (for SSL support)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kcyb3r/SendIt.git
   cd SendIt
   ```

2. **Install Dependencies**:
   Ensure you have Python and OpenSSL installed. You can install any additional dependencies using pip if needed.

## Usage

1. **Launch the Application**:
   - Run the application by executing the following command in your terminal:
     ```bash
     python sendit.py
     ```

2. **Generate Unique Connection Code**:
   - Upon launching, the application will automatically generate a unique connection code displayed in the "Unique Connection Code" field.

3. **Choose an Action**:
   - Click on **"Send File"** to send a file to another machine.
   - Click on **"Start Receiving"** to receive a file from another machine.

4. **Sending a File**:
   - After clicking **"Send File"**, a file dialog will open. Navigate to the file you want to send and select it.
   - The application will start the server in the background and attempt to send the file to the specified address (default is `127.0.0.1` on port `65432`).

5. **Receiving a File**:
   - If you clicked **"Start Receiving"**, the server will start listening for incoming files. Once a file is sent from the sender's machine, it will be saved in the `received_files` directory.

6. **View Transfer Status**:
   - The application will display messages indicating the status of the file transfer (e.g., "File 'filename' sent successfully!" or "File 'filename' received successfully!").
   - You can also view the history of received files in the "Received Files History" section.

7. **Close the Application**:
   - To exit the application, click the **"X"** button in the title bar or use the minimize button to keep it running in the background.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Python community for their support and resources.
- Special thanks to the developers of Tkinter and OpenSSL for their contributions to secure file transfer.
