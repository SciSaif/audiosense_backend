-- uploaded_files table to store the uploaded files and their metadata
CREATE TABLE uploaded_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    duration INT NOT NULL,
    fileSize INT NOT NULL,
    fileType VARCHAR(100) NOT NULL,
    uploadDate DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);