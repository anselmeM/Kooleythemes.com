<?php
// where the email is being sent
$to = 'Info@kooleythemes.com';

// must originate from this domain
$fromName = 'Kooley Themes';
$fromEmail = 'noreply@kooleythemes.com';
$name = isset($_POST['name']) ? trim($_POST['name']) : '';
$name = filter_var($name, FILTER_SANITIZE_STRING);
$mail = isset($_POST['mail']) ? trim($_POST['mail']) : '';
$mail = filter_var($mail, FILTER_SANITIZE_EMAIL);
$message = isset($_POST['message']) ? trim($_POST['message']) : '';
$message = filter_var($message, FILTER_SANITIZE_STRING);

if (strlen($name) > 0 && strlen($message) > 0 && strlen($mail) > 0) {
        $mailmsg = '
        <strong>Name : </strong> '. $name . '<br><br>
		<strong>Email : </strong> '. $mail .'<br><br>
		<strong>Message : </strong> '. $message .'<br><br>';
		
        $headers   = array();
        $headers[] = "MIME-Version: 1.0";
        $headers[] = "Content-Type: text/html; charset=utf-8";
        $headers[] = "From: " . $fromName ."<" . $fromEmail .">";
        $headers[] = "Reply-To: " . $name ."<" . $mail .">";
        $headers[] = "X-Mailer: PHP/".phpversion();
        if(mail($to, "Request a Quote", $mailmsg, implode("\r\n", $headers))) {
            header('Location: thankyou.html');
        } else {
            echo 'Unable to deliver the message';
        }
} else {
    echo 'All fields are required';
}

?>