## Setting up a Simple Web Server

This code snippet sets up a simple web server to host an HTML file.

### Instructions

To run the web server, follow these steps:

1. Save the HTML file to a directory on your local machine.

2. Open a terminal or command prompt.

3. Navigate to the directory where the HTML file is located using the `cd` command.

4. Run the following command to start the web server:

    ```bash
    python -m http.server {port}
    ```

    This command starts a web server on port 8000 by default.

5. Open a web browser and enter the following URL:

    ```
    http://localhost:8000/quotes.html
    ```

    Replace `quotes.html` with the actual filename if it's different.

6. The web browser should now display the HTML file hosted by the web server.

**Note:** Make sure you have Python installed on your machine before running the web server.
