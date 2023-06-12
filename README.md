## Store-Image-to-S3-using-Lambda
- Creating IAM user for restricted access of different AWS resources like S3 and lambda.
- Creating a s3 bucket and setting its permissions so that we can upload files.
- Creating Lambda function and setting its trigger as S3.
- Send an email features when the file is uploaded to S3.
- Lambda function to create and add thumbnail if uploaded file is image

### Step 1: Create an IAM User
    In the search bar, type "IAM" and select the IAM service.
    In the IAM dashboard, select the "Roles" option from the left-hand navigation bar.
    Click the "Add user" button to create a new role for S3 and SES Access.
    Select the entity type as “AWS Service” and use case as “Lambda” and click on “Next” button.
    Now search and select “AmazonSESFullAccess” & “AWSLambdaExecute” in Add Permission section,
    and click on “Next” button. Also, review your settings and select “Add Role” button to create your IAM Roles.


### Step 2: Create a Lambda function to trigger S3 events
    In the search bar, type "Lambda" and select the Lambda service.
    In the Lambda dashboard, select the "Create a function" option from the right-hand navigation bar.
    Select the function type as “Author from Scratch”.
    Give the function a unique name. And select the runtime as “python 3.10”. Leave other settings as it is.
    Scroll down to Execution Role, select “Use an existing role” and select the role that we created earlier from the dropdown.
    Click on “Create function” button.


### Step 3: Create two S3 buckets for uploading documents and viewing thumbnails
    In the search bar, type "S3" and select the S3 service.
    In the S3 dashboard, select the "Create Bucket" option from the right-hand navigation bar.
    Give the Bucket name (Note*: Should be unique). Select the region where the bucket needs to be created.
    De-select the Block all public access setting for this bucket (If you want to access the documents via public URL) else let it as it is.
    Click on “Create Bucket” and wait till it gets created.
    REPEAT THE ABOVE STEPS AGAIN TO CREATE BUCKET TO STORE THUMBNAIL IMAGES.
    Now select the main bucket where you will be uploading items and go into “Properties” section.
    Search for “Event Notifications” and click on “Create Event Notification”
    Now give the event a name and select “Put” as the event type.
    Now scroll down to “destination” section and select “Lambda function” as destination
    and choose your Lambda function from the dropdown that we created earlier. And click on “Save Changes”.


### Step 4: Write a code for the Lambda function that triggers S3 events
    Write the code for the Lambda function in the file "lambda_function.py".


### Step 5: Verify Email through Amazon Simple Email Service to avail notification
    In the search bar, type "SES" and select the Simple Email Service service.
    In the SES dashboard, select the "Create identity" option from the right-hand navigation bar.
    Click on “Email address” in identity type and enter the email address and click on create identity.
    Check your mailbox and verify your email to start the testing.


### Step 6: Test the code
    Go to the main S3 bucket and click on Upload.
    Select Add files and upload any document (Image to see the thumbnail) and click on Upload.
    Now go to the S3 thumbnail bucket

