# Some knowledges learned

If the urls of the backend all end with `/`, when the front end calls it, make sure to add `/` at the end as well, even for GET. Otherwise, those calls may fail in browsers on Apple device or iOS system.

When getting S3 presigned url and showing the doc in google doc viewer, you need to first encode the presigned url and then put the encoded url in google viewer url.

Eb deployment:
- Ed uses AWS credentials of AWS CLI config to deploy the env. The corresponding AWS user must have several eb and ec2 permission policies (like the eb-admin user in our AWS account):
  - AdministratorAccess-AWSElasticBeanstalk,
  - AmazonEC2FullAccess
  - etc.

- To deploy an django app like this one: first create eb env, and then add db, and then add the environmental variables.

- Use environmental variables in config and manage.py to use different prod settings (db, etc).

- Create create super user command and put it in eb container command to create the first super user. (I tried eb ssh and run command manually but failed. So it seems eb ssh is not required)

- make eb allow all hosts (it is ok for rest api server), otherwise the env always show severe status
- To use customer domain name, make a cname record in DNS table pointing to the eb env url.
- To make https, the certificate needs to be added on the load balancer.

S3 host single page application
- To not use any front end router separator like #, need to set up the error page to the index.html
- To use customer domain name, need to make a cname in DNS pointing to the S3 bucket, and the bucket name needs to be the same as the domain name.
- To use https, need to set up cloud front and attach the certificate

Customer domain name and HTTPS
- Customer domain names can be implemented by adding CNAME records.
- SSL certificates can be requested from [AWS Certificate Manager (ACM)](https://aws.amazon.com/certificate-manager/). To verify the domain of the certificate, we need to add another requested CNAME record in your DNS table. 

Receive emails from SES
- There is only one active rule set, but we can add a new rule to take action on some specific email
- To listen to incoming email, we can just add `Deliver to Amazon S3 bucket` action only and then set up lambda listening to the S3 bucket `raw-emails/` directory.
- Each email on S3 is like an .eml file. To decode the text body of an email, we should decode it with `utf-8` like [this example](https://github.com/jianghengle/simple-manager/blob/main/invoice-receiver/lambda_function.py#L30-L32). Otherwise, it might be some incorrect coded texts.
