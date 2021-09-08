# Login

![](../assets/hackandwin/login/loginpage.png)

This login page is vulnerable to [SQL injection](https://owasp.org/www-community/attacks/SQL_Injection). This is its source:

```php+HTML
<?php 
    try {            
        switch ($_SESSION["security-level"]){
            case "0": // This code is insecure.
                $lEnableJavaScriptValidation = FALSE;
                $lEnableHTMLControls = FALSE;
            break;
            case "1": // This code is insecure.
                $lEnableJavaScriptValidation = TRUE;
                $lEnableHTMLControls = TRUE;
            break;
               case "2":
               case "3":
               case "4":
            case "5": // This code is fairly secure
                $lEnableJavaScriptValidation = TRUE;
                $lEnableHTMLControls = TRUE;
            break;
        }// end switch
    } catch(Exception $e){
        echo $CustomErrorHandler->FormatError($e, "Error setting up configuration.");
    }// end try    
?>
<script type="text/javascript">
<!--
    <?php 
        if ($_SESSION["loggedin"]=="True") {
            echo "var l_loggedIn = true;" . PHP_EOL;
        }else {
            echo "var l_loggedIn = false;" . PHP_EOL;
        }// end if
        if (isset($lAuthenticationAttemptResult)){
            echo "var lAuthenticationAttemptResultFlag = {$lAuthenticationAttemptResult};" . PHP_EOL;
        }else{
            echo "var lAuthenticationAttemptResultFlag = -1;".PHP_EOL;
        }// end if
        if($lEnableJavaScriptValidation){
            echo "var lValidateInput = \"TRUE\"" . PHP_EOL;
        }else{
            echo "var lValidateInput = \"FALSE\"" . PHP_EOL;
        }// end if        
    ?>
    function onSubmitOfLoginForm(/*HTMLFormElement*/ theForm){
        try{
            if(lValidateInput == "TRUE"){
                var lUnsafeCharacters = /[`~!@#$%^&*()-_=+\[\]{}\\|;':",./<>?]/;
                if (theForm.username.value.length > 15 || 
                    theForm.password.value.length > 15){
                        alert('Username too long. We dont want to allow too many characters.\n\nSomeone might have enough room to enter a hack attempt.');
                        return false;
                };// end if
                if (theForm.username.value.search(lUnsafeCharacters) > -1 || 
                    theForm.password.value.search(lUnsafeCharacters) > -1){
                        alert('Dangerous characters detected. We can\'t allow these. This all powerful blacklist will stop such attempts.\n\nMuch like padlocks, filtering cannot be defeated.\n\nBlacklisting is l33t like l33tspeak.');
                        return false;
                };// end if
            };// end if(lValidateInput)
            return true;
        }catch(e){
            alert("Error: " + e.message);
        };// end catch
    };// end function onSubmitOfLoginForm(/*HTMLFormElement*/ theForm)
//-->
</script>
<!-- Bubble hints code -->
<?php 
    try{
           $lReflectedXSSExecutionPointBallonTip = $BubbleHintHandler->getHint("ReflectedXSSExecutionPoint");
           $lSQLInjectionPointBallonTip = $BubbleHintHandler->getHint("SQLInjectionPoint");
    } catch (Exception $e) {
        echo $CustomErrorHandler->FormatError($e, "Error attempting to execute query to fetch bubble hints.");
    }// end try
?>
<script type="text/javascript">
    $(function() {
        $('[ReflectedXSSExecutionPoint]').attr("title", "<?php echo $lReflectedXSSExecutionPointBallonTip; ?>");
        $('[ReflectedXSSExecutionPoint]').balloon();
        $('[SQLInjectionPoint]').attr("title", "<?php echo $lSQLInjectionPointBallonTip; ?>");
        $('[SQLInjectionPoint]').balloon();        
    });
