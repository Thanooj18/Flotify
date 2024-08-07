<?php
$servername = "localhost";
$username = "root"; // Replace with your MySQL username
$password = "prudhvi";     // Replace with your MySQL password
$dbname = "user_data"; // Replace with your database name

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Signup Logic
if (isset($_POST["signup"])) {
    $email = $_POST["email"];
    $password = $_POST["password"];

    // Hash the password securely
    $hashed_password = password_hash($password, PASSWORD_BCRYPT);

    $sql = "INSERT INTO users (email, password) VALUES ('$email', '$hashed_password')";
    
    if ($conn->query($sql) === true) {
        echo "Signup successful!";
    } else {
        echo "Error: " . $conn->error;
    }
}

// Login Logic
if (isset($_POST["login"])) {
    $email = $_POST["email"];
    $password = $_POST["password"];

    $sql = "SELECT password FROM users WHERE email='$email'";
    $result = $conn->query($sql);

    if ($result->num_rows == 1) {
        $row = $result->fetch_assoc();
        if (password_verify($password, $row["password"])) {
            echo "Login successful!";
            // Redirect or perform actions
        } else {
            echo "Invalid password!";
        }
    } else {
        echo "User not found!";
    }
}

// Close the database connection
$conn->close();
?>
