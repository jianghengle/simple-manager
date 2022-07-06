rm my-deployment-package.zip
cd venv/lib/python3.9/site-packages
zip -r ../../../../my-deployment-package.zip .
cd ../../../../
zip -g my-deployment-package.zip lambda_function.py