</script>
<div class="page-title">Login</div>
<?php include_once (__ROOT__.'/includes/back-button.inc');?>
<?php include_once (__ROOT__.'/includes/hints/hints-menu-wrapper.inc'); ?>
<div id="id-log-in-form-div" style="display: none; text-align:center;">
    <form     action="index.php?page=login.php"
            method="post" 
            enctype="application/x-www-form-urlencoded" 
            onsubmit="return onSubmitOfLoginForm(this);"
            id="idLoginForm">
        <table style="margin-left:auto; margin-right:auto;">
            <tr id="id-authentication-failed-tr" style="display: none;">
                <td id="id-authentication-failed-td" colspan="2" class="error-message"></td>
            </tr>
            <tr><td></td></tr>
            <tr>
                <td colspan="2" class="form-header">Please sign-in</td>
            </tr>
            <tr><td></td></tr>
            <tr>
                <td class="label">Username</td>
                <td>
                    <input    SQLInjectionPoint="1" type="text" name="username" size="20"
                            autofocus="autofocus"
                    <?php
                        if ($lEnableHTMLControls) {
                            echo('minlength="1" maxlength="15" required="required"');
                        }// end if
                    ?>
                    />
                </td>
            </tr>
            <tr>
                <td class="label">Password</td>
                <td>
                    <input SQLInjectionPoint="1" type="password" name="password" size="20"
                    <?php
                        if ($lEnableHTMLControls) {
                            echo('minlength="1" maxlength="15" required="required"');
                        }// end if
                    ?>
                    />
                </td>
            </tr>
            <tr><td></td></tr>
            <tr>
                <td colspan="2" style="text-align:center;">
                    <input name="login-php-submit-button" class="button" type="submit" value="Login" />
                </td>
            </tr>
            <tr><td></td></tr>
            <tr>
                <td colspan="2" style="text-align:center; font-style: italic;">
                    Dont have an account? <a href="index.php?page=register.php">Please register here</a>
                </td>
            </tr>
        </table>
    </form>
</div>
<div id="id-log-out-div" style="text-align: center; display: none;">
    <table>
        <tr>
            <td ReflectedXSSExecutionPoint="1" colspan="2" class="hint-header">You are logged in as <?php echo $_SESSION['logged_in_user']; ?></td>
        </tr>
        <tr><td></td></tr>
        <tr><td></td></tr>
        <tr>
            <td colspan="2" style="text-align:center;">
                <input class="button" type="button" value="Logout" onclick="document.location='index.php?do=logout'" />
            </td>
        </tr>
    </table>    
</div>
<script type="text/javascript">
    var cUNSURE = -1;
       var cACCOUNT_DOES_NOT_EXIST = 0;
       var cPASSWORD_INCORRECT = 1;
       var cNO_RESULTS_FOUND = 2;
       var cAUTHENTICATION_SUCCESSFUL = 3;
       var cAUTHENTICATION_EXCEPTION_OCCURED = 4;
       var cUSERNAME_OR_PASSWORD_INCORRECT = 5;
       var lMessage = "";
       var lAuthenticationFailed = "FALSE";
    switch(lAuthenticationAttemptResultFlag){
           case cACCOUNT_DOES_NOT_EXIST: 
                  lMessage="Account does not exist"; lAuthenticationFailed = "TRUE";
                  break;
           case cPASSWORD_INCORRECT: 
                  lMessage="Password incorrect"; lAuthenticationFailed = "TRUE"; 
                  break;
           case cNO_RESULTS_FOUND: 
                  lMessage="No results found"; lAuthenticationFailed = "TRUE"; 
                  break;
           case cAUTHENTICATION_EXCEPTION_OCCURED: 
                  lMessage="Exception occurred"; lAuthenticationFailed = "TRUE"; 
           break;
           case cUSERNAME_OR_PASSWORD_INCORRECT: 
                  lMessage="Username or password incorrect"; lAuthenticationFailed = "TRUE"; 
           break;
       };
    if(lAuthenticationFailed=="TRUE"){
        document.getElementById("id-authentication-failed-tr").style.display="";
        document.getElementById("id-authentication-failed-td").innerHTML=lMessage;
    }// end if AuthenticationAttemptResultFlag
    if (!l_loggedIn){
        document.getElementById("id-log-in-form-div").style.display="";
        document.getElementById("id-log-out-div").style.display="none";
    }else{
        document.getElementById("id-log-in-form-div").style.display="none";
        document.getElementById("id-log-out-div").style.display="";        
    }// end if l_loggedIn    
</script>
```

##  Testing

I'd rather just start testing than spend time auditing the code, since there probably isn't a very high bar for this SQL injection. To check for any SQL I'll start off by trying the user name "admin'--" and the password "aaa"

![](../assets/hackandwin/login/loginfirstcheck.png)

This error is helpful, and tells us that the website is running [mySQL](https://www.mysql.com/) and that we were able to insert a SQL comment. This is the query that was executed:

```mysql
) Query: SELECT username FROM accounts WHERE username='admin'--'; (0) [Exception] 
```

This query caused an exception because of the odd number of commas. Since the website is already wrapping up our input in two commas, adding a second comma after our comment (the --) would mean that there is an even number of comments (making our query valid) and should cause the comment to be run, and thus cause the rest of the query (the password check) to be evaluated to true.

Lo and behold, this works!

![](../assets/hackandwin/login/loginchecksecond.png)

![](../assets/hackandwin/login/loginsuccess.png)
